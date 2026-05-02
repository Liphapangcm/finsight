import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.styles.theme import COLORS
from core.loan_simulator import simulate_loan


def render_loan_simulator():
    result = st.session_state.get('result')

    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-size:1.6rem; font-weight:800;
                   color:{COLORS['primary']};">
            🏦 Loan Eligibility Simulator
        </h2>
        <p style="color:#6B7280; font-size:0.92rem;">
            See how a loan would affect your financial profile
            and what your approval chances look like.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Require a completed assessment ───────────────────────────
    if not result:
        st.info("Complete your credit assessment first to use the "
                "loan simulator.")
        if st.button("← Take Assessment"):
            st.session_state['page'] = 'assessment'
            st.rerun()
        return

    # ── Input panel ───────────────────────────────────────────────
    st.markdown('<div class="fs-card fs-card-accent">',
                unsafe_allow_html=True)
    st.markdown("### Configure Your Loan")

    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input(
            "Loan Amount (LSL — Maloti)",
            min_value    = 1_000.0,
            max_value    = 500_000.0,
            value        = 20_000.0,
            step         = 1_000.0,
            format       = "%.0f",
            help         = "How much do you want to borrow?"
        )
    with col2:
        loan_term = st.slider(
            "Repayment Term (months)",
            min_value = 3,
            max_value = 84,
            value     = 24,
            step      = 3,
        )
        st.caption(f"{loan_term} months = "
                   f"{loan_term//12} yr {loan_term%12} mo")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Run simulation ────────────────────────────────────────────
    sim = simulate_loan(
        loan_amount    = loan_amount,
        loan_term      = loan_term,
        credit_score   = result.credit_score,
        monthly_income = result.kpis.monthly_income,
        total_expenses = result.kpis.total_expenses,
        monthly_savings= result.kpis.savings_rate / 100
                         * result.kpis.monthly_income,
        total_debt     = result.kpis.debt_to_income / 100
                         * result.kpis.monthly_income,
        has_defaulted  = any(
            "default" in r.title.lower()
            for r in result.recommendations
        ),
    )

    # ── Approval probability card ─────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;'>",
                unsafe_allow_html=True)

    prob_pct = int(sim.approval_probability * 100)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid
             {sim.approval_color};">
            <div class="kpi-value"
                 style="color:{sim.approval_color};">
                {prob_pct}%
            </div>
            <div class="kpi-label">Approval Probability</div>
            <div class="kpi-delta"
                 style="color:{sim.approval_color};">
                {sim.approval_label}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">M{sim.monthly_payment:,.0f}</div>
            <div class="kpi-label">Monthly Payment</div>
            <div class="kpi-delta
                 {'kpi-positive' if sim.affordability.is_affordable
                  else 'kpi-negative'}">
                {'Affordable' if sim.affordability.is_affordable
                 else 'Too High'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">M{sim.total_interest:,.0f}</div>
            <div class="kpi-label">Total Interest Cost</div>
            <div class="kpi-delta kpi-neutral">
                {sim.effective_rate}% per year
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Affordability message ────────────────────────────────────
    aff   = sim.affordability
    a_col = COLORS['success'] if aff.is_affordable else COLORS['danger']
    a_bg  = '#E8F5E9' if aff.is_affordable else '#FFEBEE'
    st.markdown(f"""
    <div style="background:{a_bg}; border-radius:8px;
                padding:0.8rem 1.2rem; margin:1rem 0;
                border-left:4px solid {a_col};">
        <span style="color:{a_col}; font-weight:600;">
            {aff.affordability_message}
        </span><br/>
        <span style="font-size:0.82rem; color:#6B7280;">
            Max affordable monthly payment: M{aff.max_affordable_monthly:,.0f}
            &nbsp;·&nbsp;
            Max affordable loan at this term:
            M{aff.max_affordable_loan:,.0f}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs: Charts | Products | Schedule | Tips ─────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Repayment Breakdown",
        "🏦 Loan Products",
        "📅 Payment Schedule",
        "💡 Tips",
    ])

    # ── Tab 1: Repayment breakdown pie chart ─────────────────────
    with tab1:
        col_chart, col_summary = st.columns([1, 1])

        with col_chart:
            fig = go.Figure(go.Pie(
                labels    = ['Principal', 'Total Interest'],
                values    = [loan_amount, sim.total_interest],
                hole      = 0.55,
                marker    = dict(colors=[
                    COLORS['accent'], COLORS['warning']
                ]),
                textinfo  = 'label+percent',
                textfont  = dict(size=12),
            ))
            fig.update_layout(
                height          = 280,
                margin          = dict(t=20, b=20, l=20, r=20),
                paper_bgcolor   = 'rgba(0,0,0,0)',
                showlegend      = False,
                annotations     = [dict(
                    text      = f"M{sim.total_repayable:,.0f}",
                    x=0.5, y=0.5,
                    font_size = 16,
                    font_color= COLORS['primary'],
                    showarrow = False,
                )],
            )
            st.plotly_chart(fig, use_container_width=True,
                            config={'displayModeBar': False})

        with col_summary:
            rows = [
                ("Loan Amount",     f"M{loan_amount:,.0f}"),
                ("Term",            f"{loan_term} months"),
                ("Interest Rate",   f"{sim.effective_rate}% p.a."),
                ("Monthly Payment", f"M{sim.monthly_payment:,.0f}"),
                ("Total Interest",  f"M{sim.total_interest:,.0f}"),
                ("Total Repayable", f"M{sim.total_repayable:,.0f}"),
            ]
            for label, value in rows:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between;
                            padding:0.5rem 0;
                            border-bottom:1px solid {COLORS['border']};">
                    <span style="color:#6B7280;
                                 font-size:0.88rem;">{label}</span>
                    <span style="font-weight:700;
                                 color:{COLORS['primary']};
                                 font-size:0.92rem;">{value}</span>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: Loan products ──────────────────────────────────────
    with tab2:
        st.markdown("##### Products you qualify for based on your "
                    "score and requested amount")
        for product in sim.eligible_products:
            bg    = '#E8F5E9' if product.eligible else '#FAFAFA'
            color = COLORS['success'] if product.eligible \
                    else COLORS['muted']
            st.markdown(f"""
            <div class="fs-card" style="background:{bg};
                 border-left:4px solid {color};
                 margin-bottom:0.6rem;">
                <div style="display:flex;
                            justify-content:space-between;
                            align-items:flex-start;">
                    <div>
                        <div style="font-weight:700;
                                    font-size:0.98rem;
                                    color:{COLORS['primary']};">
                            {product.name}
                        </div>
                        <div style="font-size:0.8rem;
                                    color:#6B7280; margin:0.2rem 0;">
                            {product.provider}
                        </div>
                        <div style="font-size:0.82rem;
                                    color:{color};">
                            {product.reason}
                        </div>
                    </div>
                    <div style="text-align:right; min-width:120px;">
                        <div style="font-size:1.1rem; font-weight:800;
                                    color:{COLORS['primary']};">
                            {product.interest_rate}%
                        </div>
                        <div style="font-size:0.75rem;
                                    color:#6B7280;">per year</div>
                        <div style="font-size:0.85rem;
                                    font-weight:600;
                                    color:{COLORS['primary']};
                                    margin-top:0.3rem;">
                            M{product.monthly_payment:,.0f}/mo
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Amortisation schedule ──────────────────────────────
    with tab3:
        st.markdown("##### First 12 months of repayment")
        rows = []
        for s in sim.schedule:
            rows.append({
                "Month":     s.month,
                "Payment":   f"M{s.payment:,.2f}",
                "Principal": f"M{s.principal:,.2f}",
                "Interest":  f"M{s.interest:,.2f}",
                "Balance":   f"M{s.balance:,.2f}",
            })
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        # Balance over time line chart
        balance_data = pd.DataFrame([
            {"Month": s.month, "Remaining Balance": s.balance}
            for s in sim.schedule
        ])
        fig2 = px.line(
            balance_data, x="Month", y="Remaining Balance",
            title="Loan Balance Over Time",
            color_discrete_sequence=[COLORS['accent']],
        )
        fig2.update_layout(
            height        = 220,
            margin        = dict(t=40, b=20, l=10, r=10),
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor  = 'rgba(0,0,0,0)',
            yaxis         = dict(gridcolor=COLORS['border']),
            xaxis         = dict(gridcolor=COLORS['border']),
        )
        st.plotly_chart(fig2, use_container_width=True,
                        config={'displayModeBar': False})

    # ── Tab 4: Tips ───────────────────────────────────────────────
    with tab4:
        for tip in sim.tips:
            st.markdown(f"""
            <div class="fs-card" style="margin-bottom:0.6rem;
                 font-size:0.92rem; line-height:1.7;
                 color:{COLORS['text']};">
                {tip}
            </div>
            """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;'>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to My Score", use_container_width=True):
            st.session_state['page'] = 'results'
            st.rerun()
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()