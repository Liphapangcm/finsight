"""
FinSight Professional Theme — Enhanced Edition
Features: Dark mode, accessibility, print styles, premium animations
"""

import streamlit as st
from typing import Optional

COLORS = {
    "navy": "#0A1F44",
    "navy_mid": "#112553",
    "navy_light": "#1A3260",
    "blue": "#2D7FF9",
    "blue_hover": "#1A6FE8",
    "blue_light": "#EBF3FF",
    "blue_mid": "#DBEAFE",
    "teal": "#00C2A8",
    "teal_light": "#E6FAF8",
    "bg": "#F5F7FA",
    "bg_white": "#FFFFFF",
    "bg_subtle": "#F0F2F6",
    "text": "#1A1A1A",
    "text_secondary": "#4B5563",
    "text_muted": "#9CA3AF",
    "text_inverse": "#FFFFFF",
    "border": "#E5E7EB",
    "border_strong": "#D1D5DB",
    "success": "#059669",
    "success_light": "#ECFDF5",
    "warning": "#D97706",
    "warning_light": "#FFFBEB",
    "danger": "#DC2626",
    "danger_light": "#FEF2F2",
    "poor": "#DC2626",
    "fair": "#D97706",
    "good": "#059669",
    "excellent": "#00C2A8",
    "primary": "#2D7FF9",
    "accent": "#00C2A8",
}

# Dark mode colors
DARK_COLORS = {
    "bg": "#0F172A",
    "bg_white": "#1E293B",
    "bg_subtle": "#334155",
    "text": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "border": "#334155",
    "border_strong": "#475569",
}

SCORE_COLORS = {
    "Poor": COLORS["poor"],
    "Fair": COLORS["fair"],
    "Good": COLORS["good"],
    "Excellent": COLORS["excellent"],
}


