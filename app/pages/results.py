"""
FinSight Results Dashboard
Professional Palantir / Bloomberg aesthetic.
Light, data-dense, precise typography.
"""
import streamlit as st
from app.styles.theme import COLORS, SCORE_COLORS, page_header
from app.components.shap_chart       import render_shap_chart
from app.components.kpi_cards        import render_kpi_cards
from app.components.recommendations  import render_recommendations
from core.explainer                  import get_score_narrative
from utils.pdf_export                import generate_pdf_report


def render_results():
    result = st.session_state.get('result')
    if not result:
        st.warning("No results found. Complete the assessment first.")
        if st.button("← Start Assessment"):
            st.session_state['page'] = 'assessment'
            st.rerun()
        return

    score      = result.credit_score
    band       = result.score_band
    risk       = result.risk_level
    band_color = SCORE_COLORS.get(band, COLORS["blue"])

    # Score marker position on 300–850 range
    bar_pct = round(((score - 300) / 550) * 100, 1)

    # Narrative insight
    narrative = get_score_narrative(
        score, band,
        result.shap_explanation,
        result.kpis.__dict__,
    )
    insight_cls = {
        "Excellent": "insight-good",
        "Good":      "insight-info",
        "Fair":      "insight-warn",
        "Poor":      "insight-bad",
    }.get(band, "insight-info")

    # Score band pill colors
    pill_bg = {
        "Poor":      COLORS["danger_light"],
        "Fair":      COLORS["warning_light"],
        "Good":      COLORS["success_light"],
        "Excellent": COLORS["teal_light"],
    }.get(band, COLORS["blue_light"])

    # ── Layout: score panel (left) + narrative+actions (right) ───
    col_score, col_detail = st.columns([1, 1.8])

    with col_score:
        st.markdown(f"""
        <div class="score-panel">
            <div class="score-eyebrow">Credit Score</div>
            <div class="score-value" style="color:{band_color};">
                {score}
            </div>
            <div style="font-size:0.72rem;color:{COLORS['text_muted']};
                        margin-bottom:0.25rem;
                        font-family:'JetBrains Mono',monospace;">
                out of 850
            </div>
            <div class="score-band-pill"
                 style="background:{pill_bg};color:{band_color};">
                {band}
            </div>
            <div style="font-size:0.75rem;color:{COLORS['text_muted']};
                        margin-bottom:0.75rem;">
                Risk Level:
                <strong style="color:{COLORS['text']};">{risk}</strong>
            </div>
            <div class="score-track-wrap">
                <div class="score-track">
                    <div class="score-marker"
                         style="left:{bar_pct}%;
                                background:{band_color};"></div>
                </div>
                <div class="score-track-labels">
                    <span>300</span>
                    <span>Poor</span>
                    <span>Fair</span>
                    <span>Good</span>
                    <span>850</span>
                </div>
            </div>
            <div style="margin-top:1rem;padding-top:1rem;
                        border-top:1px solid {COLORS['border']};
                        font-size:0.72rem;color:{COLORS['text_muted']};
                        font-family:'JetBrains Mono',monospace;">
                Model {result.model_version}
                &nbsp;·&nbsp;
                ID&nbsp;{result.assessment_id[:8]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_detail:
        # Narrative insight box
        st.markdown(f"""
        <div class="insight-box {insight_cls}">
            {narrative}
        </div>
        """, unsafe_allow_html=True)

        # Next band progress
        next_msg = _next_band_message(score, band)
        if next_msg:
            st.markdown(next_msg, unsafe_allow_html=True)

        # Action buttons
        st.markdown("<div style='margin-top:1rem;'>",
                    unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            if st.button("🏦 Loan Simulator",
                         key="to_loan", use_container_width=True):
                st.session_state['page'] = 'loan_simulator'
                st.rerun()
        with r2:
            if st.button("🤖 AI Advisor",
                         key="to_advisor", use_container_width=True):
                st.session_state['page'] = 'advisor'
                st.rerun()

        r3, r4 = st.columns(2)
        with r3:
            st.markdown('<div class="btn-secondary">',
                        unsafe_allow_html=True)
            if st.button("↺ New Assessment",
                         key="reassess", use_container_width=True):
                for k in ['result', 'form_step', 'monthly_income',
                          'total_debt', 'has_savings', 'has_defaulted',
                          'num_active_loans', 'payment_regularity']:
                    st.session_state.pop(k, None)
                st.session_state['page'] = 'assessment'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with r4:
            st.markdown('<div class="btn-teal">',
                        unsafe_allow_html=True)
            if st.button("⬇ PDF Report",
                         key="pdf_btn", use_container_width=True):
                with st.spinner("Generating report..."):
                    try:
                        pdf_bytes = generate_pdf_report(result)
                        st.session_state['pdf_bytes'] = pdf_bytes
                    except Exception as e:
                        st.error(f"PDF error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

        if 'pdf_bytes' in st.session_state:
            st.download_button(
                label    = "⬇️ Download PDF",
                data     = st.session_state['pdf_bytes'],
                file_name= f"finsight_{result.assessment_id[:8]}.pdf",
                mime     = "application/pdf",
                use_container_width=True,
            )

    # ── Divider ───────────────────────────────────────────────────
    st.markdown('<div class="fs-divider"></div>',
                unsafe_allow_html=True)

    # ── Financial Health ──────────────────────────────────────────
    st.markdown('<div class="section-label">Financial Health Summary</div>',
                unsafe_allow_html=True)
    render_kpi_cards(result.kpis)

    st.markdown('<div class="fs-divider"></div>',
                unsafe_allow_html=True)

    # ── Factor Analysis + Action Plan ─────────────────────────────
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown(
            '<div class="section-label">Score Factor Analysis</div>',
            unsafe_allow_html=True)
        render_shap_chart(
            result.shap_explanation.feature_names,
            result.shap_explanation.shap_values,
            n=10,
        )
    with col_right:
        st.markdown(
            '<div class="section-label">Prioritised Action Plan</div>',
            unsafe_allow_html=True)
        render_recommendations(result.recommendations)

    # ── Share tip ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="share-tip">
        📸 Screenshot your score and share it —
        <strong>challenge your network to beat it</strong>
    </div>
    """, unsafe_allow_html=True)


