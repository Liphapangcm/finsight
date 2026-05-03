"""
FinSight Professional Theme
Aesthetic: Palantir / Stripe / Bloomberg — light, precise, data-focused.
Clean navy header system, white content areas, electric blue accents.
"""
import streamlit as st

COLORS = {
    "navy":           "#0A1F44",
    "navy_mid":       "#112553",
    "navy_light":     "#1A3260",
    "blue":           "#2D7FF9",
    "blue_hover":     "#1A6FE8",
    "blue_light":     "#EBF3FF",
    "blue_mid":       "#DBEAFE",
    "teal":           "#00C2A8",
    "teal_light":     "#E6FAF8",
    "bg":             "#F5F7FA",
    "bg_white":       "#FFFFFF",
    "bg_subtle":      "#F0F2F6",
    "text":           "#1A1A1A",
    "text_secondary": "#4B5563",
    "text_muted":     "#9CA3AF",
    "text_inverse":   "#FFFFFF",
    "border":         "#E5E7EB",
    "border_strong":  "#D1D5DB",
    "success":        "#059669",
    "success_light":  "#ECFDF5",
    "warning":        "#D97706",
    "warning_light":  "#FFFBEB",
    "danger":         "#DC2626",
    "danger_light":   "#FEF2F2",
    "poor":           "#DC2626",
    "fair":           "#D97706",
    "good":           "#059669",
    "excellent":      "#00C2A8",
}

SCORE_COLORS = {
    "Poor":      COLORS["poor"],
    "Fair":      COLORS["fair"],
    "Good":      COLORS["good"],
    "Excellent": COLORS["excellent"],
}


