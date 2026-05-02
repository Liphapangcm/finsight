"""
Global theme for FinSight.
Inject CSS once at app startup via apply_theme().
"""

import streamlit as st

# ── Color constants ────────────────────────────────────────────────────────────
COLORS = {
    "primary":    "#0B1F3A",   # deep navy
    "accent":     "#00BFA6",   # teal
    "success":    "#43A047",   # green
    "warning":    "#FB8C00",   # amber
    "danger":     "#E53935",   # red
    "bg":         "#F7F9FC",   # off-white background
    "card":       "#FFFFFF",   # card background
    "text":       "#1A1A2E",   # primary text
    "muted":      "#6B7280",   # secondary text
    "border":     "#E5E7EB",   # card borders
}

SCORE_COLORS = {
    "Poor":      "#E53935",
    "Fair":      "#FB8C00",
    "Good":      "#43A047",
    "Excellent": "#00897B",
}


def apply_theme():
    """Inject global CSS. Call once in main.py."""
    st.markdown(f"""
    <style>
    /* ── Page background ── */
    .stApp {{
        background-color: {COLORS['bg']};
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    /* ── Hide Streamlit default chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}

    /* ── Top navigation bar ── */
    .finsight-nav {{
        background: {COLORS['primary']};
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
    }}
    .finsight-logo {{
        color: {COLORS['accent']};
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}
    .finsight-logo span {{
        color: white;
    }}

    /* ── Cards ── */
    .fs-card {{
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .fs-card-accent {{
        border-left: 4px solid {COLORS['accent']};
    }}

    /* ── Score band badges ── */
    .score-badge {{
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }}
    .badge-poor      {{ background:#FFEBEE; color:#C62828; }}
    .badge-fair      {{ background:#FFF3E0; color:#E65100; }}
    .badge-good      {{ background:#E8F5E9; color:#2E7D32; }}
    .badge-excellent {{ background:#E0F2F1; color:#00695C; }}

    /* ── KPI metric cards ── */
    .kpi-card {{
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {COLORS['primary']};
        line-height: 1.1;
    }}
    .kpi-label {{
        font-size: 0.78rem;
        color: {COLORS['muted']};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.3rem;
    }}
    .kpi-delta {{
        font-size: 0.82rem;
        margin-top: 0.3rem;
        font-weight: 600;
    }}
    .kpi-positive {{ color: {COLORS['success']}; }}
    .kpi-negative {{ color: {COLORS['danger']};  }}
    .kpi-neutral  {{ color: {COLORS['warning']}; }}

    /* ── Recommendation cards ── */
    .rec-card {{
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
    }}
    .rec-priority {{
        display: inline-block;
        background: {COLORS['primary']};
        color: white;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        text-align: center;
        line-height: 26px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.6rem;
    }}
    .rec-title {{
        font-weight: 700;
        font-size: 1rem;
        color: {COLORS['text']};
        display: inline;
    }}
    .rec-category {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.15rem 0.6rem;
        border-radius: 10px;
        margin-left: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .cat-debt      {{ background:#EDE7F6; color:#4527A0; }}
    .cat-savings   {{ background:#E0F7FA; color:#00695C; }}
    .cat-income    {{ background:#E8F5E9; color:#1B5E20; }}
    .cat-behaviour {{ background:#FFF3E0; color:#E65100; }}
    .cat-expenses  {{ background:#FCE4EC; color:#880E4F; }}
    .rec-description {{
        color: {COLORS['muted']};
        font-size: 0.9rem;
        margin-top: 0.6rem;
        line-height: 1.6;
    }}
    .rec-impact {{
        margin-top: 0.6rem;
        font-size: 0.82rem;
        font-weight: 600;
        color: {COLORS['success']};
    }}

    /* ── Progress bar (form steps) ── */
    .progress-container {{
        background: {COLORS['border']};
        border-radius: 6px;
        height: 6px;
        margin-bottom: 2rem;
    }}
    .progress-fill {{
        background: linear-gradient(90deg,
            {COLORS['accent']}, {COLORS['primary']});
        border-radius: 6px;
        height: 6px;
        transition: width 0.4s ease;
    }}
    .step-label {{
        font-size: 0.82rem;
        color: {COLORS['muted']};
        margin-bottom: 0.4rem;
        font-weight: 500;
    }}

    /* ── Form section headers ── */
    .form-section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid {COLORS['accent']};
    }}

    /* ── Trust badge ── */
    .trust-badge {{
        background: #E8F5E9;
        border: 1px solid #A5D6A7;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.82rem;
        color: #2E7D32;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }}

    /* ── Button overrides ── */
    .stButton > button {{
        background: {COLORS['accent']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: opacity 0.2s;
        width: 100%;
    }}
    .stButton > button:hover {{
        opacity: 0.88;
        color: white;
    }}
    .btn-secondary > button {{
        background: transparent !important;
        color: {COLORS['primary']} !important;
        border: 2px solid {COLORS['primary']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def nav_bar():
    """Render the top navigation bar."""
    st.markdown("""
    <div class="finsight-nav">
        <div class="finsight-logo">Fin<span>Sight</span></div>
        <div style="color:#94A3B8; font-size:0.82rem;">
            🔒 Your data is secure and never shared
        </div>
    </div>
    """, unsafe_allow_html=True)