def _next_band_message(score: int, band: str) -> str:
    order  = ["Poor", "Fair", "Good", "Excellent"]
    thresh = [450, 580, 700, 851]
    colors = {
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
            next_band  = order[i + 1]
            gap        = thresh[i] - score
            nc         = colors.get(next_band, COLORS["blue"])
            pct        = round((score - (thresh[i-1] if i > 0 else 300))
                               / (thresh[i] - (thresh[i-1] if i > 0
                               else 300)) * 100)
            return f"""
            <div style="background:{COLORS['bg']};
                        border:1px solid {COLORS['border']};
                        border-radius:7px;padding:0.65rem 0.9rem;
                        margin-bottom:0.75rem;">
                <div style="display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:0.4rem;">
                    <span style="font-size:0.78rem;
                                 color:{COLORS['text_secondary']};">
                        📈 <strong style="color:{COLORS['text']};">
                        {gap} points</strong> to
                        <strong style="color:{nc};">{next_band}</strong>
                    </span>
                    <span style="font-family:'JetBrains Mono',monospace;
                                 font-size:0.7rem;
                                 color:{COLORS['text_muted']};">
                        {pct}%
                    </span>
                </div>
                <div style="height:3px;background:{COLORS['border']};
                            border-radius:100px;overflow:hidden;">
                    <div style="width:{pct}%;height:3px;
                                background:linear-gradient(90deg,
                                    {COLORS['blue']},{nc});
                                border-radius:100px;"></div>
                </div>
            </div>"""
    return ""