def apply_theme(dark_mode: bool = False):
    """
    Apply the application theme with optional dark mode.
    
    Args:
        dark_mode: Enable dark mode theme
    """
    # Use dark colors if enabled
    colors = {**COLORS, **(DARK_COLORS if dark_mode else {})}
    
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Reduced motion preference support */
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}

    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}

    .stApp{{
        background:{colors["bg"]};
        font-family:'Plus Jakarta Sans',sans-serif;
        color:{colors["text"]};
        transition: background-color 0.3s ease, color 0.3s ease;
    }}
    
    /* Dark mode toggle button */
    .theme-toggle {{
        position: fixed;
        bottom: 1rem;
        right: 1rem;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: {colors["bg_white"]};
        border: 1px solid {colors["border"]};
        color: {colors["text_secondary"]};
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        z-index: 1000;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .theme-toggle:hover {{
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    #MainMenu,footer,header{{visibility:hidden;}}
    .stDeployButton{{display:none;}}
    [data-testid="collapsedControl"]{{display:none!important;}}
    section[data-testid="stSidebar"]{{display:none!important;}}
    .main .block-container{{
        padding-top:0!important;
        max-width:1140px;
        padding-left:1.5rem;
        padding-right:1.5rem;
    }}

    /* ── Focus states for accessibility ── */
    button:focus-visible, 
    [role="button"]:focus-visible,
    input:focus-visible,
    select:focus-visible,
    textarea:focus-visible {{
        outline: 2px solid {colors["blue"]};
        outline-offset: 2px;
    }}

    /* ── Topbar ── */
    .fs-topbar{{
        background:{colors["navy"]};
        padding:0 1.5rem;
        height:54px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin:-4rem -1.5rem 2rem -1.5rem;
        position:sticky;
        top:0;
        z-index:999;
        border-bottom:1px solid {colors["navy_mid"]};
    }}
    .fs-logo{{
        font-weight:800;
        font-size:1.1rem;
        color:white;
        letter-spacing:-0.3px;
        display:flex;
        align-items:center;
        gap:0.45rem;
        text-decoration:none;
    }}
    .fs-logo-dot{{
        width:7px;height:7px;border-radius:50%;
        background:{colors["blue"]};
        flex-shrink:0;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.6; transform: scale(1.2); }}
    }}
    
    .fs-nav-center{{
        display:flex;align-items:center;gap:2px;
    }}
    .fs-nav-link{{
        font-size:0.8rem;font-weight:500;
        color:rgba(255,255,255,0.5);
        padding:0.35rem 0.85rem;border-radius:6px;
        cursor:pointer;transition:all 0.15s;
        border:none;background:none;
        font-family:'Plus Jakarta Sans',sans-serif;
    }}
    .fs-nav-link:hover{{color:white;background:rgba(255,255,255,0.07);transform:translateY(-1px);}}
    .fs-nav-link.active{{
        color:white;background:rgba(45,127,249,0.22);
    }}
    .fs-badge{{
        background:{colors["blue"]};color:white;
        font-size:0.65rem;font-weight:700;
        padding:0.18rem 0.55rem;border-radius:100px;
        letter-spacing:0.4px;text-transform:uppercase;
    }}

    /* ── Page header with shimmer effect ── */
    .fs-page-header{{
        margin-bottom:1.75rem;padding-bottom:1.25rem;
        border-bottom:1px solid {colors["border"]};
        position: relative;
        overflow: hidden;
    }}
    .fs-page-header::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, {colors["blue"]}, transparent);
        animation: shimmer 3s infinite;
    }}
    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    .fs-page-title{{
        font-size:1.35rem;font-weight:800;
        color:{colors["navy"]};letter-spacing:-0.4px;margin-bottom:0.2rem;
        background: linear-gradient(135deg, {colors["navy"]}, {colors["blue"]});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .fs-page-subtitle{{font-size:0.85rem;color:{colors["text_secondary"]};}}

    /* ── Loading spinner animation ── */
    .loading-spinner {{
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid {colors["border"]};
        border-top-color: {colors["blue"]};
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }}
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    
    /* ── Toast notifications ── */
    .toast {{
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: {colors["bg_white"]};
        border-left: 4px solid {colors["success"]};
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease, fadeOut 0.3s ease 2.7s forwards;
        max-width: 320px;
    }}
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    @keyframes fadeOut {{
        to {{ opacity: 0; visibility: hidden; }}
    }}
    .toast.success {{ border-left-color: {colors["success"]}; }}
    .toast.error {{ border-left-color: {colors["danger"]}; }}
    .toast.warning {{ border-left-color: {colors["warning"]}; }}
    .toast.info {{ border-left-color: {colors["blue"]}; }}
    
    /* ── Cards with improved hover ── */
    .fs-card{{
        background:{colors["bg_white"]};
        border:1px solid {colors["border"]};
        border-radius:10px;padding:1.5rem;margin-bottom:1rem;
        transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .fs-card:hover{{
        box-shadow:0 8px 24px rgba(10,31,68,0.12);
        transform:translateY(-4px);
    }}
    .fs-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {colors["blue"]}, {colors["teal"]});
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }}
    .fs-card:hover::before {{
        transform: scaleX(1);
    }}

    /* ── Section label ── */
    .section-label{{
        font-size:0.7rem;font-weight:700;color:{colors["text_muted"]};
        text-transform:uppercase;letter-spacing:1px;
        margin-bottom:0.75rem;display:flex;align-items:center;gap:0.5rem;
    }}
    .section-label::after{{
        content:'';flex:1;height:1px;background:{colors["border"]};
    }}

    /* ── Score panel with glass morphism ── */
    .score-panel{{
        background: {colors["bg_white"]};
        backdrop-filter: blur(10px);
        border:1px solid {colors["border"]};
        border-radius:16px;padding:2rem 1.75rem;
        text-align:center;position:relative;overflow:hidden;
        animation:panel-appear 0.5s ease both;
        transition: all 0.3s ease;
    }}
    .score-panel:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.1);
    }}
    @keyframes panel-appear{{
        from{{opacity:0;transform:translateY(12px)}}
        to{{opacity:1;transform:translateY(0)}}
    }}
    .score-panel::before{{
        content:'';position:absolute;top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,{colors["blue"]},{colors["teal"]});
    }}
    .score-eyebrow{{
        font-size:0.68rem;font-weight:700;letter-spacing:1.5px;
        text-transform:uppercase;color:{colors["text_muted"]};margin-bottom:0.5rem;
    }}
    .score-value{{
        font-family:'JetBrains Mono',monospace;
        font-size:4.2rem;font-weight:600;
        letter-spacing:-3px;line-height:1;margin-bottom:0.25rem;
        animation:score-pop 0.7s cubic-bezier(0.16,1,0.3,1) both 0.2s;
        background: linear-gradient(135deg, {colors["navy"]}, {colors["blue"]});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    @keyframes score-pop{{
        from{{opacity:0;transform:scale(0.6);}}
        to{{opacity:1;transform:scale(1);}}
    }}
    .score-band-pill{{
        display:inline-block;padding:0.28rem 0.9rem;
        border-radius:6px;font-size:0.75rem;font-weight:700;
        letter-spacing:0.5px;text-transform:uppercase;
        margin:0.65rem 0;
        animation:fade-in 0.4s ease both 0.5s;
        transition: all 0.2s ease;
    }}
    .score-band-pill:hover {{
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    @keyframes fade-in{{from{{opacity:0}}to{{opacity:1}}}}
    .score-track-wrap{{margin:1rem auto 0;max-width:260px;}}
    .score-track{{
        height:4px;border-radius:100px;
        background:linear-gradient(90deg,
            {colors["poor"]} 0%,{colors["fair"]} 28%,
            {colors["good"]} 58%,{colors["excellent"]} 100%);
        position:relative;margin-bottom:6px;
    }}
    .score-marker{{
        position:absolute;top:50%;
        width:12px;height:12px;border-radius:50%;
        background:{colors["navy"]};border:2px solid white;
        transform:translate(-50%,-50%);
        box-shadow:0 1px 4px rgba(0,0,0,0.25);
        transition:left 1.2s cubic-bezier(0.16,1,0.3,1);
        cursor: pointer;
    }}
    .score-marker:hover {{
        transform: translate(-50%, -50%) scale(1.2);
    }}
    .score-track-labels{{
        display:flex;justify-content:space-between;
        font-size:0.6rem;color:{colors["text_muted"]};
        font-family:'JetBrains Mono',monospace;
    }}

    /* ── Improved button styles with ripple effect ── */
    .stButton>button{{
        background:{colors["blue"]}!important;
        color:white!important;border:none!important;
        border-radius:8px!important;
        padding:0.58rem 1.4rem!important;
        font-weight:600!important;font-size:0.875rem!important;
        font-family:'Plus Jakarta Sans',sans-serif!important;
        transition:all 0.3s cubic-bezier(0.16,1,0.3,1)!important;
        width:100%!important;
        position:relative!important;
        overflow:hidden!important;
        cursor:pointer!important;
    }}
    /* Ripple effect */
    .stButton>button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    .stButton>button:active::before {{
        width: 200px;
        height: 200px;
    }}
    .stButton>button:hover{{
        background:{colors["blue_hover"]}!important;
        box-shadow:0 6px 20px rgba(45,127,249,0.35)!important;
        transform:translateY(-2px) scale(1.01)!important;
    }}

    /* ── Chart tooltips ── */
    .chart-tooltip {{
        position: absolute;
        background: {colors["bg_white"]};
        border: 1px solid {colors["border"]};
        border-radius: 4px;
        padding: 0.5rem;
        font-size: 0.75rem;
        pointer-events: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 100;
        transition: opacity 0.2s;
    }}

    /* ── Print styles for PDF export ── */
    @media print {{
        .stButton, .fs-topbar, .theme-toggle, .stDownloadButton {{
            display: none !important;
        }}
        .main .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}
        .score-panel, .metric-card, .fs-card {{
            break-inside: avoid;
            box-shadow: none !important;
            border: 1px solid #ddd !important;
        }}
        body {{
            background: white !important;
            color: black !important;
        }}
        a {{
            text-decoration: none !important;
            color: black !important;
        }}
    }}

    /* Continue with your existing styles... */
    /* (Keep all the existing styles from your original theme.py here) */
    
    /* ── Responsive improvements ── */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        .score-value {{
            font-size: 2.8rem !important;
        }}
        .metric-value {{
            font-size: 1.2rem !important;
        }}
        .fs-nav-link {{
            padding: 0.25rem 0.6rem !important;
            font-size: 0.75rem !important;
        }}
        .fs-topbar {{
            padding: 0 1rem !important;
        }}
    }}
    
    /* Touch device optimizations */
    @media (hover: none) and (pointer: coarse) {{
        .stButton>button {{
            padding: 0.75rem 1.4rem !important;
        }}
        .metric-card, .rec-item {{
            cursor: pointer;
        }}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def nav_bar(active_page: str = "landing", score: Optional[int] = None, band: Optional[str] = None):
    pages = [
        ("landing", "Home"),
        ("results", "My Score"),
        ("loan_simulator", "Loan Simulator"),
        ("advisor", "AI Advisor"),
    ]
    links = ""
    for key, label in pages:
        cls = "active" if key == active_page else ""
        links += (
            f'<button class="fs-nav-link {cls}" '
            f"onclick=\"window.parent.postMessage('nav:{key}','*')\">"
            f"{label}</button>"
        )

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

    st.markdown(
        f"""
    <div class="fs-topbar">
        <div class="fs-logo">
            <div class="fs-logo-dot"></div>
            FinSight
        </div>
        <div class="fs-nav-center">{links}</div>
        <div>{right_html}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = ""):
    sub = f'<div class="fs-page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
    <div class="fs-page-header">
        <div class="fs-page-title">{title}</div>{sub}
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_toast(message: str, type: str = "info"):
    """
    Display a toast notification.
    
    Args:
        message: Toast message text
        type: 'success', 'error', 'warning', or 'info'
    """
    icons = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    st.markdown(f"""
    <div class="toast {type}">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.2rem;">{icons.get(type, 'ℹ️')}</span>
            <span style="font-size: 0.875rem;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def dark_mode_toggle():
    """Add a dark mode toggle button to the UI"""
    st.markdown(f"""
    <button class="theme-toggle" id="themeToggle" onclick="
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', isDark);
        // Reload to apply theme
        window.location.reload();
    ">
        🌓
    </button>
    <script>
        // Load saved preference
        const savedDark = localStorage.getItem('darkMode');
        if (savedDark === 'true') {{
            document.body.classList.add('dark-mode');
        }}
    </script>
    """, unsafe_allow_html=True)