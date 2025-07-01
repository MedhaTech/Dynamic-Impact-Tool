import traceback
import streamlit as st

def safe_llm_call(fn, *args, default=None, show_error=True, **kwargs):
    """
    Wrap any LLM call safely and catch all exceptions.
    """
    try:
        result = fn(*args, **kwargs)
        if result is None:
            raise ValueError("Received None from LLM.")
        return result
    except Exception as e:
        if show_error:
            st.error(f"LLM Error: {e}")
            st.expander("See details").write(traceback.format_exc())
        return default
