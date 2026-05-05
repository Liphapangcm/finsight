import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from app.styles.theme import COLORS
from core.loan_simulator import simulate_loan


def _c(key: str, fallback: str = "#0A1F44") -> str:
    """Safe color getter — never raises KeyError."""
    return COLORS.get(key, fallback)


def render_loan_simulator():
    result = st.session_state.get('result')

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div class="fs-page-title">
            <span style="background: linear-gradient(135deg, {_c('blue')}, {_c('teal')});
                         -webkit-background-clip: text;
                         -webkit-text-fill-color: transparent;">
                🏦 Loan Eligibility Simulator
            </span>
        </div>
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

    # ── Current financial summary card ──
    with st.expander("📊 Your Current Financial Snapshot", expanded=False):
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("Credit Score", f"{result.credit_score}/850", 
                     delta="Excellent" if result.credit_score >= 750 else None)
        with col_b:
            st.metric("Monthly Income", f"M{result.kpis.monthly_income:,.0f}")
        with col_c:
            st.metric("Monthly Expenses", f"M{result.kpis.total_expenses:,.0f}")
        with col_d:
            st.metric("DTI Ratio", f"{result.kpis.debt_to_income:.1f}%",
                     delta="Good" if result.kpis.debt_to_income < 35 else "High",
                     delta_color="inverse" if result.kpis.debt_to_income >= 35 else "normal")

    # ── Loan inputs with real-time feedback ──
    st.markdown(
        '<div class="section-label">Configure Your Loan</div>',
        unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Animated loan amount slider
        loan_amount = st.slider(
            "💰 Loan Amount (LSL — Maloti)",
            min_value=1_000.0, 
            max_value=500_000.0,
            value=st.session_state.get("sim_loan_amount", 20_000.0),
            step=5_000.0,
            format="M%.0f",
            help="Higher amounts may affect approval probability"
        )
        st.session_state["sim_loan_amount"] = loan_amount
        
        # Show quick amount suggestions
        st.caption("💡 Quick suggestions: 💰 10k  💰 25k  💰 50k  💰 100k")
        
    with col2:
        loan_term = st.slider(
            "📅 Repayment Term (months)",
            min_value=3, 
            max_value=84, 
            value=st.session_state.get("sim_loan_term", 24),
            step=3,
            help="Longer terms mean lower monthly payments but more interest"
        )
        st.session_state["sim_loan_term"] = loan_term
        
        # Term visualization
        years = loan_term // 12
        months = loan_term % 12
        term_text = f"{years} yr {months} mo" if years > 0 else f"{months} mo"
        st.caption(f"Term length: {term_text}")

    # Add interest rate based on credit score
    if result.credit_score >= 750:
        base_rate = 8.5
        rate_badge = "🏆 Excellent rate"
        rate_color = _c('success')
    elif result.credit_score >= 700:
        base_rate = 11.0
        rate_badge = "👍 Good rate"
        rate_color = _c('info')
    elif result.credit_score >= 650:
        base_rate = 14.5
        rate_badge = "📊 Standard rate"
        rate_color = _c('warning')
    elif result.credit_score >= 580:
        base_rate = 18.0
        rate_badge = "⚠️ Higher rate"
        rate_color = _c('danger')
    else:
        base_rate = 22.0
        rate_badge = "🔴 Limited options"
        rate_color = _c('danger')
    
    st.info(f"💡 **Your estimated interest rate: {base_rate}%** ({rate_badge}) based on your credit score of {result.credit_score}")

    # ── Derive simulation inputs from result ──
    income         = result.kpis.monthly_income
    total_expenses = result.kpis.total_expenses
    savings        = max(0.0, result.kpis.savings_rate / 100 * income)
    total_debt     = max(0.0, result.kpis.debt_to_income / 100 * income)
    has_defaulted  = any(
        "default" in r.title.lower()
        for r in result.recommendations
    )

    # Show loading animation on input change
    with st.spinner("Calculating loan options..."):
        time.sleep(0.1)  # Small delay for UX
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

    # ── Enhanced Summary KPI row with animations ──
    prob_pct  = int(sim.approval_probability * 100)
    appr_color= sim.approval_color

    # Create animated progress bar for approval probability
    st.markdown(f"""
    <style>
        @keyframes fillProgress {{
            from {{ width: 0%; }}
            to {{ width: {prob_pct}%; }}
        }}
        .prob-bar-fill {{
            animation: fillProgress 1.2s ease-out forwards;
        }}
    </style>
    """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    
    with k1:
        st.markdown(f"""
        <div class="metric-card" style="border-top:3px solid {appr_color};">
            <div class="metric-label">🎯 Approval Probability</div>
            <div class="metric-value" style="color:{appr_color};">{prob_pct}%</div>
            <div class="metric-badge b-info">{sim.approval_label}</div>
            <div class="progress-bar-container" style="margin-top: 0.5rem;">
                <div class="progress-bar">
                    <div class="progress-fill prob-bar-fill" 
                         style="width: {prob_pct}%; background: {appr_color};"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k2:
        a_cls = "b-good" if sim.affordability.is_affordable else "b-bad"
        a_lbl = "✅ Affordable" if sim.affordability.is_affordable else "⚠️ Too High"
        
        # Calculate DTI after loan
        new_monthly_payment = sim.monthly_payment
        current_dti = (total_debt / income * 100) if income > 0 else 0
        new_dti = ((total_debt + new_monthly_payment) / income * 100) if income > 0 else 0
        dti_change = new_dti - current_dti
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Monthly Payment</div>
            <div class="metric-value">M{sim.monthly_payment:,.0f}</div>
            <div class="metric-badge {a_cls}">{a_lbl}</div>
            <div style="font-size: 0.7rem; margin-top: 0.35rem; color: {_c('text_muted')};">
                {'📈' if dti_change > 0 else '📉'} DTI +{dti_change:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k3:
        interest_savings = base_rate * loan_amount / 100 * (loan_term / 12)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💸 Total Interest Cost</div>
            <div class="metric-value">M{sim.total_interest:,.0f}</div>
            <div class="metric-badge b-info">{sim.effective_rate}% APR</div>
            <div style="font-size: 0.7rem; margin-top: 0.35rem; color: {_c('warning')};">
                ~M{sim.total_interest / max(loan_term, 1):,.0f}/month in interest
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Enhanced Affordability alert with visual gauge ──
    aff   = sim.affordability
    a_col = _c('success') if aff.is_affordable else _c('danger')
    a_bg  = _c('success_light') if aff.is_affordable else _c('danger_light')
    
    # Calculate affordability percentage
    affordability_percent = (sim.monthly_payment / aff.max_affordable_monthly * 100) if aff.max_affordable_monthly > 0 else 0
    gauge_color = _c('success') if affordability_percent <= 70 else (_c('warning') if affordability_percent <= 90 else _c('danger'))
    
    st.markdown(f"""
    <div style="background:{a_bg};border-radius:12px;
                padding:1rem 1.2rem;margin:1rem 0;
                border-left:4px solid {a_col};
                transition: all 0.3s ease;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1;">
                <strong style="color:{a_col}; font-size: 1rem;">
                    {aff.affordability_message}
                </strong><br/>
                <span style="font-size:0.78rem;color:{_c('text_secondary')};">
                    Max affordable monthly payment: <strong>M{aff.max_affordable_monthly:,.0f}</strong><br/>
                    Max affordable loan at this term: <strong>M{aff.max_affordable_loan:,.0f}</strong>
                </span>
            </div>
            <div style="min-width: 150px;">
                <div style="font-size: 0.7rem; color: {_c('text_muted')}; margin-bottom: 0.25rem;">Affordability Gauge</div>
                <div class="progress-bar" style="height: 8px;">
                    <div class="progress-fill" style="width: {min(100, affordability_percent)}%; background: {gauge_color}; transition: width 0.5s ease;"></div>
                </div>
                <div style="font-size: 0.7rem; text-align: right; margin-top: 0.25rem; color: {gauge_color};">
                    {affordability_percent:.0f}% of affordable limit
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Add Score Impact Prediction ──
    st.markdown("---")
    st.markdown("### 📈 Expected Credit Score Impact")
    
    # Simulate score impact based on loan performance
    if prob_pct >= 70:
        impact = "+15 to +25"
        impact_color = _c('success')
        impact_icon = "📈"
    elif prob_pct >= 40:
        impact = "+5 to +15"
        impact_color = _c('info')
        impact_icon = "📊"
    else:
        impact = "-10 to +5"
        impact_color = _c('warning')
        impact_icon = "⚠️"
    
    col_impact1, col_impact2, col_impact3 = st.columns(3)
    with col_impact1:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <div style="font-size: 2rem;">{impact_icon}</div>
            <div style="font-size: 0.7rem; color: {_c('text_muted')};">Expected Change</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: {impact_color};">{impact}</div>
            <div style="font-size: 0.65rem;">points in 6-12 months</div>
        </div>
        """, unsafe_allow_html=True)
    with col_impact2:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <div style="font-size: 2rem;">✅</div>
            <div style="font-size: 0.7rem; color: {_c('text_muted')};">On-time Payments</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: {_c('success')};">+10 to +20</div>
            <div style="font-size: 0.65rem;">per year of good history</div>
        </div>
        """, unsafe_allow_html=True)
    with col_impact3:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <div style="font-size: 2rem;">⚠️</div>
            <div style="font-size: 0.7rem; color: {_c('text_muted')};">Late Payments</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: {_c('danger')};">-50 to -100</div>
            <div style="font-size: 0.65rem;">per missed payment</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tabs with enhanced content ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Repayment Breakdown",
        "🏦 Loan Products",
        "📅 Payment Schedule",
        "📉 Compare Scenarios",
        "💡 Smart Tips",
    ])

    with tab1:
        c_chart, c_summary = st.columns([1, 1])
        with c_chart:
            # Enhanced donut chart with better styling
            fig = go.Figure(go.Pie(
                labels   = ['Principal', 'Total Interest'],
                values   = [loan_amount, sim.total_interest],
                hole     = 0.6,
                marker   = dict(colors=[_c('blue'), _c('warning')],
                               line=dict(color='white', width=2)),
                textinfo = 'label+percent',
                textfont = dict(size=12, color='white'),
                pull     = [0, 0.05],  # Slightly pull interest slice
            ))
            fig.update_layout(
                height        = 300,
                margin        = dict(t=40, b=20, l=20, r=20),
                paper_bgcolor = 'rgba(0,0,0,0)',
                showlegend    = False,
                annotations   = [dict(
                    text       = f"Total<br>M{sim.total_repayable:,.0f}",
                    x=0.5, y=0.5,
                    font_size  = 13,
                    font_color = _c('navy'),
                    font_weight = 'bold',
                    showarrow  = False,
                )],
            )
            st.plotly_chart(fig, use_container_width=True,
                            config={'displayModeBar': False})

        with c_summary:
            # Add payment ratio visualization
            principal_ratio = (loan_amount / sim.total_repayable * 100) if sim.total_repayable > 0 else 0
            
            rows = [
                ("Loan Amount",     f"M{loan_amount:,.0f}", f"{principal_ratio:.0f}% of total"),
                ("Term",            f"{loan_term} months", term_text),
                ("Interest Rate",   f"{sim.effective_rate}% APR", f"{100-principal_ratio:.0f}% of total"),
                ("Monthly Payment", f"M{sim.monthly_payment:,.0f}", f"~M{sim.monthly_payment * 12:,.0f}/year"),
                ("Total Interest",  f"M{sim.total_interest:,.0f}", f"M{sim.total_interest / max(loan_term, 1):,.0f}/month"),
                ("Total Repayable", f"M{sim.total_repayable:,.0f}", f"{100-principal_ratio:.1f}% interest"),
            ]
            for lbl, val, sub in rows:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;
                            align-items: center;
                            padding:0.6rem 0;
                            border-bottom:1px solid {_c('border')};">
                    <span style="color:{_c('text_secondary')};
                                 font-size:0.85rem;">{lbl}</span>
                    <div style="text-align: right;">
                        <span style="font-weight:700;color:{_c('navy')};
                                     font-size:0.88rem;
                                     font-family:'JetBrains Mono',monospace;">
                            {val}
                        </span>
                        <div style="font-size:0.65rem; color:{_c('text_muted')};">{sub}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div style="font-size:0.8rem;color:{_c('text_muted')};
                    margin-bottom:1rem;">
            💡 Products matching your score of {result.credit_score} and requested amount.
        </div>
        """, unsafe_allow_html=True)
        
        for idx, product in enumerate(sim.eligible_products):
            bg     = _c('success_light') if product.eligible else _c('bg')
            border = _c('success') if product.eligible else _c('border')
            label_color = _c('success') if product.eligible else _c('text_muted')
            
            # Add delay animation for each product
            delay = idx * 0.1
            st.markdown(f"""
            <style>
                @keyframes slideIn{idx} {{
                    from {{ opacity: 0; transform: translateX(-20px); }}
                    to {{ opacity: 1; transform: translateX(0); }}
                }}
                .product-card-{idx} {{
                    animation: slideIn{idx} 0.3s ease-out {delay}s both;
                }}
            </style>
            <div class="fs-card product-card-{idx}"
                 style="background:{bg};
                        border-left:3px solid {border};
                        margin-bottom:0.8rem;
                        transition: all 0.3s ease;">
                <div style="display:flex;justify-content:space-between;
                            align-items:center; flex-wrap: wrap; gap: 1rem;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                            <span style="font-weight:800;font-size:0.95rem;
                                        color:{_c('navy')};">
                                {product.name}
                            </span>
                            {f'<span style="background:{_c("success")}20; color:{_c("success")}; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.65rem; font-weight:600;">✓ Recommended</span>' if product.eligible and idx == 0 else ''}
                        </div>
                        <div style="font-size:0.75rem;
                                    color:{_c('text_muted')};
                                    margin:0.3rem 0;">
                            {product.provider}
                        </div>
                        <div style="font-size:0.8rem;
                                    color:{label_color};
                                    margin-top: 0.25rem;">
                            {product.reason}
                        </div>
                    </div>
                    <div style="text-align:right; min-width:120px;">
                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:1.2rem;font-weight:700;
                                    color:{_c('navy')};">
                            {product.interest_rate}%
                        </div>
                        <div style="font-size:0.68rem;
                                    color:{_c('text_muted')};">
                            APR
                        </div>
                        <div style="font-size:0.9rem;font-weight:600;
                                    color:{_c('navy')};margin-top:5px;">
                            M{product.monthly_payment:,.0f}<span style="font-size:0.7rem;">/mo</span>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 0.75rem;">
                    <button onclick="alert('Application started for {product.name}')" 
                            style="background: {border}; color: white; border: none; 
                                   padding: 0.25rem 1rem; border-radius: 5px; 
                                   font-size: 0.7rem; cursor: pointer;">
                        Apply Now →
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("##### 📅 Amortization Schedule (First 12 months)")
        
        # Create enhanced dataframe with better formatting
        schedule_df = pd.DataFrame([{
            "Month":     s.month,
            "Payment":   f"M{s.payment:,.0f}",
            "Principal": f"M{s.principal:,.0f}",
            "Interest":  f"M{s.interest:,.0f}",
            "Balance":   f"M{s.balance:,.0f}",
            "Principal %": f"{(s.principal / s.payment * 100):.0f}%" if s.payment > 0 else "0%",
        } for s in sim.schedule[:12]])
        
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        
        # Add download button for full schedule
        full_schedule_df = pd.DataFrame([{
            "Month": s.month,
            "Payment": s.payment,
            "Principal": s.principal,
            "Interest": s.interest,
            "Remaining Balance": s.balance,
        } for s in sim.schedule])
        
        csv = full_schedule_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Full Payment Schedule (CSV)",
            data=csv,
            file_name=f"loan_schedule_{loan_amount:,.0f}_{loan_term}m.csv",
            mime="text/csv",
            use_container_width=True,
        )
        
        # Enhanced balance chart
        fig2 = px.area(
            pd.DataFrame([
                {"Month": s.month, "Remaining Balance": s.balance}
                for s in sim.schedule
            ]),
            x="Month", y="Remaining Balance",
            title="Loan Balance Amortization Over Time",
            color_discrete_sequence=[_c('blue')],
        )
        fig2.update_layout(
            height        = 260,
            margin        = dict(t=50, b=20, l=10, r=10),
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor  = 'rgba(0,0,0,0)',
            yaxis         = dict(gridcolor=_c('border'), title="Balance (LSL)"),
            xaxis         = dict(gridcolor=_c('border'), title="Month"),
            hovermode     = 'x unified',
        )
        fig2.update_traces(fill='tozeroy', opacity=0.7)
        st.plotly_chart(fig2, use_container_width=True,
                        config={'displayModeBar': False})

    with tab4:
        st.markdown("##### 🔄 Compare Loan Scenarios")
        
        # Add comparison sliders
        col_comp1, col_comp2 = st.columns(2)
        with col_comp1:
            alt_amount = st.number_input(
                "Alternative Loan Amount",
                min_value=1_000.0,
                max_value=500_000.0,
                value=min(loan_amount * 1.5, 500_000),
                step=5_000.0,
                format="%.0f",
                key="alt_amount"
            )
        with col_comp2:
            alt_term = st.slider(
                "Alternative Term (months)",
                min_value=3,
                max_value=84,
                value=min(loan_term + 12, 84),
                step=6,
                key="alt_term"
            )
        
        if st.button("🔄 Compare Scenarios", use_container_width=True):
            alt_sim = simulate_loan(
                loan_amount=alt_amount,
                loan_term=alt_term,
                credit_score=result.credit_score,
                monthly_income=income,
                total_expenses=total_expenses,
                monthly_savings=savings,
                total_debt=total_debt,
                has_defaulted=has_defaulted,
            )
            
            # Create comparison chart
            comp_data = pd.DataFrame({
                'Metric': ['Monthly Payment', 'Total Interest', 'Total Repayable'],
                'Current': [sim.monthly_payment, sim.total_interest, sim.total_repayable],
                'Alternative': [alt_sim.monthly_payment, alt_sim.total_interest, alt_sim.total_repayable],
            })
            
            fig_comp = px.bar(comp_data, x='Metric', y=['Current', 'Alternative'],
                             title='Loan Scenario Comparison',
                             barmode='group',
                             color_discrete_sequence=[_c('blue'), _c('teal')])
            fig_comp.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Amount (LSL)",
            )
            st.plotly_chart(fig_comp, use_container_width=True,
                           config={'displayModeBar': False})
            
            # Show recommendation
            if alt_sim.monthly_payment < sim.monthly_payment:
                st.success(f"✅ Alternative scenario saves M{sim.monthly_payment - alt_sim.monthly_payment:,.0f}/month!")
            elif alt_sim.total_interest < sim.total_interest:
                st.info(f"💡 Alternative scenario saves M{sim.total_interest - alt_sim.total_interest:,.0f} in total interest")

    with tab5:
        # Enhanced tips with categories
        tip_categories = {
            "💰 Financial": [],
            "📊 Credit Score": [],
            "⚡ Quick Wins": []
        }
        
        for tip in sim.tips:
            if any(word in tip.lower() for word in ['save', 'budget', 'emergency', 'expense']):
                tip_categories["💰 Financial"].append(tip)
            elif any(word in tip.lower() for word in ['score', 'credit', 'payment', 'default']):
                tip_categories["📊 Credit Score"].append(tip)
            else:
                tip_categories["⚡ Quick Wins"].append(tip)
        
        for category, tips in tip_categories.items():
            if tips:
                st.markdown(f"##### {category}")
                for tip in tips:
                    st.markdown(f"""
                    <div class="fs-card"
                         style="margin-bottom:0.6rem;
                                font-size:0.88rem;
                                line-height:1.7;
                                background: linear-gradient(135deg, {_c('bg_white')}, {_c('bg')});">
                        💡 {tip}
                    </div>
                    """, unsafe_allow_html=True)

    # ── Enhanced Navigation ──
    st.markdown("<div style='margin-top:1.5rem;'>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("← Back to My Score", use_container_width=True):
            st.session_state['page'] = 'results'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with nav2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with nav3:
        if st.button("📤 Share Quote", use_container_width=True):
            st.toast("Quote copied to clipboard! 📋", icon="✅")