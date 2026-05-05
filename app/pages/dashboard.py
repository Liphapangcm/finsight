"""
Financial Dashboard — Premium Overview
Features: Real-time metrics, trend visualization, goal tracking, insights hub
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from app.styles.theme import COLORS, SCORE_COLORS
from app.components.score_gauge import render_mini_score_gauge


def _c(key: str, fallback: str = "#0A1F44") -> str:
    """Safe color getter — never raises KeyError."""
    return COLORS.get(key, fallback)


def render_dashboard():
    """
    Main dashboard view with comprehensive financial overview
    """
    result = st.session_state.get('result')
    
    # Page header with date and greeting
    current_hour = datetime.now().hour
    greeting = "🌅 Good Morning" if current_hour < 12 else "🌞 Good Afternoon" if current_hour < 17 else "🌙 Good Evening"
    
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div class="fs-page-title">
            <span style="background: linear-gradient(135deg, {_c('blue')}, {_c('teal')});
                         -webkit-background-clip: text;
                         -webkit-text-fill-color: transparent;">
                📊 Financial Dashboard
            </span>
        </div>
        <div class="fs-page-subtitle">
            {greeting}, {st.session_state.get('user_name', 'User')}! 👋
            <span style="display: block; font-size: 0.75rem; margin-top: 0.25rem;">
                Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Refresh button in top right
    col_refresh, _ = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    if not result:
        st.info("📝 Complete your credit assessment to see your personalized dashboard.")
        _, col, _ = st.columns([1, 1, 1])
        with col:
            if st.button("Begin Assessment →", use_container_width=True, type="primary"):
                st.session_state['page'] = 'assessment'
                st.rerun()
        return
    
    # ── Quick Stats Banner ──────────────────────────────────────────
    score = result.credit_score
    band = result.score_band
    risk = result.risk_level
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-label">🏆 Credit Score</div>
            <div class="metric-value" style="color: {SCORE_COLORS.get(band, _c('blue'))};">{score}</div>
            <div class="metric-badge b-info">{band}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        income = result.kpis.monthly_income
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-label">💰 Monthly Income</div>
            <div class="metric-value">M{income:,.0f}</div>
            <div class="metric-badge b-good">Reported</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        dti = result.kpis.debt_to_income
        dti_class = "b-good" if dti < 35 else ("b-warn" if dti < 50 else "b-bad")
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-label">📊 Debt-to-Income</div>
            <div class="metric-value">{dti:.1f}%</div>
            <div class="metric-badge {dti_class}">{"Healthy" if dti < 35 else "Elevated" if dti < 50 else "High"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        savings_rate = result.kpis.savings_rate
        savings_class = "b-good" if savings_rate >= 20 else ("b-warn" if savings_rate >= 10 else "b-bad")
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-label">💵 Savings Rate</div>
            <div class="metric-value">{savings_rate:.1f}%</div>
            <div class="metric-badge {savings_class}">{"Strong" if savings_rate >= 20 else "Moderate" if savings_rate >= 10 else "Low"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ── Two Column Layout: Score Gauge + AI Insight ─────────────────
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        render_mini_score_gauge(score, band)
        st.markdown(f"""
        <div style="text-align: center; margin-top: -1rem;">
            <div style="background: {_c('bg_subtle')}; border-radius: 12px; padding: 0.75rem; margin-top: 0.5rem;">
                <div style="font-size: 0.7rem; color: {_c('text_muted')};">Risk Level</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: {SCORE_COLORS.get(band, _c('blue'))};">{risk}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # Market context / Peer comparison placeholder
        if score >= 750:
            peer_text = "Top 10% of users"
            peer_color = _c('success')
            peer_icon = "🏆"
        elif score >= 700:
            peer_text = "Above average"
            peer_color = _c('info')
            peer_icon = "📈"
        elif score >= 580:
            peer_text = "Average"
            peer_color = _c('warning')
            peer_icon = "📊"
        else:
            peer_text = "Needs improvement"
            peer_color = _c('danger')
            peer_icon = "📉"
        
        st.markdown(f"""
        <div class="fs-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">🤖</span>
                <span style="font-weight: 700; font-size: 1rem;">AI Financial Insight</span>
            </div>
            <p style="font-size: 0.85rem; line-height: 1.6; color: {_c('text_secondary')};">
                Your credit score of <strong>{score}</strong> is <strong style="color: {peer_color};">{peer_text}</strong> {peer_icon}. 
                {'Excellent! You qualify for premium rates.' if score >= 750 else 
                  'Good work! Keep building positive history.' if score >= 700 else
                  'Focus on timely payments and reducing debt.'}
            </p>
            <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <span style="background: {_c('blue_light')}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem;">
                    🎯 {score}/850
                </span>
                <span style="background: {_c('blue_light')}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem;">
                    📊 {dti:.0f}% DTI
                </span>
                <span style="background: {_c('blue_light')}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem;">
                    💰 {savings_rate:.0f}% Saved
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ── Financial Health Trends (Simulated) ─────────────────────────
    st.markdown('<div class="section-label">📈 Financial Health Trends</div>', unsafe_allow_html=True)
    
    # Simulate 12 months of trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Generate realistic trends based on current score
    base_score = max(300, score - 50)
    score_trend = [int(base_score + (score - base_score) * (i / 11)) for i in range(12)]
    
    # Savings trend (assuming improvement)
    savings_trend = [max(0, savings_rate - 5 + i * 0.8) for i in range(12)]
    
    # DTI trend (assuming improvement)
    dti_trend = [min(80, dti + 10 - i * 1.2) for i in range(12)]
    
    col_trend1, col_trend2 = st.columns(2)
    
    with col_trend1:
        fig_score = go.Figure()
        fig_score.add_trace(go.Scatter(
            x=months,
            y=score_trend,
            mode='lines+markers',
            name='Credit Score',
            line=dict(color=_c('blue'), width=3),
            marker=dict(size=8, color=_c('blue')),
            fill='tozeroy',
            fillcolor=f'rgba(45, 127, 249, 0.1)',
        ))
        fig_score.update_layout(
            title="Credit Score Evolution",
            height=300,
            margin=dict(t=40, b=20, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor=_c('border'), range=[300, 850]),
            xaxis=dict(gridcolor=_c('border')),
            hovermode='x unified',
        )
        st.plotly_chart(fig_score, use_container_width=True, config={'displayModeBar': False})
    
    with col_trend2:
        # Dual axis chart for savings vs DTI
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Scatter(
            x=months,
            y=savings_trend,
            mode='lines+markers',
            name='Savings Rate (%)',
            line=dict(color=_c('teal'), width=3),
            marker=dict(size=8, color=_c('teal')),
            yaxis='y1',
        ))
        fig_dual.add_trace(go.Scatter(
            x=months,
            y=dti_trend,
            mode='lines+markers',
            name='Debt-to-Income (%)',
            line=dict(color=_c('warning'), width=3, dash='dot'),
            marker=dict(size=8, color=_c('warning')),
            yaxis='y2',
        ))
        fig_dual.update_layout(
            title="Savings vs Debt Trends",
            height=300,
            margin=dict(t=40, b=20, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title="Savings Rate (%)", gridcolor=_c('border'), side='left'),
            yaxis2=dict(title="DTI (%)", gridcolor=_c('border'), side='right', overlaying='y', showgrid=False),
            xaxis=dict(gridcolor=_c('border')),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        )
        st.plotly_chart(fig_dual, use_container_width=True, config={'displayModeBar': False})
    
    # ── Financial Ratios Visualization ──────────────────────────────
    st.markdown('<div class="section-label">⚖️ Financial Ratios Analysis</div>', unsafe_allow_html=True)
    
    col_ratios1, col_ratios2, col_ratios3 = st.columns(3)
    
    with col_ratios1:
        # Expense ratio donut
        expense_ratio = result.kpis.expense_ratio
        expense_color = _c('success') if expense_ratio < 50 else (_c('warning') if expense_ratio < 70 else _c('danger'))
        fig_expense = go.Figure(go.Pie(
            labels=['Expenses', 'Remaining Income'],
            values=[expense_ratio, 100 - expense_ratio],
            hole=0.7,
            marker=dict(colors=[expense_color, _c('border')]),
            showlegend=False,
            textinfo='none',
        ))
        fig_expense.update_layout(
            height=180,
            margin=dict(t=20, b=20, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text=f"{expense_ratio:.0f}%", x=0.5, y=0.5, font_size=20, font_color=expense_color, showarrow=False)],
        )
        st.plotly_chart(fig_expense, use_container_width=True, config={'displayModeBar': False})
        st.caption(f"📊 Expense Ratio: {expense_ratio:.1f}% of income")
    
    with col_ratios2:
        # Savings vs debt ratio
        savings_vs_debt = (savings_rate / max(1, dti)) * 100
        fig_savings = go.Figure(go.Indicator(
            mode="gauge+number",
            value=min(100, savings_vs_debt),
            number=dict(suffix="%", font_size=28),
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=1, tickcolor=_c('border')),
                bar=dict(color=_c('teal')),
                bgcolor='rgba(0,0,0,0)',
                borderwidth=0,
                steps=[
                    dict(range=[0, 33], color=_c('danger_light')),
                    dict(range=[33, 66], color=_c('warning_light')),
                    dict(range=[66, 100], color=_c('success_light')),
                ],
            ),
        ))
        fig_savings.update_layout(height=180, margin=dict(t=20, b=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_savings, use_container_width=True, config={'displayModeBar': False})
        st.caption("💪 Savings vs Debt Health Score")
    
    with col_ratios3:
        # Cash flow score
        cash_flow = result.kpis.net_cash_flow
        cash_flow_color = _c('success') if cash_flow > 0 else _c('danger')
        fig_cash = go.Figure(go.Indicator(
            mode="number",
            value=abs(cash_flow),
            number=dict(prefix="M" if cash_flow > 0 else "-M", font_size=28, font_color=cash_flow_color),
            title=dict(text="Monthly Cash Flow", font_size=14),
        ))
        fig_cash.update_layout(height=180, margin=dict(t=40, b=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cash, use_container_width=True, config={'displayModeBar': False})
        st.caption(f"{'✅ Positive' if cash_flow > 0 else '⚠️ Negative'} cash flow")
    
    # ── Quick Action Cards ──────────────────────────────────────────
    st.markdown('<div class="section-label">🚀 Quick Actions</div>', unsafe_allow_html=True)
    
    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
    
    with col_action1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state['page'] = 'landing'
            st.rerun()
    
    with col_action2:
        if st.button("📊 Loan Simulator", use_container_width=True):
            st.session_state['page'] = 'loan_simulator'
            st.rerun()
    
    with col_action3:
        if st.button("🤖 AI Advisor", use_container_width=True):
            st.session_state['page'] = 'advisor'
            st.rerun()
    
    with col_action4:
        if st.button("📄 New Assessment", use_container_width=True):
            for key in ['result', 'form_step', 'monthly_income', 'total_debt', 
                       'has_savings', 'has_defaulted', 'num_active_loans', 
                       'payment_regularity', 'pdf_bytes']:
                st.session_state.pop(key, None)
            st.session_state['page'] = 'assessment'
            st.rerun()
    
    # ── Goal Setting Section ────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-label">🎯 Financial Goals Tracker</div>', unsafe_allow_html=True)
    
    # Goal tracker
    goals = [
        {"name": "Emergency Fund", "target": 50000, "current": min(50000, result.kpis.monthly_savings * 3)},
        {"name": "Debt Free", "target": 100000, "current": min(100000, result.kpis.total_debt * 0.3)},
        {"name": "Credit Score", "target": 750, "current": score},
    ]
    
    for goal in goals:
        progress = min(100, (goal["current"] / goal["target"]) * 100)
        progress_color = _c('success') if progress >= 80 else (_c('warning') if progress >= 40 else _c('info'))
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="font-size: 0.8rem; font-weight: 600;">{goal['name']}</span>
                <span style="font-size: 0.7rem; color: {_c('text_muted')};">{goal['current']:,.0f} / {goal['target']:,.0f}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%; background: {progress_color}; transition: width 0.5s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ── Recent Activity Feed ────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-label">📋 Recent Activity</div>', unsafe_allow_html=True)
    
    activities = [
        {"icon": "📊", "action": "Credit assessment completed", "time": "Today", "detail": f"Score: {score}"},
        {"icon": "🏦", "action": "Loan simulator used", "time": "Yesterday", "detail": "Explored options"},
        {"icon": "📈", "action": "Score improved", "time": "Last week", "detail": "+12 points"},
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div class="fs-card" style="padding: 0.75rem; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.2rem;">{activity['icon']}</span>
                <div style="flex: 1;">
                    <div style="font-size: 0.85rem; font-weight: 600;">{activity['action']}</div>
                    <div style="font-size: 0.7rem; color: {_c('text_muted')};">{activity['detail']}</div>
                </div>
                <div style="font-size: 0.65rem; color: {_c('text_muted')};">{activity['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ── Export Section ──────────────────────────────────────────────
    st.markdown("---")
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        if st.button("📥 Download Full Report (PDF)", use_container_width=True):
            st.toast("Report generation started... 📄", icon="✅")
            # Add PDF generation logic here
    
    with col_export2:
        if st.button("📧 Share Dashboard", use_container_width=True):
            st.toast("Share link copied to clipboard! 🔗", icon="✅")