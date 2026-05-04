# app/pages/loan_sim.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from app.styles.theme import COLORS
from core.loan_simulator import simulate_loan


def _c(key: str, fallback: str = "#0A1F44") -> str:
    """Safe color getter — never raises KeyError."""
    return COLORS.get(key, fallback)


def render_loan_simulator():
    result = st.session_state.get('result')

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div class="fs-page-title">🏦 Loan Eligibility Simulator</div>
        <div class="fs-page-subtitle">
            See how a loan would affect your financial profile
            and what your approval chances look like.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not result:
        st.info("Complete your credit assessment first to use "
                "the loan simulator.")
        _, col, _ = st.columns([1, 1, 1])
        with col:
            if st.button("← Take Assessment",
                         use_container_width=True):
                st.session_state['page'] = 'assessment'
                st.rerun()
        return

    # ── Loan inputs ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-label">Configure Your Loan</div>',
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input(
            "Loan Amount (LSL — Maloti)",
            min_value=1_000.0, max_value=500_000.0,
            value=20_000.0, step=1_000.0, format="%.0f",
        )
    with col2:
        loan_term = st.slider(
            "Repayment Term (months)",
            min_value=3, max_value=84, value=24, step=3,
        )
        st.caption(
            f"{loan_term} months = "
            f"{loan_term // 12} yr {loan_term % 12} mo"
        )

    # ── Derive simulation inputs from result ──────────────────────
    income         = result.kpis.monthly_income
    total_expenses = result.kpis.total_expenses
    savings        = max(0.0, result.kpis.savings_rate / 100 * income)
    total_debt     = max(0.0, result.kpis.debt_to_income / 100 * income)
    has_defaulted  = any(
        "default" in r.title.lower()
        for r in result.recommendations
    )

    sim = simulate_loan(
        loan_amount    = loan_amount,
        loan_term      = loan_term,
        credit_score   = result.credit_score,
        monthly_income = income,
        total_expenses = total_expenses,
        monthly_savings= savings,
        total_debt     = total_debt,
        has_defaulted  = has_defaulted,
    )

    # ── Summary KPI row ───────────────────────────────────────────
    st.markdown("<div style='margin-top:1.25rem;'>",
                unsafe_allow_html=True)
    prob_pct  = int(sim.approval_probability * 100)
    appr_color= sim.approval_color

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="metric-card"
             style="border-top:3px solid {appr_color};">
            <div class="metric-label">Approval Probability</div>
            <div class="metric-value"
                 style="color:{appr_color};">{prob_pct}%</div>
            <div class="metric-badge b-info">{sim.approval_label}</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        a_cls = "b-good" if sim.affordability.is_affordable else "b-bad"
        a_lbl = "Affordable" if sim.affordability.is_affordable \
                else "Too High"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Payment</div>
            <div class="metric-value">M{sim.monthly_payment:,.0f}</div>
            <div class="metric-badge {a_cls}">{a_lbl}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Interest Cost</div>
            <div class="metric-value">M{sim.total_interest:,.0f}</div>
            <div class="metric-badge b-info">
                {sim.effective_rate}% per year
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Affordability alert ───────────────────────────────────────
    aff   = sim.affordability
    a_col = _c('success') if aff.is_affordable else _c('danger')
    a_bg  = _c('success_light') if aff.is_affordable \
            else _c('danger_light')
    st.markdown(f"""
    <div style="background:{a_bg};border-radius:8px;
                padding:0.8rem 1.1rem;margin:1rem 0;
                border-left:3px solid {a_col};font-size:0.85rem;">
        <strong style="color:{a_col};">
            {aff.affordability_message}
        </strong><br/>
        <span style="font-size:0.78rem;color:{_c('text_secondary')};">
            Max affordable monthly payment:
            M{aff.max_affordable_monthly:,.0f}
            &nbsp;·&nbsp;
            Max affordable loan at this term:
            M{aff.max_affordable_loan:,.0f}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Repayment Breakdown",
        "🏦 Loan Products",
        "📅 Payment Schedule",
        "💡 Tips",
    ])

    with tab1:
        c_chart, c_summary = st.columns([1, 1])
        with c_chart:
            fig = go.Figure(go.Pie(
                labels   = ['Principal', 'Total Interest'],
                values   = [loan_amount, sim.total_interest],
                hole     = 0.55,
                marker   = dict(colors=[_c('blue'), _c('warning')]),
                textinfo = 'label+percent',
                textfont = dict(size=12),
            ))
            fig.update_layout(
                height        = 260,
                margin        = dict(t=20, b=20, l=20, r=20),
                paper_bgcolor = 'rgba(0,0,0,0)',
                showlegend    = False,
                annotations   = [dict(
                    text       = f"M{sim.total_repayable:,.0f}",
                    x=0.5, y=0.5,
                    font_size  = 14,
                    font_color = _c('navy'),
                    showarrow  = False,
                )],
            )
            st.plotly_chart(fig, use_container_width=True,
                            config={'displayModeBar': False})

        with c_summary:
            rows = [
                ("Loan Amount",     f"M{loan_amount:,.0f}"),
                ("Term",            f"{loan_term} months"),
                ("Interest Rate",   f"{sim.effective_rate}% p.a."),
                ("Monthly Payment", f"M{sim.monthly_payment:,.0f}"),
                ("Total Interest",  f"M{sim.total_interest:,.0f}"),
                ("Total Repayable", f"M{sim.total_repayable:,.0f}"),
            ]
            for lbl, val in rows:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;
                            padding:0.5rem 0;
                            border-bottom:1px solid {_c('border')};">
                    <span style="color:{_c('text_secondary')};
                                 font-size:0.85rem;">{lbl}</span>
                    <span style="font-weight:700;color:{_c('navy')};
                                 font-size:0.88rem;
                                 font-family:'JetBrains Mono',monospace;">
                        {val}
                    </span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div style="font-size:0.8rem;color:{_c('text_muted')};
                    margin-bottom:1rem;">
            Products matching your score and requested amount.
        </div>
        """, unsafe_allow_html=True)
        for product in sim.eligible_products:
            bg     = _c('success_light') if product.eligible \
                     else _c('bg')
            border = _c('success') if product.eligible \
                     else _c('border')
            label_color = _c('success') if product.eligible \
                          else _c('text_muted')
            st.markdown(f"""
            <div class="fs-card"
                 style="background:{bg};
                        border-left:3px solid {border};
                        margin-bottom:0.6rem;">
                <div style="display:flex;justify-content:space-between;
                            align-items:flex-start;">
                    <div>
                        <div style="font-weight:700;font-size:0.92rem;
                                    color:{_c('navy')};">
                            {product.name}
                        </div>
                        <div style="font-size:0.78rem;
                                    color:{_c('text_muted')};
                                    margin:0.2rem 0;">
                            {product.provider}
                        </div>
                        <div style="font-size:0.8rem;
                                    color:{label_color};">
                            {product.reason}
                        </div>
                    </div>
                    <div style="text-align:right;min-width:110px;">
                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:1.1rem;font-weight:600;
                                    color:{_c('navy')};">
                            {product.interest_rate}%
                        </div>
                        <div style="font-size:0.72rem;
                                    color:{_c('text_muted')};">
                            per year
                        </div>
                        <div style="font-size:0.82rem;font-weight:600;
                                    color:{_c('navy')};margin-top:3px;">
                            M{product.monthly_payment:,.0f}/mo
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("##### First 12 months of repayment")
        rows = [{
            "Month":     s.month,
            "Payment":   f"M{s.payment:,.2f}",
            "Principal": f"M{s.principal:,.2f}",
            "Interest":  f"M{s.interest:,.2f}",
            "Balance":   f"M{s.balance:,.2f}",
        } for s in sim.schedule]
        st.dataframe(pd.DataFrame(rows),
                     use_container_width=True, hide_index=True)

        fig2 = px.line(
            pd.DataFrame([
                {"Month": s.month, "Remaining Balance": s.balance}
                for s in sim.schedule
            ]),
            x="Month", y="Remaining Balance",
            title="Loan Balance Over Time",
            color_discrete_sequence=[_c('blue')],
        )
        fig2.update_layout(
            height        = 220,
            margin        = dict(t=40, b=20, l=10, r=10),
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor  = 'rgba(0,0,0,0)',
            yaxis         = dict(gridcolor=_c('border')),
            xaxis         = dict(gridcolor=_c('border')),
        )
        st.plotly_chart(fig2, use_container_width=True,
                        config={'displayModeBar': False})

    with tab4:
        for tip in sim.tips:
            st.markdown(f"""
            <div class="fs-card"
                 style="margin-bottom:0.6rem;font-size:0.88rem;
                        line-height:1.7;">
                {tip}
            </div>
            """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;'>",
                unsafe_allow_html=True)
    nav1, nav2 = st.columns(2)
    with nav1:
        st.markdown('<div class="btn-secondary">',
                    unsafe_allow_html=True)
        if st.button("← Back to My Score",
                     use_container_width=True):
            st.session_state['page'] = 'results'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with nav2:
        st.markdown('<div class="btn-secondary">',
                    unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)