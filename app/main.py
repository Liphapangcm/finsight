import sys
import os

# ── Fix import paths ──────────────────────────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from startup import ensure_model_exists
ensure_model_exists()

import streamlit as st
from app.styles.theme import apply_theme, nav_bar
from app.pages.landing    import render_landing
from app.pages.assessment import render_assessment
from app.pages.results    import render_results
from app.pages.loan_sim   import render_loan_simulator
# ── Page config — must be FIRST streamlit call ────────────────────
st.set_page_config(
    page_title           = "FinSight — Credit Scoring",
    page_icon            = "📊",
    layout               = "wide",
    initial_sidebar_state= "collapsed",
)

# ── Apply global theme ────────────────────────────────────────────
apply_theme()
nav_bar()

# ── Initialise session state ──────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'
if 'form_step' not in st.session_state:
    st.session_state['form_step'] = 1

# ── Router ────────────────────────────────────────────────────────
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