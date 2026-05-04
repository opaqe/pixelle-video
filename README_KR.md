<h1 align="center">🎬 Pixelle-Video —— AI 전자동 숏폼 비디오 엔진</h1>

<p align="center"><a href="README_EN.md">English</a> | <a href="README.md">中文</a> | <b>한국어</b></p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=uUkx-lRxLjc" target="_blank"><img src="https://img.shields.io/badge/🎥 Video%20Tutorial-EA4C89" alt="Video Tutorial"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/releases" target="_blank"><img src="https://img.shields.io/badge/📦 Windows-50C878" alt="Windows Package"></a>
  <a href="https://aidc-ai.github.io/Pixelle-Video" target="_blank"><img src="https://img.shields.io/badge/📘 Documentation-4A90E2" alt="Documentation"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/stargazers"><img src="https://img.shields.io/github/stars/AIDC-AI/Pixelle-Video.svg" alt="Stargazers"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/issues"><img src="https://img.shields.io/github/issues/AIDC-AI/Pixelle-Video.svg" alt="Issues"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/network/members"><img src="https://img.shields.io/github/forks/AIDC-AI/Pixelle-Video.svg" alt="Forks"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AIDC-AI/Pixelle-Video.svg" alt="License"></a>
</p>

https://github.com/user-attachments/assets/a42e7457-fcc8-40da-83fc-784c45a8b95d

**주제(Topic)**만 입력하시면 Pixelle-Video가 자동으로 다음 작업을 수행합니다:
- ✍️ 비디오 스크립트 작성
- 🎨 AI 이미지/비디오 생성  
- 🗣️ 음성 내레이션 합성
- 🎵 배경 음악 추가
- 🎬 원클릭으로 비디오 합성/제작

**진입 장벽 제로, 영상 편집 경험 불필요** - 문장 하나만 입력하면 될 정도로 비디오 제작을 간단하게!


## 🖥️ 웹 인터페이스 미리보기

![Web UI Interface](resources/webui_en.png)


## 📋 최근 업데이트

- ✅ **2026-01-26**: 모션 트랜스퍼 파이프라인 추가 — 레퍼런스 비디오와 이미지를 업로드하여 모션을 전송합니다.
- ✅ **2026-01-14**: "디지털 휴먼" 및 "이미지 투 비디오" 파이프라인 추가, 다국어 TTS 음성 지원
- ✅ **2026-01-06**: RunningHub 48G VRAM 머신 지원 추가
- ✅ **2025-12-28**: RunningHub 동시성 제한 설정 기능, LLM 구조화 데이터 응답 처리 개선
- ✅ **2025-12-17**: ComfyUI API Key 설정 기능, Nano Banana 모델 지원, API 템플릿 커스텀 파라미터 기능
- ✅ **2025-12-10**: 사이드바에 내장 FAQ 제공, 원활한 오디오 처리를 위해 TTS 서비스 불안정성을 해결하도록 edge-tts 버전 고정
- ✅ **2025-12-08**: 다중 스크립트 분할 모드 (문단/줄/문장 단위), 직접 미리보기를 통한 템플릿 선택 개선
- ✅ **2025-12-06**: 크로스 플랫폼 호환성을 보장하는 기능, 비디오 생성 API URL 경로 처리 수정
- ✅ **2025-12-05**: Windows 올인원 패키지 다운로드 출시, 이미지 및 비디오 분석 워크플로우 최적화
- ✅ **2025-12-04**: 새로운 "사용자 미디어" 탑재 - 자신의 사진/비디오를 업로드하여 AI 기반 분석 및 스크립트 도출 기능
- ✅ **2025-11-18**: RunningHub 병렬 처리, 히스토리 페이지 마련, 비디오 작업 일괄 처리 생성 지원


## ✨ 주요 기능

