# 배치 모드 "주제 부연 설명(topic_context)" 추가 설계

## 배경 / 문제

배치 생성 모드(`web/components/content_input.py`의 `render_content_input()` batch 분기)는
줄바꿈으로 구분된 topic 문자열 목록만 입력받는다. 각 topic은 그대로
`TOPIC_NARRATION_PROMPT`의 `{topic}` 자리에 들어가 LLM에 전달된다
(`pixelle_video/prompts/topic_narration.py` → `pixelle_video/utils/content_generators.py`
`generate_narrations_from_topic()` → `pixelle_video/pipelines/standard.py`
`generate_content()` → `web/utils/batch_manager.py` `SimpleBatchManager.execute_batch()`).

문제: `"인정 욕구를 이용한 통제"` 같은 제목만으로는 LLM이 어떤 관점/영역(예: 다크 심리학)으로
내용을 써야 할지 판단하기 어렵다. 싱글 모드는 입력창이 자유 텍스트라 사용자가 이미
제목+설명을 한 번에 적을 수 있지만, 배치 모드는 "1줄 = 1개 topic"이라는 제약 때문에
설명을 넣을 자리가 없다.

## 요구사항

- 배치 실행 1회에 적용되는 **공통 부연 설명 필드**를 하나 추가한다 (topic별 개별 설명은 지원하지 않음 — YAGNI).
- 부연 설명이 비어 있으면 기존 동작과 100% 동일해야 한다 (싱글 모드, 배치 모드 모두 회귀 없음).
- 부연 설명이 있으면 LLM 프롬프트에서 "제목(topic)"과 "맥락/방향(context)"을 구조적으로
  분리해서 전달한다 — 단순 문자열 이어붙이기(`f"{topic}\n{context}"`)는 하지 않는다.

## 데이터 흐름

```
web/components/content_input.py (batch UI)
  └─ 새 st.text_area → topic_context 문자열 → 반환 dict에 포함
        ↓
web/components/output_preview.py: render_batch_output()
  └─ shared_config["topic_context"] = video_params.get("topic_context") or None
        ↓ (수정 불필요 — 기존 generic 병합 로직이 그대로 처리)
web/utils/batch_manager.py: SimpleBatchManager.execute_batch()
  └─ shared_config의 None이 아닌 키를 모두 task_params에 병합
  └─ pixelle_video.generate_video(**task_params) 호출
        ↓
pixelle_video/service.py: generate_video_wrapper → pipeline_instance(text=text, **kwargs)
pixelle_video/pipelines/linear.py: __call__()
  └─ ctx = PipelineContext(input_text=text, params=kwargs, ...)  # kwargs 그대로 params가 됨
        ↓
pixelle_video/pipelines/standard.py: generate_content()
  └─ topic_context = ctx.params.get("topic_context")
  └─ generate_narrations_from_topic(..., topic_context=topic_context)
        ↓
pixelle_video/utils/content_generators.py: generate_narrations_from_topic()
  └─ build_topic_narration_prompt(..., topic_context=topic_context)
        ↓
pixelle_video/prompts/topic_narration.py: build_topic_narration_prompt()
  └─ topic_context가 있으면 "# Additional Context / Direction" 블록 생성, 없으면 빈 문자열
  └─ TOPIC_NARRATION_PROMPT.format(..., topic_context_block=block)
```

`batch_manager.py`는 이미 `shared_config`의 모든 (None이 아닌) 키를 제네릭하게
`task_params`에 병합하고, `LinearVideoPipeline.__call__`도 `kwargs`를 그대로
`ctx.params`에 저장하므로 **`batch_manager.py`와 `linear.py`는 수정하지 않는다.**

## 변경 파일

### 1. `pixelle_video/prompts/topic_narration.py`
- `TOPIC_NARRATION_PROMPT`에서 `# Input Topic\n{topic}` 다음 줄에 `{topic_context_block}` 플레이스홀더 추가.
- `build_topic_narration_prompt()` 시그니처에 `topic_context: str | None = None` 추가.
  - 값이 있으면:
    ```
    \n# Additional Context / Direction\n{context}\n\nUse the above context to guide the specific angle, tone, and direction of the narrations. The Input Topic above is the headline; this context tells you which specific perspective to take.\n
    ```
    형태의 블록 문자열 생성.
  - 값이 없으면 빈 문자열(`""`) → 섹션 자체가 렌더링되지 않음 (기존 동작과 동일한 결과물).

### 2. `pixelle_video/utils/content_generators.py`
- `generate_narrations_from_topic()`에 `topic_context: Optional[str] = None` 파라미터 추가,
  `build_topic_narration_prompt(...)` 호출 시 전달.

### 3. `pixelle_video/pipelines/standard.py`
- `generate_content()` (mode == "generate" 분기)에서 `ctx.params.get("topic_context")`를 읽어
  `generate_narrations_from_topic(...)` 호출에 전달.

### 4. `web/components/content_input.py`
- 배치 분기 (`topics` 입력 아래, `title_prefix` 입력 위)에 새 `st.text_area` 추가:
  - `tr("batch.topic_context_label")`, placeholder `tr("batch.topic_context_placeholder")`,
    help `tr("batch.topic_context_help")`
  - 선택 입력 (빈 값 허용)
- 반환 dict에 `"topic_context": topic_context_input.strip()` 추가 (빈 문자열 허용).

### 5. `web/components/output_preview.py`
- `render_batch_output()`의 `shared_config` 딕셔너리에
  `"topic_context": video_params.get("topic_context") or None` 한 줄 추가.

### 6. `web/i18n/locales/{ko_KR,en_US,zh_CN}.json`
- 신규 키 3개: `batch.topic_context_label`, `batch.topic_context_placeholder`, `batch.topic_context_help`.
- `ko_KR.json`은 기존 `batch.*` 키들의 과장된/유머러스한 톤(예: "뼈대가 부러질 수 있습니다")을 유지.
- `en_US.json` / `zh_CN.json`은 기존처럼 평이한 톤으로 작성.

## 범위 밖 (하지 않음)

- 싱글 모드 UI 변경 (이미 자유 텍스트 입력이라 필요 없음)
- topic별 개별 부연 설명 (배치 전체 공통 1개로 한정)
- `min_narration_words` / `max_narration_words` 같은 무관한 UI 노출 개선
- 새로운 프리셋/컨셉 관리 시스템 (과한 확장 — YAGNI)

## 에러 처리

- `topic_context`가 공백만 있는 문자열인 경우 `.strip()` 후 빈 문자열이면 `None`과 동일하게 처리
  (블록 미생성).
- 기존 파라미터들과 동일하게 별도 유효성 검증(길이 제한 등)은 추가하지 않는다 — 다른 자유 텍스트
  입력(예: 싱글 모드 topic, title_prefix)과 동일한 신뢰 수준으로 취급.

## 테스트 계획

- `build_topic_narration_prompt(topic=..., topic_context=None, ...)` 결과가 기존과 동일한
  문자열을 생성하는지 확인 (회귀 없음).
- `build_topic_narration_prompt(topic=..., topic_context="다크 심리학 관점...", ...)` 호출 시
  "# Additional Context / Direction" 섹션이 올바른 위치에 삽입되는지 확인.
- Streamlit 배치 모드에서 새 필드에 값을 입력하고 실제 생성을 1회 수동 실행해, 생성된
  내레이션이 부연 설명의 방향성을 반영하는지 확인.
- 싱글 모드 생성이 기존과 동일하게 동작하는지(회귀) 확인.
