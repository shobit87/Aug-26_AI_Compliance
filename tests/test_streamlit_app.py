"""Basic import smoke test for the Streamlit app."""

from importlib import reload

import ai_compliance_agent.streamlit_app as streamlit_app


def test_streamlit_module_exposes_main():
    reloaded = reload(streamlit_app)
    assert hasattr(reloaded, "main")