- ✅ **완전 자동 생성** - 주제 키워드만 입력하면 처음부터 끝까지 완전한 영상을 만들어 냅니다.
- ✅ **AI 스마트 카피라이팅** - 지능적으로 주제를 파악해 내레이션을 전개, 대본을 걱정하지 마세요.
- ✅ **AI 이미지 생성** - 각각의 문장에 어울리는 미려한 AI 일러스트 장면 제공.
- ✅ **AI 비디오 생성** - 역동적 콘텐츠를 뽑기 위해 비디오 생성 모델들(예: WAN 2.1) 지원.
- ✅ **AI 음성 생성** - Edge-TTS, Index-TTS를 비롯한 여러 대중적인 TTS 엔진 제공.
- ✅ **배경 음악 지원 (BGM)** - 영상의 분위기 조성을 위한 다양한 BGM 삽입 옵션.
- ✅ **비주얼 스타일 관리** - 선별된 디자인 템플릿과 고유 비디오 스타일을 제공.
- ✅ **가변 해상도 크기 조정** - 세로(숏폼), 가로, 정사각형 등 원하는 해상도로 바로 추출 가능.
- ✅ **다양한 AI 모델 채택** - GPT, Qwen, DeepSeek, Ollama 등 상황에 따라 도입 가능.
- ✅ **유연한 기능 컴포넌트** - ComfyUI 아키텍처 베이스에 의해 짜여있어 어떤 특성이든 재조합 가능(예시: 이미지 생성을 FLUX로 교체, Voice를 ChatTTS로 교체 등 자유로움 구성 지원).


## 📊 비디오 생성 파이프라인

Pixelle-Video는 모듈식 구조를 이용해 비디오 변환 처리 전 과정이 심플하게 연결됩니다:

![Video Generation Flow](resources/flow_en.png)

텍스트 한 줄만 던져도 알아서 단계별 작업을 처리합니다: **스크립트 생성 → 이미지 기획 → 프레임별 처리 → 비디오 최종 합성**

각 단계는 사용자가 원할 때 언제든 세밀하게 조정할 수 있도록 커스터마이징을 지원하며, 필요한 AI를 골라서 입맛에 맞게 대체 투입할 수 있습니다.


## 🎬 비디오 예시

다음은 다양한 주제와 스타일로 만들어 본 실제 Pixelle-Video 활용 사례입니다:

### 📱 확장 기능형 비디오

<table>
<tr>
<td width="33%">
<h3>👤 AI 디지털 아바타</h3>
<video src="https://github.com/user-attachments/assets/7c122563-c2e0-4dcd-a73c-25ba1d4fa2dd" controls width="100%"></video>
<p align="center"><b>한국어로 설명하는 AI 아바타</b></p>
</td>
<td width="33%">
<h3>🖼️ 이미지 투 비디오</h3>
<video src="https://github.com/user-attachments/assets/5b4eef17-07d0-4bde-9748-2ed68cc9888e" controls width="100%"></video>
<p align="center"><b>애니메이션/카툰 비디오</b></p>
</td>
<td width="33%">
<h3>💃 모션 트랜스퍼</h3>
<video src="https://github.com/user-attachments/assets/7b1240bc-e965-434c-b343-118ec4793d4f" controls width="100%"></video>
<p align="center"><b>춤추는 새끼 고양이</b></p>
</td>
</tr>
</table>

### 📱 세로형(숏폼) 비디오 

