# app/styles/theme.py
"""
FinSight Premium Theme — Dark Luxury Fintech
Deep space navy + gold/teal accent system
Glassmorphism cards, animated reveals, screenshot-worthy results
"""

import streamlit as st

COLORS = {
    "bg_primary":    "#070B14",
    "bg_secondary":  "#0D1526",
    "bg_card":       "#111827",
    "bg_glass":      "rgba(255,255,255,0.04)",
    "border_glass":  "rgba(255,255,255,0.08)",
    "border_accent": "rgba(0,212,170,0.3)",
    "primary":       "#00D4AA",
    "primary_dark":  "#00A882",
    "gold":          "#F5C842",
    "gold_light":    "#FFE08A",
    "text_primary":  "#F0F4FF",
    "text_secondary":"#8B9CC8",
    "text_muted":    "#4A5578",
    "success":       "#10D98A",
    "warning":       "#F5A623",
    "danger":        "#FF4D6A",
    "excellent":     "#00D4AA",
    "good":          "#10D98A",
    "fair":          "#F5A623",
    "poor":          "#FF4D6A",
}

SCORE_COLORS = {
    "Poor":      "#FF4D6A",
    "Fair":      "#F5A623",
    "Good":      "#10D98A",
    "Excellent": "#00D4AA",
}

SCORE_GRADIENTS = {
    "Poor":      "linear-gradient(135deg, #FF4D6A, #C0392B)",
    "Fair":      "linear-gradient(135deg, #F5A623, #E67E22)",
    "Good":      "linear-gradient(135deg, #10D98A, #059669)",
    "Excellent": "linear-gradient(135deg, #00D4AA, #0891B2)",
}


