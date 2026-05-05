# tests/conftest.py
"""
Pytest configuration.

Key problem this solves:
When pytest collects tests, it imports all modules in the project.
Some modules (app/main.py, app/pages/*.py, app/components/*.py)
import streamlit and call st.set_page_config() at module level.
Streamlit requires a running server context for this — without it,
any import of these modules crashes with:
    StreamlitAPIException: `set_page_config()` can only be called once

Solution: mock the streamlit module before any test collection
happens, so app/ imports succeed silently without a server.

This conftest.py is loaded by pytest before any test files,
making the mock available for all test collection.

Note: core/, database/, ml/ do NOT import streamlit directly,
so they work fine without mocking. Only app/ needs this.
"""
import sys
from unittest.mock import MagicMock, patch


def _mock_streamlit():
    """
    Replace the streamlit module with a MagicMock.
    Every attribute access (st.markdown, st.columns, etc.)
    returns another MagicMock, which is callable and does nothing.
    This lets app/ modules be imported without a Streamlit server.
    """
    mock_st = MagicMock()

    # set_page_config is called at import time in main.py —
    # it must not raise, just silently succeed
    mock_st.set_page_config = MagicMock(return_value=None)

    # session_state needs dict-like behaviour for some imports
    mock_st.session_state = {}

    # secrets needs .get() for config.py
    mock_st.secrets = MagicMock()
    mock_st.secrets.get = MagicMock(return_value=None)

    sys.modules['streamlit'] = mock_st
    sys.modules['streamlit.components'] = MagicMock()
    sys.modules['streamlit.components.v1'] = MagicMock()


# Install the mock immediately when conftest is loaded —
# before pytest collects any test files
_mock_streamlit()