<table>
<tr>
<td width="33%">
<h3>🌄 다큐멘터리 & 라이프스타일 – 기본 템플릿</h3>
<video src="https://github.com/user-attachments/assets/e6716c1d-78de-453d-84c2-10873c8c595f" controls width="100%"></video>
<p align="center"><b>여행을 통한 아름다운 풍경들</b></p>
</td>
<td width="33%">
<h3>🔍 문화 해몽 – 기본 템플릿</h3>
<video src="https://github.com/user-attachments/assets/f5de75f6-135a-4ab4-9f5f-079f649764d5" controls width="100%"></video>
<p align="center"><b>산타 할아버지의 주민등록증</b></p>
</td>
<td width="33%">
<h3>🔭 지식 탐구 – 기본 템플릿</h3>
<video src="https://github.com/user-attachments/assets/ceb8b0df-8331-4e1f-88e7-db5b295a1c1d" controls width="100%"></video>
<p align="center"><b>우리는 왜 외계인을 발견하지 못했을까?</b></p>
</td>
</tr>
<tr>
<td width="33%">
<h3>🌱 자기 계발 – 클론 보이스</h3>
<video src="https://github.com/user-attachments/assets/1bad9a49-df83-4905-9cc8-9a7640e9c7d8" controls width="100%"></video>
<p align="center"><b>레벨업하는 가장 현실적인 방법</b></p>
</td>
<td width="33%">
<h3>🧠 철학 – 기본 템플릿</h3>
<video src="https://github.com/user-attachments/assets/663b705a-2aea-44bc-b266-4bb27aa255a8" controls width="100%"></video>
<p align="center"><b>안티프래질(Antifragility)이란 무엇인가</b></p>
</td>
<td width="33%">
<h3>🏯 역사 & 국조 – 정적 프레임</h3>
<video src="https://github.com/user-attachments/assets/56e0a018-fa99-47eb-a97f-fc2fa8915724" controls width="100%"></video>
<p align="center"><b>자치통감 요약 해설</b></p>
</td>
</tr>
<tr>
<td width="33%">
<h3>☀️ 감성 에세이 – 클론 보이스</h3>
<video src="https://github.com/user-attachments/assets/4687df95-dd21-4a7b-b01e-f33a7b646644" controls width="100%"></video>
<p align="center"><b>한겨울 빛나는 햇살</b></p>
</td>
<td width="33%">
<h3>📜 소설 각색/리뷰 – 커스텀 스크립트</h3>
<video src="https://github.com/user-attachments/assets/d354465e-3fa8-40b4-93e9-61ad75ef0697" controls width="100%"></video>
<p align="center"><b>만화 투파창궁</b></p>
</td>
<td width="33%">
<h3>🧬 상식 정보 전달 – Qwen 이미지 생성</h3>
<video src="https://github.com/user-attachments/assets/8ac21768-41ce-4d41-acdd-e3dd3eb9725a" controls width="100%"></video>
<p align="center"><b>알아두면 쓸모있는 웰니스 건강 꿀팁</b></p>
</td>
</tr>
</table>

### 🖥️ 가로형 비디오 (장편/정보성)

<table>
<tr>
<td width="50%">
<h3>💰 부업/경제 유튜브 스타일 - 무비 템플릿</h3>
<video src="https://github.com/user-attachments/assets/c9209d4e-73a6-4b82-aaad-cf102248c9e2" controls width="100%"></video>
<p align="center"><b>수익을 내는 부업의 진실</b></p>
</td>
<td width="50%">
<h3>🏛️ 인문/사회 해설 - 사용자 지정 템플릿</h3>
<video src="https://github.com/user-attachments/assets/a767c452-d5f1-4cff-bb34-b80fff0d4c3e" controls width="100%"></video>
<p align="center"><b>자치통감에서 배우는 인사이트</b></p>
</td>
</tr>
</table>

> 💡 **팁**: 이 예시들은 어떤 과정도 거치지 않고 순수하게 "주제어 타이핑"만으로 출력한 결과물이라는 사실을 기억해 주세요. 어떤 프로그램도 열어볼 필요가 없습니다!

<div id="tutorial-start" />

## 🚀 빠른 시작 가이드

### 🪟 Windows 올인원 패키지 (권장 - 이 버전이 가장 빠르고 확실합니다)

**파이썬 환경, ffmpeg, uv 등 번거로운 명령어 설치 및 환경 설정 과정이 일절 없습니다. 클릭 한 번으로 실행하세요!**

