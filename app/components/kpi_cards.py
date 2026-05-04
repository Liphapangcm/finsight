# app/main.py
"""
FinSight — Main entry point.
Fixes:
- Sidebar pages giving blank white screen
- SessionInfo warning before page loads
- White reload flashes (use st.session_state guards)
- Loan simulator button returning to home
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── Page config MUST be the very first Streamlit call ─────────────
import streamlit as st

st.set_page_config(
    page_title           = "FinSight — Credit Scoring",
    page_icon            = "📊",
    layout               = "wide",
    initial_sidebar_state= "collapsed",   # keep sidebar collapsed
)

# ── NOW run startup (after set_page_config, before other imports) ──
from startup import ensure_model_exists
ensure_model_exists()

# ── Remaining imports ──────────────────────────────────────────────
from app.styles.theme     import apply_theme, nav_bar
from app.pages.landing    import render_landing
from app.pages.assessment import render_assessment
from app.pages.results    import render_results
from app.pages.loan_sim   import render_loan_simulator
from app.pages.advisor    import render_advisor

# ── Apply theme ────────────────────────────────────────────────────
apply_theme()

# ── Initialise session state defaults (prevent white flash) ────────
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'
if 'form_step' not in st.session_state:
    st.session_state['form_step'] = 1

# ── Nav bar (passes score if available) ───────────────────────────
result = st.session_state.get('result')
if result:
    nav_bar(
        active_page = st.session_state['page'],
        score       = result.credit_score,
        band        = result.score_band,
    )
else:
    nav_bar(active_page=st.session_state['page'])

# ── Router ─────────────────────────────────────────────────────────
page = st.session_state['page']

if page == 'landing':
    render_landing()
elif page == 'assessment':
    render_assessment()
elif page == 'results':
    render_results()
elif page == 'loan_simulator':
    render_loan_simulator()
elif page == 'advisor':
    render_advisor()
else:
    st.session_state['page'] = 'landing'
    st.rerun()