def apply_theme():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Reset & Base ── */
    .stApp {{
        background: {COLORS['bg_primary']};
        font-family: 'Space Grotesk', sans-serif;
        color: {COLORS['text_primary']};
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse 80% 50% at 20% -10%,
                rgba(0,212,170,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%,
                rgba(245,200,66,0.08) 0%, transparent 55%),
            radial-gradient(ellipse 40% 60% at 50% 50%,
                rgba(13,21,38,0.9) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }}

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
    section[data-testid="stSidebar"] {{ display: none; }}

    /* ── Main content on top of bg ── */
    .main .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 0 !important;
        max-width: 1100px;
    }}

    /* ── Navigation ── */
    .fs-nav {{
        background: rgba(7,11,20,0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid {COLORS['border_glass']};
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -4rem -4rem 2.5rem -4rem;
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    .fs-logo {{
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['gold']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .fs-nav-badge {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}
    .fs-nav-badge::before {{
        content: '';
        width: 6px; height: 6px;
        border-radius: 50%;
        background: {COLORS['success']};
        box-shadow: 0 0 6px {COLORS['success']};
        animation: pulse-dot 2s infinite;
    }}
    @keyframes pulse-dot {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.6; transform: scale(0.8); }}
    }}

    /* ── Glass Cards ── */
    .fs-card {{
        background: {COLORS['bg_glass']};
        border: 1px solid {COLORS['border_glass']};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: border-color 0.2s, transform 0.2s;
    }}
    .fs-card:hover {{
        border-color: rgba(0,212,170,0.15);
    }}
    .fs-card-accent {{
        border-left: 3px solid {COLORS['primary']};
        background: linear-gradient(135deg,
            rgba(0,212,170,0.05) 0%,
            rgba(0,0,0,0) 100%);
    }}

    /* ── Score Reveal Card (the shareable one) ── */
    .score-reveal-card {{
        background: linear-gradient(145deg,
            #0D1526 0%,
            #111827 50%,
            #0A1020 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin: 0 auto;
        max-width: 480px;
    }}
    .score-reveal-card::before {{
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            from 0deg at 50% 50%,
            transparent 0deg,
            rgba(0,212,170,0.03) 60deg,
            transparent 120deg,
            rgba(245,200,66,0.02) 180deg,
            transparent 240deg,
            rgba(0,212,170,0.03) 300deg,
            transparent 360deg
        );
        animation: rotate-bg 20s linear infinite;
        pointer-events: none;
    }}
    @keyframes rotate-bg {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    /* ── Score Number ── */
    .score-number {{
        font-family: 'Syne', sans-serif;
        font-size: 6rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -4px;
        margin: 0.5rem 0;
        animation: count-up 1.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    @keyframes count-up {{
        from {{ opacity: 0; transform: scale(0.5) translateY(20px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .score-label {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: {COLORS['text_muted']};
        margin-bottom: 0.3rem;
    }}
    .score-band-pill {{
        display: inline-block;
        padding: 0.4rem 1.4rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 0.8rem 0;
        position: relative;
        z-index: 1;
    }}

    /* ── Score Bar ── */
    .score-bar-container {{
        margin: 1.2rem auto;
        max-width: 320px;
        position: relative;
    }}
    .score-bar-track {{
        height: 6px;
        border-radius: 100px;
        background: linear-gradient(90deg,
            #FF4D6A 0%,
            #F5A623 30%,
            #10D98A 60%,
            #00D4AA 100%);
        position: relative;
        overflow: visible;
    }}
    .score-bar-marker {{
        position: absolute;
        top: 50%;
        width: 14px; height: 14px;
        border-radius: 50%;
        background: white;
        border: 2px solid currentColor;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 12px currentColor;
        transition: left 1.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .score-bar-labels {{
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
        font-size: 0.68rem;
        color: {COLORS['text_muted']};
        font-family: 'JetBrains Mono', monospace;
    }}

    /* ── KPI Cards ── */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
    }}
    .kpi-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.1rem 1rem;
        text-align: center;
        transition: all 0.2s;
        animation: fade-up 0.5s ease both;
    }}
    .kpi-card:hover {{
        border-color: rgba(0,212,170,0.2);
        background: rgba(0,212,170,0.04);
        transform: translateY(-2px);
    }}
    @keyframes fade-up {{
        from {{ opacity: 0; transform: translateY(16px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .kpi-value {{
        font-family: 'Syne', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        color: {COLORS['text_primary']};
        line-height: 1.1;
        letter-spacing: -1px;
    }}
    .kpi-label {{
        font-size: 0.7rem;
        color: {COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 0.25rem;
        font-weight: 500;
    }}
    .kpi-delta {{
        font-size: 0.75rem;
        margin-top: 0.3rem;
        font-weight: 600;
        padding: 0.15rem 0.5rem;
        border-radius: 100px;
        display: inline-block;
    }}
    .delta-good {{
        background: rgba(16,217,138,0.1);
        color: {COLORS['success']};
    }}
    .delta-warn {{
        background: rgba(245,166,35,0.1);
        color: {COLORS['warning']};
    }}
    .delta-bad {{
        background: rgba(255,77,106,0.1);
        color: {COLORS['danger']};
    }}
    .delta-neutral {{
        background: rgba(139,156,200,0.1);
        color: {COLORS['text_secondary']};
    }}

    /* ── Section Headers ── */
    .section-header {{
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .section-header::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg,
            {COLORS['border_glass']}, transparent);
    }}

    /* ── Recommendation Cards ── */
    .rec-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s;
        animation: slide-in 0.4s ease both;
    }}
    .rec-card:hover {{
        background: rgba(255,255,255,0.04);
        border-color: rgba(0,212,170,0.2);
        transform: translateX(4px);
    }}
    @keyframes slide-in {{
        from {{ opacity: 0; transform: translateX(-16px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    .rec-number {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px; height: 22px;
        border-radius: 50%;
        background: linear-gradient(135deg,
            {COLORS['primary']}, {COLORS['primary_dark']});
        font-size: 0.7rem;
        font-weight: 700;
        color: {COLORS['bg_primary']};
        margin-right: 0.5rem;
        flex-shrink: 0;
    }}
    .rec-title {{
        font-weight: 600;
        font-size: 0.9rem;
        color: {COLORS['text_primary']};
        display: inline;
    }}
    .rec-category {{
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 100px;
        margin-left: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        vertical-align: middle;
    }}
    .rec-desc {{
        font-size: 0.82rem;
        color: {COLORS['text_secondary']};
        line-height: 1.6;
        margin-top: 0.5rem;
    }}
    .rec-impact {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }}
    .rec-impact::before {{
        content: '↑';
        font-size: 0.8rem;
    }}

    /* ── Category color pills ── */
    .cat-debt      {{ background:rgba(139,92,246,0.15); color:#A78BFA; }}
    .cat-savings   {{ background:rgba(0,212,170,0.12); color:{COLORS['primary']}; }}
    .cat-income    {{ background:rgba(16,217,138,0.12); color:{COLORS['success']}; }}
    .cat-behaviour {{ background:rgba(245,166,35,0.12); color:{COLORS['warning']}; }}
    .cat-expenses  {{ background:rgba(255,77,106,0.12); color:{COLORS['danger']}; }}

    /* ── Progress Bar (form) ── */
    .step-indicator {{
        display: flex;
        gap: 0.4rem;
        margin-bottom: 1.5rem;
    }}
    .step-dot {{
        height: 3px;
        border-radius: 100px;
        flex: 1;
        background: rgba(255,255,255,0.1);
        transition: background 0.3s;
    }}
    .step-dot.active {{
        background: linear-gradient(90deg,
            {COLORS['primary']}, {COLORS['gold']});
    }}
    .step-text {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
        margin-bottom: 0.5rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }}

    /* ── Form Labels ── */
    .stNumberInput label,
    .stSelectbox label,
    .stSlider label,
    .stRadio label {{
        color: {COLORS['text_secondary']} !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}

    /* ── Form Inputs ── */
    .stTextInput input,
    .stNumberInput input {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: {COLORS['text_primary']} !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    .stTextInput input:focus,
    .stNumberInput input:focus {{
        border-color: rgba(0,212,170,0.4) !important;
        box-shadow: 0 0 0 3px rgba(0,212,170,0.08) !important;
    }}

    /* ── Selectbox ── */
    .stSelectbox > div > div {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: linear-gradient(135deg,
            {COLORS['primary']}, {COLORS['primary_dark']}) !important;
        color: {COLORS['bg_primary']} !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,212,170,0.3) !important;
        opacity: 0.95 !important;
    }}
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    .btn-ghost > button {{
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: {COLORS['text_secondary']} !important;
        box-shadow: none !important;
    }}
    .btn-ghost > button:hover {{
        border-color: rgba(0,212,170,0.3) !important;
        color: {COLORS['primary']} !important;
        box-shadow: none !important;
    }}
    .btn-gold > button {{
        background: linear-gradient(135deg,
            {COLORS['gold']}, {COLORS['warning']}) !important;
        color: #1A1200 !important;
    }}
    .btn-gold > button:hover {{
        box-shadow: 0 8px 25px rgba(245,200,66,0.3) !important;
    }}

    /* ── Trust badge ── */
    .trust-badge {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16,217,138,0.06);
        border: 1px solid rgba(16,217,138,0.15);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.78rem;
        color: rgba(16,217,138,0.8);
        margin-bottom: 1.5rem;
    }}

    /* ── Narrative box ── */
    .narrative-box {{
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-bottom: 1.2rem;
        border-left: 3px solid;
        font-size: 0.9rem;
        line-height: 1.7;
        animation: fade-up 0.4s ease both;
    }}

    /* ── Form section title ── */
    .form-section {{
        font-family: 'Syne', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: {COLORS['primary']};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0,212,170,0.15);
    }}

    /* ── Live balance tracker ── */
    .balance-tracker {{
        background: linear-gradient(135deg,
            rgba(0,212,170,0.06), rgba(0,0,0,0));
        border: 1px solid rgba(0,212,170,0.12);
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{
        background: {COLORS['bg_primary']}; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(0,212,170,0.2);
        border-radius: 2px; }}

    /* ── Plotly chart bg ── */
    .js-plotly-plot .plotly {{
        background: transparent !important; }}
    .js-plotly-plot .plotly .main-svg {{
        background: transparent !important; }}

    /* ── Stagger animation delays ── */
    .kpi-card:nth-child(1) {{ animation-delay: 0.05s; }}
    .kpi-card:nth-child(2) {{ animation-delay: 0.10s; }}
    .kpi-card:nth-child(3) {{ animation-delay: 0.15s; }}
    .kpi-card:nth-child(4) {{ animation-delay: 0.20s; }}
    .kpi-card:nth-child(5) {{ animation-delay: 0.25s; }}
    .kpi-card:nth-child(6) {{ animation-delay: 0.30s; }}
    .rec-card:nth-child(1) {{ animation-delay: 0.1s; }}
    .rec-card:nth-child(2) {{ animation-delay: 0.2s; }}
    .rec-card:nth-child(3) {{ animation-delay: 0.3s; }}
    .rec-card:nth-child(4) {{ animation-delay: 0.4s; }}
    .rec-card:nth-child(5) {{ animation-delay: 0.5s; }}

    /* ── Loading spinner ── */
    .stSpinner > div {{
        border-color: {COLORS['primary']} transparent transparent !important;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        padding: 3px !important;
        gap: 2px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: {COLORS['text_muted']} !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(0,212,170,0.1) !important;
        color: {COLORS['primary']} !important;
    }}

    /* ── Dataframe ── */
    .stDataFrame {{
        background: rgba(255,255,255,0.02) !important;
        border-radius: 10px !important;
    }}

    /* ── Info/warning boxes ── */
    .stAlert {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: {COLORS['text_secondary']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def nav_bar(show_score: bool = False, score: int = None,
            band: str = None):
    score_html = ""
    if show_score and score:
        color = SCORE_COLORS.get(band, COLORS['primary'])
        score_html = f"""
        <div style="display:flex; align-items:center; gap:0.6rem;">
            <span style="font-size:0.75rem;
                         color:{COLORS['text_muted']};">Your score</span>
            <span style="font-family:'Syne',sans-serif;
                         font-weight:800; font-size:1.1rem;
                         color:{color};">{score}</span>
            <span style="font-size:0.72rem; font-weight:600;
                         color:{color}; background:rgba(0,0,0,0.3);
                         padding:0.15rem 0.5rem;
                         border-radius:100px;">{band}</span>
        </div>
        """

    st.markdown(f"""
    <div class="fs-nav">
        <div class="fs-logo">FinSight</div>
        {score_html if score_html else
         '<div class="fs-nav-badge">Secured · Private · Free</div>'}
    </div>
    """, unsafe_allow_html=True)