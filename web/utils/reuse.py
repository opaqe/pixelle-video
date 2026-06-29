"""One-shot "reuse settings" helpers.

When the user clicks "Start new work with this template" in History, we stash the
previous task's settings (everything except the video script) into session state.
The Home-page input components then pre-select their widgets from these values on
the next render. The values are applied once and cleared, so subsequent user edits
are never overridden.
"""

import streamlit as st

_REUSE_KEY = "reuse_params"


def set_reuse_params(params: dict) -> None:
    """Stash settings to reuse on the next Home render (script fields excluded)."""
    st.session_state[_REUSE_KEY] = dict(params or {})


def get_reuse_params() -> dict:
    return st.session_state.get(_REUSE_KEY) or {}


def reuse_active() -> bool:
    return bool(st.session_state.get(_REUSE_KEY))


def clear_reuse_params() -> None:
    st.session_state.pop(_REUSE_KEY, None)


def reuse_index(widget_key: str, value_list, saved_value, fallback: int = 0) -> int:
    """Index of ``saved_value`` within ``value_list`` for a radio/selectbox default.

    When reuse is active and ``saved_value`` is present, the stale widget state is
    dropped so the returned index actually takes effect; otherwise ``fallback`` is
    returned unchanged.
    """
    if reuse_active() and saved_value is not None and saved_value in value_list:
        st.session_state.pop(widget_key, None)
        return value_list.index(saved_value)
    return fallback


def reuse_scalar(widget_key: str, saved_value, fallback):
    """Pre-fill a slider/number/text widget value when reuse is active."""
    if reuse_active() and saved_value is not None:
        st.session_state.pop(widget_key, None)
        return saved_value
    return fallback


def reuse_template_param(param_name: str, default):
    """Default value for a dynamic template-parameter widget (brand, describe, ...),
    honoring the one-shot reuse of a previous task's ``template_params``."""
    params = get_reuse_params()
    template_params = (params.get("template_params") or {}) if params else {}
    if params and param_name in template_params:
        st.session_state.pop(f"video_custom_{param_name}", None)
        return template_params[param_name]
    return default
