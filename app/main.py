"""
FinSight — Streamlit entry point.
Run with: streamlit run app/main.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Run startup checks (trains model if missing)
from startup import ensure_model_exists
ensure_model_exists()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.styles.theme import apply_theme, nav_bar
from app.pages.landing    import render_landing
from app.pages.assessment import render_assessment
from app.pages.results    import render_results

# ── Page config — must be first Streamlit call ────────────────────────────────
st.set_page_config(
    page_title      = "FinSight — Credit Scoring",
    page_icon       = "📊",
    layout          = "wide",
    initial_sidebar_state = "collapsed",
)

# ── Apply global theme ────────────────────────────────────────────────────────
apply_theme()
nav_bar()

# ── Initialise session state ──────────────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'
if 'form_step' not in st.session_state:
    st.session_state['form_step'] = 1

# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state['page']

if page == 'landing':
    render_landing()
elif page == 'assessment':
    render_assessment()
elif page == 'results':
    render_results()
else:
    st.session_state['page'] = 'landing'
    st.rerun()