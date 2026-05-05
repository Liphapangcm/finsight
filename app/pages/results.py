# app/pages/results.py

import re
import streamlit as st
from app.styles.theme import COLORS, SCORE_COLORS
from app.components.shap_chart      import render_shap_chart
from app.components.kpi_cards       import render_kpi_cards
from app.components.recommendations import render_recommendations
from core.explainer                 import get_score_narrative
from utils.pdf_export               import generate_pdf_report


def _md_to_html(text: str) -> str:
    """Convert **bold** markdown to HTML — prevents asterisks showing."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)


def render_results():
    # Guard against SessionInfo warning
    if 'result' not in st.session_state:
        st.info("No results yet. Complete the assessment first.")
        _, col, _ = st.columns([1, 1, 1])
        with col:
            if st.button("← Start Assessment",
                         use_container_width=True):
                st.session_state['page'] = 'assessment'
                st.rerun()
        return

    result = st.session_state['result']
    if result is None:
        st.session_state['page'] = 'assessment'
        st.rerun()
        return

    score      = result.credit_score
    band       = result.score_band
    risk       = result.risk_level
    band_color = SCORE_COLORS.get(band, COLORS["blue"])
    bar_pct    = round(((score - 300) / 550) * 100, 1)
    total_debt = max(0.0, result.kpis.debt_to_income / 100
                     * result.kpis.monthly_income)

    narrative  = _md_to_html(get_score_narrative(
        score, band,
        result.shap_explanation,
        result.kpis.__dict__,
    ))

    insight_cls = {
        "Excellent": "insight-good",
        "Good":      "insight-info",
        "Fair":      "insight-warn",
        "Poor":      "insight-bad",
    }.get(band, "insight-info")

    pill_bg = {
        "Poor":      COLORS["danger_light"],
        "Fair":      COLORS["warning_light"],
        "Good":      COLORS["success_light"],
        "Excellent": COLORS["teal_light"],
    }.get(band, COLORS["blue_light"])

    # ── Score panel + detail ──────────────────────────────────────
    col_score, col_detail = st.columns([1, 1.8])

    with col_score:
        # Use the animated gauge component
        from app.components.score_gauge import render_score_gauge
        render_score_gauge(score, band, risk)

    with col_detail:
        st.markdown(f"""
        <div class="insight-box {insight_cls}">
            {narrative}
        </div>
        """, unsafe_allow_html=True)

        next_html = _next_band_html(score, band)
        if next_html:
            st.markdown(next_html, unsafe_allow_html=True)

        # Buttons — 2×2 grid
        st.markdown("<div style='margin-top:0.75rem;'>",
                    unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            if st.button("🏦  Loan Simulator",
                         key="btn_loan",
                         use_container_width=True):
                st.session_state['page'] = 'loan_simulator'
                st.rerun()
        with b2:
            if st.button("🤖  AI Advisor",
                         key="btn_advisor",
                         use_container_width=True):
                st.session_state['page'] = 'advisor'
                st.rerun()

        b3, b4 = st.columns(2)
        with b3:
            st.markdown('<div class="btn-secondary">',
                        unsafe_allow_html=True)
            if st.button("↺  New Assessment",
                         key="btn_reassess",
                         use_container_width=True):
                for k in ['result', 'form_step', 'monthly_income',
                          'total_debt', 'has_savings', 'has_defaulted',
                          'num_active_loans', 'payment_regularity',
                          'pdf_bytes', 'chat_messages']:
                    st.session_state.pop(k, None)
                st.session_state['page'] = 'assessment'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with b4:
            st.markdown('<div class="btn-teal">',
                        unsafe_allow_html=True)
            if st.button("⬇  PDF Report",
                         key="btn_pdf",
                         use_container_width=True):
                with st.spinner("Generating report..."):
                    try:
                        st.session_state['pdf_bytes'] = \
                            generate_pdf_report(result)
                    except Exception as e:
                        st.error(f"PDF error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get('pdf_bytes'):
            st.download_button(
                label              = "⬇️  Download PDF",
                data               = st.session_state['pdf_bytes'],
                file_name          = (f"finsight_"
                                      f"{result.assessment_id[:8]}.pdf"),
                mime               = "application/pdf",
                use_container_width= True,
            )

    st.markdown('<div class="fs-divider"></div>',
                unsafe_allow_html=True)

    # ── Financial Health ──────────────────────────────────────────
    st.markdown(
        '<div class="section-label">Financial Health Summary</div>',
        unsafe_allow_html=True)
    render_kpi_cards(result.kpis)

    st.markdown('<div class="fs-divider"></div>',
                unsafe_allow_html=True)

    # ── SHAP + Recommendations ────────────────────────────────────
    col_l, col_r = st.columns([1.1, 0.9])
    with col_l:
        st.markdown(
            '<div class="section-label">Score Factor Analysis</div>',
            unsafe_allow_html=True)
        # Pass total_debt so the chart can suppress misleading
        # negative debt bars when the user has zero debt
        render_shap_chart(
            result.shap_explanation.feature_names,
            result.shap_explanation.shap_values,
            n=10,
            total_debt=total_debt,
        )
    with col_r:
        st.markdown(
            '<div class="section-label">Prioritised Action Plan</div>',
            unsafe_allow_html=True)
        render_recommendations(result.recommendations)

    st.markdown(f"""
    <div class="share-tip">
        📸 Screenshot your score and share it —
        <strong>challenge your network to beat it</strong>
    </div>
    """, unsafe_allow_html=True)


def _next_band_html(score: int, band: str) -> str:
    order  = ["Poor", "Fair", "Good", "Excellent"]
    thresh = [450, 580, 700, 851]
    lo_map = {"Poor": 300, "Fair": 450, "Good": 580, "Excellent": 700}
    nc_map = {
        "Fair":      COLORS["fair"],
        "Good":      COLORS["good"],
        "Excellent": COLORS["excellent"],
    }

    if band == "Excellent":
        return f"""
        <div style="background:{COLORS['teal_light']};
                    border:1px solid {COLORS['teal']}40;
                    border-radius:7px;padding:0.65rem 0.9rem;
                    font-size:0.8rem;color:{COLORS['good']};
                    margin-bottom:0.75rem;font-weight:500;">
            🏆 You've reached the highest credit band. Maintain it.
        </div>"""

    for i, b in enumerate(order[:-1]):
        if b == band:
            next_band = order[i + 1]
            gap       = thresh[i] - score
            nc        = nc_map.get(next_band, COLORS["blue"])
            lo        = lo_map.get(band, 300)
            span      = thresh[i] - lo
            pct       = round(((score - lo) / max(span, 1)) * 100)
            return f"""
            <div class="next-band-bar">
                <div style="display:flex;justify-content:space-between;
                            align-items:center;">
                    <span style="font-size:0.78rem;
                                 color:{COLORS['text_secondary']};">
                        📈
                        <strong style="color:{COLORS['text']};">
                            {gap} points
                        </strong>
                        to
                        <strong style="color:{nc};">{next_band}</strong>
                    </span>
                    <span style="font-family:'JetBrains Mono',monospace;
                                 font-size:0.7rem;
                                 color:{COLORS['text_muted']};">
                        {pct}%
                    </span>
                </div>
                <div class="bar-outer">
                    <div class="bar-inner"
                         style="width:{pct}%;"></div>
                </div>
            </div>"""
    return ""