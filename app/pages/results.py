# app/pages/results.py
"""
FinSight Results Page — All bugs fixed:
- Asterisks in narrative replaced with proper HTML bold
- Zero debt no longer shows negative DTI/debt repayment
- Score counter animation via JS
- Animated metric cards with stagger
- Button layout fixed (2x2 grid)
- Loading state guard prevents SessionInfo warning
"""
import re
import streamlit as st
from app.styles.theme import COLORS, SCORE_COLORS
from app.components.shap_chart      import render_shap_chart
from app.components.kpi_cards       import render_kpi_cards
from app.components.recommendations import render_recommendations
from core.explainer                 import get_score_narrative
from utils.pdf_export               import generate_pdf_report


def _md_to_html(text: str) -> str:
    """
    Converts **bold** markdown to <strong> HTML tags.
    Prevents asterisks appearing literally in insight boxes.
    """
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)


def render_results():
    # ── Guard: prevent SessionInfo warning on first load ──────────
    if 'result' not in st.session_state:
        st.info("No results yet. Complete the assessment first.")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
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

    # Score marker position on 300–850 range
    bar_pct = round(((score - 300) / 550) * 100, 1)

    # ── Narrative — convert **bold** to HTML, not raw asterisks ───
    raw_narrative = get_score_narrative(
        score, band,
        result.shap_explanation,
        result.kpis.__dict__,
    )
    narrative = _md_to_html(raw_narrative)

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

    # ── Layout: score (left) + actions (right) ────────────────────
    col_score, col_detail = st.columns([1, 1.8])

    with col_score:
        st.markdown(f"""
        <div class="score-panel">
            <div class="score-eyebrow">Credit Score</div>

            <!-- Animated score counter -->
            <div class="score-value"
                 id="score-display"
                 style="color:{band_color};">
                {score}
            </div>
            <script>
            (function() {{
                var el = document.getElementById('score-display');
                if (!el || el.dataset.animated) return;
                el.dataset.animated = '1';
                var target = {score};
                var start  = Math.max(300, target - 180);
                var dur    = 900;
                var t0     = null;
                function ease(t) {{ return 1 - Math.pow(1 - t, 3); }}
                function step(ts) {{
                    if (!t0) t0 = ts;
                    var p = Math.min((ts - t0) / dur, 1);
                    el.textContent = Math.round(start + (target - start) * ease(p));
                    if (p < 1) requestAnimationFrame(step);
                    else el.textContent = target;
                }}
                requestAnimationFrame(step);
            }})();
            </script>

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
                         id="score-marker"
                         style="left:0%;background:{band_color};">
                    </div>
                </div>
                <div class="score-track-labels">
                    <span>300</span><span>Poor</span>
                    <span>Fair</span><span>Good</span><span>850</span>
                </div>
            </div>
            <script>
            (function() {{
                var m = document.getElementById('score-marker');
                if (!m || m.dataset.moved) return;
                m.dataset.moved = '1';
                setTimeout(function() {{
                    m.style.left = '{bar_pct}%';
                }}, 300);
            }})();
            </script>
            <div style="margin-top:1rem;padding-top:1rem;
                        border-top:1px solid {COLORS['border']};
                        font-size:0.68rem;color:{COLORS['text_muted']};
                        font-family:'JetBrains Mono',monospace;">
                Model&nbsp;{result.model_version}
                &nbsp;·&nbsp;
                ID&nbsp;{result.assessment_id[:8]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_detail:
        # Narrative with proper HTML bold
        st.markdown(f"""
        <div class="insight-box {insight_cls}">
            {narrative}
        </div>
        """, unsafe_allow_html=True)

        # Next band progress bar
        next_html = _next_band_html(score, band)
        if next_html:
            st.markdown(next_html, unsafe_allow_html=True)

        # ── Action buttons — 2×2 grid, always aligned ─────────────
        st.markdown("<div style='margin-top:0.75rem;'>",
                    unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            if st.button("🏦  Loan Simulator",
                         key="btn_loan", use_container_width=True):
                st.session_state['page'] = 'loan_simulator'
                st.rerun()
        with r1c2:
            if st.button("🤖  AI Advisor",
                         key="btn_advisor", use_container_width=True):
                st.session_state['page'] = 'advisor'
                st.rerun()

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown('<div class="btn-secondary">',
                        unsafe_allow_html=True)
            if st.button("↺  New Assessment",
                         key="btn_reassess", use_container_width=True):
                for k in ['result', 'form_step', 'monthly_income',
                          'total_debt', 'has_savings', 'has_defaulted',
                          'num_active_loans', 'payment_regularity',
                          'pdf_bytes']:
                    st.session_state.pop(k, None)
                st.session_state['page'] = 'assessment'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with r2c2:
            st.markdown('<div class="btn-teal">',
                        unsafe_allow_html=True)
            if st.button("⬇  PDF Report",
                         key="btn_pdf", use_container_width=True):
                with st.spinner("Generating report..."):
                    try:
                        pdf_bytes = generate_pdf_report(result)
                        st.session_state['pdf_bytes'] = pdf_bytes
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

    # ── Divider ───────────────────────────────────────────────────
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
        render_shap_chart(
            result.shap_explanation.feature_names,
            result.shap_explanation.shap_values,
            n=10,
        )
    with col_r:
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


def _next_band_html(score: int, band: str) -> str:
    """Returns animated progress bar toward next score band."""
    order  = ["Poor", "Fair", "Good", "Excellent"]
    thresh = [450, 580, 700, 851]
    nc_map = {
        "Fair":      COLORS["fair"],
        "Good":      COLORS["good"],
        "Excellent": COLORS["excellent"],
    }
    lo_map = {
        "Poor": 300, "Fair": 450,
        "Good": 580, "Excellent": 700,
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
            pct       = round(((score - lo) / span) * 100)
            return f"""
            <div class="next-band-bar">
                <div style="display:flex;justify-content:space-between;
                            align-items:center;">
                    <span style="font-size:0.78rem;
                                 color:{COLORS['text_secondary']};">
                        📈 <strong style="color:{COLORS['text']};">
                        {gap} points</strong> to
                        <strong style="color:{nc};">{next_band}</strong>
                    </span>
                    <span style="font-family:'JetBrains Mono',monospace;
                                 font-size:0.7rem;
                                 color:{COLORS['text_muted']};">{pct}%</span>
                </div>
                <div class="bar-outer">
                    <div class="bar-inner"
                         style="width:{pct}%;
                                --bar-width:{pct}%;"></div>
                </div>
            </div>"""
    return ""