👉 **[Windows 올인원 원클릭 실행 툴 설치 (Releases 이동)](https://github.com/AIDC-AI/Pixelle-Video/releases/latest)**

1. 최신 배포 탭(Releases)에서 통합 패키지를 받고 압축을 해제합니다.
2. `start.bat`을 더블클릭합니다.
3. 브라우저가 자동으로 웹 인터페이스로 이동합니다. (http://localhost:8501)
4. "⚙️ System Configuration (시스템 설정)"에서 원하시는 API 키를 살짝만 적어줍니다.
5. 이제 🎬 비디오를 만드시면 됩니다!

> 💡 **팁**: 처음 쓸 때 여러분은 API 키 설정 딱 하나만 하시면 됩니다.

### 개발자용 수동 구축 (macOS / Linux, 혹은 개조를 원하는 심화 유저)

#### 필수 조건 확인

시작하기 전 차세대 파이썬 패키징 매니저인 `uv` 와 비디오 컴포지션을 위한 `ffmpeg` 설치가 요구됩니다:

##### 1. uv 설치

운영체제별 명령어는 공식 페이지에서 확인을 권장합니다:  
👉 **[uv 설치 매뉴얼로 이동](https://docs.astral.sh/uv/getting-started/installation/)**

설치 후 터미널에 `uv --version`을 쳐서 버전명이 나오면 정상입니다.

##### 2. ffmpeg 탑재

**macOS**
```bash
brew install ffmpeg
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**
- 공식 사이트: https://ffmpeg.org/download.html
- zip 파일 경로 다운로드 후 압축을 풀고 안의 `bin` 폴더를 시스템 환경 변수에 꼭 추가 바랍니다.

설치 후 터미널에서 `ffmpeg -version`을 쳤을 때 오류가 안 뜨면 정상입니다.


#### 개발 환경 세팅 과정

**Step 1: 깃허브에서 프로젝트 당겨오기**

```bash
git clone https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

**Step 2: 웹 인터페이스 빌드 시작**

```bash
# uv를 통해 구동하면 종속성이 자동으로 매니징됩니다
uv run streamlit run web/app.py
```

명령어를 치면 브라우저가 자동 연결됩니다 http://localhost:8501

**Step 3: 웹으로 넘어가서 정보 입력**

페이지가 보이면 "⚙️ 시스템 구성 (System Configuration)" 탭으로 갑니다:
- **LLM Configuration (언어 분석 엔진)**: GPT, Qwen 등의 서비스의 API 서버 및 키 입력
- **Image Configuration (시각 이미지 엔진)**: 이미지 결과물 렌더링을 위해 사용하는 ComfyUI 또는 RunningHub 정보 입력

키 입력을 마치고 "Save Configuration(저장)" 버튼을 누르면 정상 작동합니다!

<div id="tutorial-end" />

## 💻 사용 설명서

앱을 실행하고 나면, 3단 구조인 레이아웃으로 이루어져 있습니다. 다음은 각 기능에 대한 세부 조작법입니다:


### ⚙️ 시스템 설정 필수 입력 창 (초기 1회)

처음 사용할 때는 설정이 1회 요구됩니다. "⚙️ 시스템 설정" 패널을 열어주세요:

#### 1. LLM 설정 (대규모 문장 모델)
영상의 줄거리, 대본, 내레이션을 짜주는 브레인입니다.

**기본 프리셋 선택**  
- 드롭다운 버튼을 눌러 Qwen, GPT-4o, DeepSeek 등을 적당히 고릅니다.
- base_url, model 옵션값은 최적화되어 자동 채워집니다.
- 키가 없다면 옆에 있는 "🔑 API 키 발급받기" 링크로 가서 키를 취득합니다.

**수동 설정**  
- API Key: 본인의 API 키 지정
- Base URL: API 엔드포인트 URL 지정
- Model: 원하는 모델명 입력

#### 2. 이미지 설정
이미지 및 애니메이션 효과를 부여하기 위한 설정입니다.

**로컬 기반 설정 (권장)**  
- ComfyUI URL: 컴퓨터 내부에서 실행되고 있는 ComfyUI 주소값 (보통 http://127.0.0.1:8188)
- "Test Connection"을 쳐보면 통신 불량 여부를 즉각 판단해 줍니다.

**클라우드 기반 설정**  
- RunningHub API Key: PC 사양과 무관하게 웹상의 클라우드를 통한 그림 생성 서비스

설정 후 "설정 저장"을 클릭하세요.


### 📝 기획 및 내용 (왼쪽 영역)

#### 영상 제작 모드 (Generation Mode)
- **AI 생성 콘텐츠**: 주제나 키워드만 던지면 AI가 스토리라인을 짜고 대본을 뱉습니다. 
  - (예시 적용: "독서의 필요성과 습관 들이기")
- **고정 스크립트 모드**: 대본을 직접 적는 사람을 위한 기능. 사용자가 입력한 대사가 그대로 출력됩니다. 

#### BGM 믹싱
- **No BGM**: 무음, 음성 효과만 출력
- **Built-in Music**: 미리 포함되어 있는 기본 음악 효과 활용
- **Custom Music (커스텀)**: 내가 올린 mp3 등을 `bgm/` 폴더에 넣고 경로를 긁어오면 영상에 오디오로 박힙니다.


### 🎤 더빙, 음성 모델 설정 (가운데 영역 上)

#### TTS 옵션 (텍스트-성우 변환)
- Edge-TTS 나 Index-TTS 등 자신이 원하는 스타일의 음성 합성 기능을 선택합니다.
- 자신이 직접 개조한 ComfyUI 기반 TTS 워크플로우를 자유롭게 넣을 수도 있습니다 (`workflows/` 폴더 스캔형).

#### 레퍼런스 오디오 (옵션)
- 내 목소리, 남의 목소리 등을 복제 (Voice Cloning) 하고 싶을 때 참고 오디오를 하나 업로드 합니다 (mp3/wav/flac 등).
- 이 파일과 함께 작동하는 기능은 특정 TTS 워크플로우만 국한될 수 있습니다.

#### 미리 들려주기 모드
- 짧게 입력된 테스트용 문장을 미리 "미리보기(Preview Voice)" 버튼으로 체험 가능.


### 🎨 무대, 스타일 및 템플릿 설정 (가운데 영역 下)

#### 이미지 출력 기능
최종 비디오에 얹어질 시각적 무드를 체크합니다.

**ComfyUI 워크플로우**  
- 로컬 또는 원격으로 원하는 스타일(flux 등)의 이미지 출력 프로세스를 적용
- `image_flux.json` 이 기본 추천 메커니즘입니다.

**화면 비율 (해상도)**  
- 일반적인 숏폼/장편 유튜브 가로세로 규격부터 1024x1024 1:1 종횡비 변경까지 선택적으로 폭/높이 지정 

**프롬프트 조정**  
- 분위기를 구체적으로 한정해 줄 영문 문장
- 팁 예시: Minimalist black-and-white matchstick figure style illustration, clean lines, simple sketch style

#### 비디오 레이아웃
단순한 사진 슬라이드쇼가 아닌 영상 배치를 결정합니다.

**템플릿 규칙**  
- `static_*.html`: 글자와 테마 느낌만 있는 정적인 영상 (시각 자료 안 넣는 텍스트 위주) 
- `image_*.html`: AI가 렌더링한 이미지 기반 스토리라인 영상
- `video_*.html`: AI가 젠(Gene) 해낸 움직이는 영상 요소들

**이용 팁**
- 해상도 규격 (가로/세로/정사각형)별로 매칭되는 템플릿을 고르세요
- HTML 지식이 있으면 `templates/` 폴더에서 스스로 템플릿을 개발해 쓸 수 있습니다.
- 🔗 (미리보기) [전체 템플릿 캡처 이미지 보기](https://aidc-ai.github.io/Pixelle-Video/user-guide/templates/#built-in-template-preview)


### 🎬 최종 렌더링 (오른쪽 영역)

#### 비디오 출력 버튼
- 모든 항목을 세팅하셨다면 "🎬 Generate Video"를 클릭하세요. 
- 이 버튼을 누르시면 이제 아무것도 할 것 없이 기다리기만 하면 됩니다!

#### 진행 정보 요약
- 이 화면이 멈춘 것인지 작동하는 중인지 알려줍니다 (예시: 과정 3/5 대본 번역 완료-이미지 작업 중). 

#### 완성 영상 송출
- 완료되면 비디오가 화면에 바로 뜹니다.
- 플레이어 밑에 실제 사용된 파일 크기와 플레이타임이 기재되어 있습니다. 영상 원본은 `output/` 폴더 내에 저장됩니다.


### ❓ 기타 자주 하시는 질문 사항 (FAQ)

**Q: 영상을 뽑아내는 데 걸리는 시간은요?**  
A: 총 길이 3~4문장이면 통상적으로 1분도 안 되어 나옵니다만, 인터넷이나 컴퓨터 통신 속도에 약간의 영향을 받습니다. 

**Q: 결과물이 맘에 들지 않으면 어떻게 바꿀 수 있나요?**  
A: 
1. 대화 시나리오가 아쉽거나 매끄럽지 않다면 LLM을 교체해 보세요.
2. 그림체가 이상하다면 이미지 세팅에서 스타일 지시어 프롬프트를 다듬으세요.
3. 목소리도 당연히 여러 성우 버전으로 들어보며 바꿀 수 있습니다.

**Q: 결론적으로 돈이 얼마나 나가나요?**  
A: **기본적으로 0원에 즐길 수 있습니다.**

- **완전 0원 무제한 사용**: Ollama LLM(로컬 PC AI 구동) + ComfyUI 로컬 PC 렌더링 구동
- **권장 사항 (초가성비 1원대)**: Qwen 기반 언어 모델 (퀄리티가 높고 이용료가 극히 적음) + ComfyUI 로컬 실행
- **클라우드 연동형**: 최고급 모델(OpenAI) + 무설치 그림 생성 (RunningHub 클라우드), API 연결량 과금

**유저 가이드라인**: 본인 그래픽카드가 비교적 최신이면 모두 로컬(내 컴퓨터)로 돌리면 0원입니다. 하지만 언어 쪽을 Qwen으로, 그림만 그래픽카드로 쓰시는 편이 퀄리티가 좋습니다.


## 🤝 연관 오픈 소스 프로젝트

본 프로젝트는 아래 훌륭한 오픈 소스 생태계를 참조했습니다:

- [Pixelle-MCP](https://github.com/AIDC-AI/Pixelle-MCP) - ComfyUI MCP 서버 지원 기반 제공
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - 매우 탁월한 자동 영상 생산기
- [NarratoAI](https://github.com/linyqh/NarratoAI) - 필름 커멘터리 작업화 툴
- [MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus) - 안정적인 비디오 운영 플랫폼
- [ComfyKit](https://github.com/puke3615/ComfyKit) - ComfyUI 래퍼 및 매니저 엔진

위 프로젝트에게 경의와 감사를 보냅니다! 🙏


## 💬 소통 공간 안내

업데이트 소식을 확인하고 질문사항이 있다면 커뮤니티로 들어오세요! 언제나 환영합니다.

| Discord (디스코드 서버) | WeChat (위챗) |
| ---- | ---- |
| <img src="resources/discord.png" alt="Discord Community" width="250" /> | <img src="resources/wechat.png" alt="WeChat Group" width="250" /> |


## 📢 건의사항 및 기여하기

- 🐛 **버그 리포팅**: 기능 문제 발견 시 [Issue](https://github.com/AIDC-AI/Pixelle-Video/issues) 로 오세요.
- 💡 **기능 제안**: 새로운 방향성에 관한 아이디어는 [Feature Request](https://github.com/AIDC-AI/Pixelle-Video/issues) 에 남겨주세요.
- ⭐ **별 남기기**: 오픈 소스 개발자들에게 깃허브 스타(Star) 1점은 커다란 활력이 됩니다. 이 프로젝트가 만족스럽다면 꼭 별을 남겨주세요!


## 📝 저작권 표기

이 프로젝트는 Apache License 2.0 으로 허가되어 자유롭게 쓸 수 있습니다. 자세한 권리 문구는 [LICENSE](LICENSE) 에서 규정합니다.


## ⭐ 통계

[![Star History Chart](https://api.star-history.com/svg?repos=AIDC-AI/Pixelle-Video&type=Date)](https://star-history.com/#AIDC-AI/Pixelle-Video&Date)