def apply_theme():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    *,*::before,*::after{{box-sizing:border-box;}}

    .stApp{{
        background:{COLORS['bg']};
        font-family:'Plus Jakarta Sans',sans-serif;
        color:{COLORS['text']};
    }}
    #MainMenu,footer,header{{visibility:hidden;}}
    .stDeployButton{{display:none;}}
    section[data-testid="stSidebar"]{{display:none;}}
    .main .block-container{{
        padding-top:0!important;
        max-width:1140px;
        padding-left:2rem;
        padding-right:2rem;
    }}

    /* ── Topbar ── */
    .fs-topbar{{
        background:{COLORS['navy']};
        padding:0 2rem;
        height:54px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin:-4rem -2rem 2rem -2rem;
        position:sticky;
        top:0;
        z-index:999;
        border-bottom:1px solid {COLORS['navy_mid']};
    }}
    .fs-logo{{
        font-weight:800;
        font-size:1.1rem;
        color:white;
        letter-spacing:-0.3px;
        display:flex;
        align-items:center;
        gap:0.5rem;
    }}
    .fs-logo-dot{{
        width:7px;height:7px;
        border-radius:50%;
        background:{COLORS['blue']};
    }}
    .fs-nav-center{{
        display:flex;
        align-items:center;
        gap:2px;
    }}
    .fs-nav-link{{
        font-size:0.8rem;
        font-weight:500;
        color:rgba(255,255,255,0.5);
        padding:0.35rem 0.85rem;
        border-radius:6px;
        cursor:pointer;
        transition:all 0.15s;
        border:none;
        background:none;
    }}
    .fs-nav-link:hover{{color:white;background:rgba(255,255,255,0.07);}}
    .fs-nav-link.active{{
        color:white;
        background:rgba(45,127,249,0.22);
    }}
    .fs-badge{{
        background:{COLORS['blue']};
        color:white;
        font-size:0.65rem;
        font-weight:700;
        padding:0.18rem 0.55rem;
        border-radius:100px;
        letter-spacing:0.4px;
        text-transform:uppercase;
    }}

    /* ── Page header ── */
    .fs-page-header{{
        margin-bottom:1.75rem;
        padding-bottom:1.25rem;
        border-bottom:1px solid {COLORS['border']};
    }}
    .fs-page-title{{
        font-size:1.35rem;
        font-weight:800;
        color:{COLORS['navy']};
        letter-spacing:-0.4px;
        margin-bottom:0.2rem;
    }}
    .fs-page-subtitle{{
        font-size:0.85rem;
        color:{COLORS['text_secondary']};
    }}

    /* ── Cards ── */
    .fs-card{{
        background:{COLORS['bg_white']};
        border:1px solid {COLORS['border']};
        border-radius:10px;
        padding:1.5rem;
        margin-bottom:1rem;
        transition:box-shadow 0.15s;
    }}
    .fs-card:hover{{box-shadow:0 2px 12px rgba(10,31,68,0.07);}}

    /* ── Section label ── */
    .section-label{{
        font-size:0.7rem;
        font-weight:700;
        color:{COLORS['text_muted']};
        text-transform:uppercase;
        letter-spacing:1px;
        margin-bottom:0.75rem;
        display:flex;
        align-items:center;
        gap:0.5rem;
    }}
    .section-label::after{{
        content:'';
        flex:1;
        height:1px;
        background:{COLORS['border']};
    }}

    /* ── Score panel ── */
    .score-panel{{
        background:{COLORS['bg_white']};
        border:1px solid {COLORS['border']};
        border-radius:10px;
        padding:2rem 1.75rem;
        text-align:center;
        position:relative;
        overflow:hidden;
    }}
    .score-panel::before{{
        content:'';
        position:absolute;
        top:0;left:0;right:0;
        height:3px;
        background:linear-gradient(90deg,{COLORS['blue']},{COLORS['teal']});
    }}
    .score-eyebrow{{
        font-size:0.68rem;
        font-weight:700;
        letter-spacing:1.5px;
        text-transform:uppercase;
        color:{COLORS['text_muted']};
        margin-bottom:0.5rem;
    }}
    .score-value{{
        font-family:'JetBrains Mono',monospace;
        font-size:4.2rem;
        font-weight:600;
        letter-spacing:-3px;
        line-height:1;
        margin-bottom:0.25rem;
    }}
    .score-band-pill{{
        display:inline-block;
        padding:0.28rem 0.9rem;
        border-radius:6px;
        font-size:0.75rem;
        font-weight:700;
        letter-spacing:0.5px;
        text-transform:uppercase;
        margin:0.65rem 0;
    }}
    .score-track-wrap{{
        margin:1rem auto 0;
        max-width:260px;
    }}
    .score-track{{
        height:4px;
        border-radius:100px;
        background:linear-gradient(90deg,
            {COLORS['poor']} 0%,
            {COLORS['fair']} 28%,
            {COLORS['good']} 58%,
            {COLORS['excellent']} 100%);
        position:relative;
        margin-bottom:6px;
    }}
    .score-marker{{
        position:absolute;
        top:50%;
        width:11px;height:11px;
        border-radius:50%;
        background:{COLORS['navy']};
        border:2px solid white;
        transform:translate(-50%,-50%);
        box-shadow:0 1px 4px rgba(0,0,0,0.2);
    }}
    .score-track-labels{{
        display:flex;
        justify-content:space-between;
        font-size:0.6rem;
        color:{COLORS['text_muted']};
        font-family:'JetBrains Mono',monospace;
    }}

    /* ── Metric grid ── */
    .metric-grid{{
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:0.9rem;
        margin-bottom:1.5rem;
    }}
    .metric-card{{
        background:{COLORS['bg_white']};
        border:1px solid {COLORS['border']};
        border-radius:10px;
        padding:1.1rem 1.1rem 0.9rem;
        transition:box-shadow 0.15s;
    }}
    .metric-card:hover{{box-shadow:0 2px 10px rgba(10,31,68,0.07);}}
    .metric-label{{
        font-size:0.68rem;
        font-weight:700;
        color:{COLORS['text_muted']};
        text-transform:uppercase;
        letter-spacing:0.8px;
        margin-bottom:0.45rem;
    }}
    .metric-value{{
        font-family:'JetBrains Mono',monospace;
        font-size:1.55rem;
        font-weight:600;
        color:{COLORS['navy']};
        letter-spacing:-0.8px;
        line-height:1;
        margin-bottom:0.45rem;
    }}
    .metric-badge{{
        display:inline-flex;
        align-items:center;
        font-size:0.7rem;
        font-weight:600;
        padding:0.18rem 0.5rem;
        border-radius:5px;
    }}
    .b-good{{background:{COLORS['success_light']};color:{COLORS['success']};}}
    .b-warn{{background:{COLORS['warning_light']};color:{COLORS['warning']};}}
    .b-bad{{background:{COLORS['danger_light']};color:{COLORS['danger']};}}
    .b-info{{background:{COLORS['blue_light']};color:{COLORS['blue']};}}

    /* ── Insight box ── */
    .insight-box{{
        border-radius:8px;
        padding:0.85rem 1rem;
        margin-bottom:1.25rem;
        font-size:0.85rem;
        line-height:1.7;
        border-left:3px solid;
    }}
    .insight-good{{background:{COLORS['success_light']};border-color:{COLORS['success']};color:#065f46;}}
    .insight-warn{{background:{COLORS['warning_light']};border-color:{COLORS['warning']};color:#92400e;}}
    .insight-bad{{background:{COLORS['danger_light']};border-color:{COLORS['danger']};color:#991b1b;}}
    .insight-info{{background:{COLORS['blue_light']};border-color:{COLORS['blue']};color:#1e40af;}}

    /* ── Recommendation items ── */
    .rec-item{{
        background:{COLORS['bg_white']};
        border:1px solid {COLORS['border']};
        border-radius:8px;
        padding:0.9rem 1rem;
        margin-bottom:0.55rem;
        transition:all 0.15s;
        display:flex;
        gap:0.8rem;
        align-items:flex-start;
    }}
    .rec-item:hover{{
        border-color:{COLORS['blue']};
        box-shadow:0 0 0 3px {COLORS['blue_light']};
    }}
    .rec-num{{
        width:22px;height:22px;min-width:22px;
        border-radius:6px;
        background:{COLORS['navy']};
        color:white;
        font-size:0.68rem;
        font-weight:700;
        display:flex;
        align-items:center;
        justify-content:center;
        margin-top:1px;
    }}
    .rec-body{{flex:1;}}
    .rec-title-row{{
        font-size:0.85rem;
        font-weight:700;
        color:{COLORS['text']};
        margin-bottom:0.25rem;
        display:flex;
        align-items:center;
        gap:0.45rem;
        flex-wrap:wrap;
    }}
    .rec-tag{{
        font-size:0.6rem;
        font-weight:700;
        padding:0.12rem 0.45rem;
        border-radius:4px;
        text-transform:uppercase;
        letter-spacing:0.4px;
    }}
    .tag-debt{{background:#EDE9FE;color:#5B21B6;}}
    .tag-savings{{background:{COLORS['teal_light']};color:#065f46;}}
    .tag-income{{background:{COLORS['success_light']};color:{COLORS['success']};}}
    .tag-behaviour{{background:{COLORS['warning_light']};color:{COLORS['warning']};}}
    .tag-expenses{{background:{COLORS['danger_light']};color:{COLORS['danger']};}}
    .rec-desc{{
        font-size:0.8rem;
        color:{COLORS['text_secondary']};
        line-height:1.6;
        margin-bottom:0.35rem;
    }}
    .rec-impact{{
        font-size:0.72rem;
        font-weight:600;
        color:{COLORS['teal']};
        display:inline-flex;
        align-items:center;
        gap:3px;
    }}
    .rec-impact::before{{content:'↑';font-weight:700;}}

    /* ── Step indicator ── */
    .step-row{{
        display:flex;
        align-items:center;
        gap:0.4rem;
        margin-bottom:1.5rem;
    }}
    .step-seg{{
        height:3px;
        border-radius:100px;
        flex:1;
        background:{COLORS['border']};
        transition:background 0.25s;
    }}
    .step-seg.done{{background:{COLORS['blue']};}}
    .step-meta{{
        font-size:0.73rem;
        color:{COLORS['text_muted']};
        font-weight:500;
        margin-bottom:0.4rem;
    }}
    .step-meta strong{{color:{COLORS['navy']};}}

    /* ── Form inputs ── */
    .stNumberInput label,.stSelectbox label,
    .stSlider label,.stRadio label,.stTextInput label{{
        font-size:0.8rem!important;
        font-weight:600!important;
        color:{COLORS['text_secondary']}!important;
        font-family:'Plus Jakarta Sans',sans-serif!important;
    }}
    .stTextInput input,.stNumberInput input{{
        background:{COLORS['bg_white']}!important;
        border:1.5px solid {COLORS['border_strong']}!important;
        border-radius:7px!important;
        color:{COLORS['text']}!important;
        font-family:'JetBrains Mono',monospace!important;
        font-size:0.88rem!important;
        transition:border-color 0.15s,box-shadow 0.15s!important;
    }}
    .stTextInput input:focus,.stNumberInput input:focus{{
        border-color:{COLORS['blue']}!important;
        box-shadow:0 0 0 3px rgba(45,127,249,0.1)!important;
    }}
    .stSelectbox>div>div{{
        background:{COLORS['bg_white']}!important;
        border:1.5px solid {COLORS['border_strong']}!important;
        border-radius:7px!important;
        color:{COLORS['text']}!important;
    }}

    /* ── Buttons ── */
    .stButton>button{{
        background:{COLORS['blue']}!important;
        color:white!important;
        border:none!important;
        border-radius:7px!important;
        padding:0.55rem 1.4rem!important;
        font-weight:600!important;
        font-size:0.875rem!important;
        font-family:'Plus Jakarta Sans',sans-serif!important;
        transition:all 0.15s!important;
        width:100%!important;
    }}
    .stButton>button:hover{{
        background:{COLORS['blue_hover']}!important;
        box-shadow:0 4px 12px rgba(45,127,249,0.28)!important;
        transform:translateY(-1px)!important;
    }}
    .stButton>button:active{{transform:translateY(0)!important;box-shadow:none!important;}}
    .btn-secondary>button{{
        background:transparent!important;
        color:{COLORS['text_secondary']}!important;
        border:1.5px solid {COLORS['border_strong']}!important;
        box-shadow:none!important;
    }}
    .btn-secondary>button:hover{{
        border-color:{COLORS['blue']}!important;
        color:{COLORS['blue']}!important;
        background:{COLORS['blue_light']}!important;
        box-shadow:none!important;
        transform:none!important;
    }}
    .btn-teal>button{{
        background:{COLORS['teal']}!important;
        color:white!important;
    }}
    .btn-teal>button:hover{{
        background:#00A892!important;
        box-shadow:0 4px 12px rgba(0,194,168,0.28)!important;
    }}

    /* ── Trust note ── */
    .trust-note{{
        display:flex;
        align-items:center;
        gap:0.5rem;
        font-size:0.77rem;
        color:{COLORS['success']};
        background:{COLORS['success_light']};
        border:1px solid #A7F3D0;
        border-radius:7px;
        padding:0.5rem 0.85rem;
        margin-bottom:1.5rem;
        font-weight:500;
    }}

    /* ── Form section ── */
    .form-section{{
        font-size:0.7rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:1px;
        color:{COLORS['blue']};
        margin:1.25rem 0 0.75rem;
        padding-bottom:0.45rem;
        border-bottom:1px solid {COLORS['blue_mid']};
    }}

    /* ── Balance widget ── */
    .balance-widget{{
        background:{COLORS['bg']};
        border:1px solid {COLORS['border']};
        border-radius:8px;
        padding:0.9rem 1.1rem;
        margin-top:0.9rem;
        display:flex;
        justify-content:space-between;
        align-items:center;
    }}
    .bal-label{{
        font-size:0.66rem;
        font-weight:600;
        text-transform:uppercase;
        letter-spacing:0.8px;
        color:{COLORS['text_muted']};
        margin-bottom:0.2rem;
    }}
    .bal-value{{
        font-family:'JetBrains Mono',monospace;
        font-size:1.15rem;
        font-weight:600;
        color:{COLORS['navy']};
        letter-spacing:-0.5px;
    }}

    /* ── Divider ── */
    .fs-divider{{height:1px;background:{COLORS['border']};margin:1.75rem 0;}}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"]{{
        background:{COLORS['bg']}!important;
        border-radius:8px!important;
        padding:3px!important;
        gap:2px!important;
        border:1px solid {COLORS['border']}!important;
    }}
    .stTabs [data-baseweb="tab"]{{
        background:transparent!important;
        color:{COLORS['text_muted']}!important;
        border-radius:6px!important;
        font-family:'Plus Jakarta Sans',sans-serif!important;
        font-size:0.8rem!important;
        font-weight:600!important;
    }}
    .stTabs [aria-selected="true"]{{
        background:{COLORS['bg_white']}!important;
        color:{COLORS['navy']}!important;
        box-shadow:0 1px 3px rgba(0,0,0,0.08)!important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar{{width:5px;}}
    ::-webkit-scrollbar-track{{background:{COLORS['bg']};}}
    ::-webkit-scrollbar-thumb{{background:{COLORS['border_strong']};border-radius:3px;}}

    /* ── Plotly bg ── */
    .js-plotly-plot .plotly,
    .js-plotly-plot .plotly .main-svg{{background:transparent!important;}}

    /* ── Share tip ── */
    .share-tip{{
        text-align:center;
        font-size:0.77rem;
        color:{COLORS['text_muted']};
        padding:0.7rem;
        border:1px dashed {COLORS['border_strong']};
        border-radius:8px;
        margin-top:1.5rem;
    }}
    .share-tip strong{{color:{COLORS['blue']};}}
    </style>
    """, unsafe_allow_html=True)


def nav_bar(active_page: str = "score",
            score: int = None, band: str = None):
    pages = [
        ("score",    "Credit Score"),
        ("loans",    "Loan Simulator"),
        ("advisor",  "AI Advisor"),
    ]
    links = ""
    for key, label in pages:
        cls = "active" if key == active_page else ""
        links += f'<span class="fs-nav-link {cls}">{label}</span>'

    right_html = ""
    if score and band:
        color = SCORE_COLORS.get(band, COLORS["blue"])
        right_html = f"""
        <div style="display:flex;align-items:center;gap:0.5rem;">
            <span style="font-size:0.68rem;color:rgba(255,255,255,0.4);
                         font-weight:600;letter-spacing:0.8px;">SCORE</span>
            <span style="font-family:'JetBrains Mono',monospace;
                         font-weight:600;font-size:0.98rem;
                         color:{color};">{score}</span>
            <span class="fs-badge">{band}</span>
        </div>"""

    st.markdown(f"""
    <div class="fs-topbar">
        <div class="fs-logo">
            <div class="fs-logo-dot"></div>
            FinSight
        </div>
        <div class="fs-nav-center">{links}</div>
        <div>{right_html}</div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    sub = (f'<div class="fs-page-subtitle">{subtitle}</div>'
           if subtitle else "")
    st.markdown(f"""
    <div class="fs-page-header">
        <div class="fs-page-title">{title}</div>
        {sub}
    </div>
    """, unsafe_allow_html=True)