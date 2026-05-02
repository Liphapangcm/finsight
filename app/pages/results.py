import streamlit as st
from app.styles.theme import COLORS
from app.components.score_gauge     import render_score_gauge
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

    # ── Header ────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1rem;">
        <h2 style="font-size:1.6rem; font-weight:800;
                   color:{COLORS['primary']}; margin-bottom:0.3rem;">
            Your FinSight Credit Report
        </h2>
        <div style="font-size:0.82rem; color:#6B7280;">
            Model {result.model_version} ·
            ID: {result.assessment_id[:8]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Narrative summary ─────────────────────────────────────────
    narrative = get_score_narrative(
        result.credit_score,
        result.score_band,
        result.shap_explanation,
        result.kpis.__dict__,
    )
    band_bg = {
        'Poor':      '#FFEBEE',
        'Fair':      '#FFF3E0',
        'Good':      '#E8F5E9',
        'Excellent': '#E0F2F1',
    }.get(result.score_band, '#F7F9FC')
    band_color = {
        'Poor':      '#C62828',
        'Fair':      '#E65100',
        'Good':      '#2E7D32',
        'Excellent': '#00695C',
    }.get(result.score_band, COLORS['primary'])

    st.markdown(f"""
    <div style="background:{band_bg}; border-radius:10px;
                padding:1rem 1.4rem; margin-bottom:1.2rem;
                border-left:4px solid {band_color};">
        <div style="font-size:0.95rem; color:{band_color};
                    line-height:1.7;">
            {narrative}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score gauge ───────────────────────────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        render_score_gauge(
            result.credit_score,
            result.score_band,
            result.risk_level,
        )

    # ── Score improvement hint ────────────────────────────────────
    next_band_msg = _next_band_message(result.credit_score, result.score_band)
    if next_band_msg:
        st.markdown(f"""
        <div style="text-align:center; font-size:0.85rem;
                    color:{COLORS['muted']}; margin-top:-0.5rem;
                    margin-bottom:1.2rem;">
            {next_band_msg}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#E5E7EB; margin:1.2rem 0;'>",
                unsafe_allow_html=True)

    # ── KPI cards ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-size:1.05rem; font-weight:700;
                color:{COLORS['primary']}; margin-bottom:0.8rem;">
        📊 Financial Health Summary
    </div>
    """, unsafe_allow_html=True)
    render_kpi_cards(result.kpis)

    st.markdown("<hr style='border-color:#E5E7EB; margin:1.2rem 0;'>",
                unsafe_allow_html=True)

    # ── SHAP + Recommendations ────────────────────────────────────
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        render_shap_chart(
            result.shap_explanation.feature_names,
            result.shap_explanation.shap_values,
            n=10,
        )
    with col_right:
        render_recommendations(result.recommendations)

    st.markdown("<hr style='border-color:#E5E7EB; margin:1.2rem 0;'>",
                unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────
    col1, col2, col3, col4= st.columns(4)

    with col1:
        if st.button("🔄 New Assessment", use_container_width=True):
            for key in ['result', 'form_step', 'monthly_income',
                        'total_debt', 'has_savings', 'has_defaulted',
                        'num_active_loans', 'payment_regularity']:
                st.session_state.pop(key, None)
            st.session_state['page'] = 'assessment'
            st.rerun()

    with col2:
        if st.button("🏦 Simulate a Loan", use_container_width=True):
            st.session_state['page'] = 'loan_simulator'
            st.rerun()

    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()

    with col4:
        # ── PDF Download ──────────────────────────────────────────
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Building your PDF report..."):
                try:
                    pdf_bytes = generate_pdf_report(result)
                    st.session_state['pdf_bytes'] = pdf_bytes
                    st.success("PDF ready! Click below to download.")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")

    # Show download button only after PDF is generated
    if 'pdf_bytes' in st.session_state:
        st.download_button(
            label     = "⬇️ Download PDF Report",
            data      = st.session_state['pdf_bytes'],
            file_name = f"finsight_report_{result.assessment_id[:8]}.pdf",
            mime      = "application/pdf",
            use_container_width=True,
        )


def _next_band_message(score: int, band: str) -> str:
    """
    Shows how many points to the next score band.
    Motivates users without overwhelming them.
    """
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
            return (f"📈 You are <strong>{points_gap} points</strong> "
                    f"away from <strong>{next_band}</strong> status.")
    if band == 'Excellent':
        return "🏆 You have reached the highest credit band. Maintain it!"
    return ""