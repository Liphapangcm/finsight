# app/components/kpi_cards.py
import streamlit as st
from core.schemas import FinancialKPIs


def render_kpi_cards(kpis: FinancialKPIs):
    """
    Renders a row of 3 KPI metric cards.
    """
    col1, col2, col3 = st.columns(3)

    # ── Card 1: Debt-to-Income ────────────────────────────────────
    dti   = kpis.debt_to_income
    d_cls = ("kpi-positive" if dti < 35
             else "kpi-neutral" if dti < 50
             else "kpi-negative")
    d_txt = ("Healthy" if dti < 35
             else "Moderate" if dti < 50
             else "High Risk")

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{dti:.1f}%</div>
            <div class="kpi-label">Debt-to-Income</div>
            <div class="kpi-delta {d_cls}">{d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Card 2: Savings Rate ──────────────────────────────────────
    sr    = kpis.savings_rate
    s_cls = ("kpi-positive" if sr >= 10
             else "kpi-neutral" if sr >= 3
             else "kpi-negative")
    s_txt = ("Strong" if sr >= 10
             else "Low" if sr >= 3
             else "None")

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{sr:.1f}%</div>
            <div class="kpi-label">Savings Rate</div>
            <div class="kpi-delta {s_cls}">{s_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Card 3: Monthly Cash Flow ─────────────────────────────────
    flow  = kpis.net_cash_flow
    f_cls = "kpi-positive" if flow >= 0 else "kpi-negative"
    f_pfx = "+" if flow >= 0 else ""
    f_txt = "Surplus" if flow >= 0 else "Deficit ⚠️"

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">M{f_pfx}{flow:,.0f}</div>
            <div class="kpi-label">Monthly Cash Flow</div>
            <div class="kpi-delta {f_cls}">{f_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Secondary row: Expense Ratio ──────────────────────────────
    st.markdown("<div style='margin-top:0.8rem;'></div>",
                unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    exp_ratio = kpis.expense_ratio
    e_cls = ("kpi-positive" if exp_ratio < 70
             else "kpi-neutral" if exp_ratio < 90
             else "kpi-negative")

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{exp_ratio:.1f}%</div>
            <div class="kpi-label">Expense Ratio</div>
            <div class="kpi-delta {e_cls}">
                {'Healthy' if exp_ratio < 70
                 else 'Watch This' if exp_ratio < 90
                 else 'Too High'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">M{kpis.monthly_income:,.0f}</div>
            <div class="kpi-label">Monthly Income</div>
            <div class="kpi-delta kpi-neutral">Reported</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">M{kpis.total_expenses:,.0f}</div>
            <div class="kpi-label">Total Expenses</div>
            <div class="kpi-delta {e_cls}">Per Month</div>
        </div>
        """, unsafe_allow_html=True)