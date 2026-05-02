# app/pages/results.py
"""
FinSight Results Page — Premium Dark UI
Designed to be screenshot-worthy and shareable on social media.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from app.styles.theme import COLORS, SCORE_COLORS, SCORE_GRADIENTS
from app.components.shap_chart      import render_shap_chart
from app.components.kpi_cards       import render_kpi_cards
from app.components.recommendations import render_recommendations
from core.explainer                 import get_score_narrative
from utils.pdf_export               import generate_pdf_report


def render_results():
    result = st.session_state.get('result')
    if not result:
        st.warning("No results found. Please complete the assessment first.")
        if st.button("← Start Assessment"):
            st.session_state['page'] = 'assessment'
            st.rerun()
        return

    score      = result.credit_score
    band       = result.score_band
    band_color = SCORE_COLORS.get(band, COLORS['primary'])
    gradient   = SCORE_GRADIENTS.get(band, SCORE_GRADIENTS['Good'])

    # ── Score position on bar (300-850 range) ────────────────────
    bar_pct = ((score - 300) / 550) * 100

    # ── Narrative ─────────────────────────────────────────────────
    narrative = get_score_narrative(
        score, band,
        result.shap_explanation,
        result.kpis.__dict__,
    )

    # ── THE SHAREABLE SCORE CARD ──────────────────────────────────
    col_l, col_c, col_r = st.columns([0.8, 2, 0.8])
    with col_c:
        st.markdown(f"""
        <div class="score-reveal-card">

            <!-- Decorative ring -->
            <div style="
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                width: 260px; height: 260px;
                border-radius: 50%;
                border: 1px solid rgba(255,255,255,0.04);
                pointer-events: none;
            "></div>
            <div style="
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                width: 220px; height: 220px;
                border-radius: 50%;
                border: 1px solid rgba(255,255,255,0.03);
                pointer-events: none;
            "></div>

            <!-- FinSight watermark -->
            <div style="
                position: absolute;
                top: 1.2rem; right: 1.4rem;
                font-family: 'Syne', sans-serif;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 1px;
                background: linear-gradient(135deg,
                    {COLORS['primary']}, {COLORS['gold']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                opacity: 0.7;
            ">FINSIGHT</div>

            <div class="score-label">CREDIT SCORE</div>

            <div class="score-number" style="
                background: {gradient};
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">{score}</div>

            <div style="color:{COLORS['text_muted']};
                        font-size:0.75rem; margin-bottom:0.5rem;">
                out of 850
            </div>

            <span class="score-band-pill" style="
                background: {band_color}18;
                color: {band_color};
                border: 1px solid {band_color}40;
            ">{band.upper()}</span>

            <!-- Score bar -->
            <div class="score-bar-container">
                <div class="score-bar-track">
                    <div class="score-bar-marker"
                         style="left:{bar_pct}%;
                                color:{band_color};
                                border-color:{band_color};">
                    </div>
                </div>
                <div class="score-bar-labels">
                    <span>300</span>
                    <span>Poor</span>
                    <span>Fair</span>
                    <span>Good</span>
                    <span>850</span>
                </div>
            </div>

            <!-- Risk level -->
            <div style="
                margin-top: 0.8rem;
                padding: 0.6rem 1.2rem;
                background: rgba(255,255,255,0.03);
                border-radius: 100px;
                display: inline-block;
                font-size: 0.78rem;
                color: {COLORS['text_secondary']};
            ">
                Risk Level:
                <strong style="color:{band_color};">
                    {result.risk_level}
                </strong>
                &nbsp;·&nbsp; Model {result.model_version}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.5rem;'>",
                unsafe_allow_html=True)

    # ── Narrative summary ─────────────────────────────────────────
    col_l, col_c, col_r = st.columns([0.3, 3, 0.3])
    with col_c:
        narrative_bg    = f"{band_color}0D"
        narrative_border= f"{band_color}30"
        st.markdown(f"""
        <div class="narrative-box" style="
            background: {narrative_bg};
            border-color: {band_color};
            border-left-color: {band_color};
        ">
            <span style="color:{COLORS['text_secondary']};
                         font-size:0.9rem;">{narrative}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Next band progress ────────────────────────────────────────
    next_msg = _next_band_message(score, band)
    if next_msg:
        col_l, col_c, col_r = st.columns([0.3, 3, 0.3])
        with col_c:
            st.markdown(f"""
            <div style="text-align:center; margin-bottom:1.5rem;">
                <span style="
                    font-size:0.82rem;
                    color:{COLORS['text_muted']};
                ">{next_msg}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────
    st.markdown("<div style='margin-bottom:2rem;'>",
                unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("↺  Reassess", use_container_width=True):
            for key in ['result','form_step','monthly_income',
                        'total_debt','has_savings','has_defaulted',
                        'num_active_loans','payment_regularity']:
                st.session_state.pop(key, None)
            st.session_state['page'] = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        if st.button("🏦  Loan Sim", use_container_width=True):
            st.session_state['page'] = 'loan_simulator'
            st.rerun()

    with c3:
        if st.button("🤖  AI Advisor", use_container_width=True):
            st.session_state['page'] = 'advisor'
            st.rerun()

    with c4:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("🏠  Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("⬇  PDF Report", use_container_width=True):
            with st.spinner("Building report..."):
                try:
                    pdf_bytes = generate_pdf_report(result)
                    st.session_state['pdf_bytes'] = pdf_bytes
                except Exception as e:
                    st.error(f"PDF error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'pdf_bytes' in st.session_state:
        st.download_button(
            label              = "⬇️ Download PDF",
            data               = st.session_state['pdf_bytes'],
            file_name          = f"finsight_{result.assessment_id[:8]}.pdf",
            mime               = "application/pdf",
            use_container_width= True,
        )

    st.markdown("""
    <div style="height:1px; background:linear-gradient(90deg,
        transparent, rgba(255,255,255,0.06), transparent);
        margin: 1.5rem 0;">
    </div>
    """, unsafe_allow_html=True)

    # ── Financial Health Summary ──────────────────────────────────
    st.markdown('<div class="section-header">📊 Financial Health</div>',
                unsafe_allow_html=True)
    render_kpi_cards(result.kpis)

    st.markdown("""
    <div style="height:1px; background:linear-gradient(90deg,
        transparent, rgba(255,255,255,0.06), transparent);
        margin: 1.5rem 0;">
    </div>
    """, unsafe_allow_html=True)

    # ── SHAP + Recommendations ────────────────────────────────────
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown('<div class="section-header">🔍 Score Factors</div>',
                    unsafe_allow_html=True)
        render_shap_chart(
            result.shap_explanation.feature_names,
            result.shap_explanation.shap_values,
            n=10,
        )
    with col_right:
        st.markdown('<div class="section-header">📋 Action Plan</div>',
                    unsafe_allow_html=True)
        render_recommendations(result.recommendations)

    # ── Screenshot tip ────────────────────────────────────────────
    st.markdown(f"""
    <div style="
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        background: rgba(245,200,66,0.04);
        border: 1px solid rgba(245,200,66,0.1);
        border-radius: 12px;
        font-size: 0.8rem;
        color: {COLORS['text_muted']};
    ">
        📸 Screenshot your score card and share it —
        <span style="color:{COLORS['gold']};">
            challenge your friends to beat your score
        </span>
    </div>
    """, unsafe_allow_html=True)


def _next_band_message(score: int, band: str) -> str:
    bands = [
        (300, 449, 'Poor'),
        (450, 579, 'Fair'),
        (580, 699, 'Good'),
        (700, 850, 'Excellent'),
    ]
    thresholds = [450, 580, 700, 851]
    for i, (lo, hi, b) in enumerate(bands):
        if b == band and i < len(bands) - 1:
            next_band  = bands[i+1][2]
            points_gap = thresholds[i] - score
            next_color = SCORE_COLORS.get(next_band, COLORS['primary'])
            return (
                f"📈 <strong style='color:{COLORS['text_primary']};'>"
                f"{points_gap} points</strong> away from "
                f"<strong style='color:{next_color};'>{next_band}</strong>"
            )
    if band == 'Excellent':
        return (
            f"🏆 <strong style='color:{COLORS['gold']};'>"
            f"You've reached the top band.</strong> Maintain it."
        )
    return ""