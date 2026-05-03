import streamlit as st
from core.schemas import FinancialKPIs
from app.styles.theme import COLORS


def render_kpi_cards(kpis: FinancialKPIs):
    dti  = kpis.debt_to_income
    sr   = kpis.savings_rate
    flow = kpis.net_cash_flow
    exp  = kpis.expense_ratio

    def _badge(cls, label):
        return (f'<div class="metric-badge {cls}">{label}</div>')

    dti_badge  = (_badge("b-good",  "Healthy")  if dti  < 35 else
                  _badge("b-warn",  "Moderate") if dti  < 50 else
                  _badge("b-bad",   "High Risk"))
    sr_badge   = (_badge("b-good",  "Strong")   if sr   >= 10 else
                  _badge("b-warn",  "Low")       if sr   >= 3  else
                  _badge("b-bad",   "None"))
    flow_badge = (_badge("b-good",  "Surplus")  if flow >= 0  else
                  _badge("b-bad",   "Deficit ⚠"))
    exp_badge  = (_badge("b-good",  "Healthy")  if exp  < 70  else
                  _badge("b-warn",  "Elevated") if exp  < 90  else
                  _badge("b-bad",   "High"))

    flow_sign = "+" if flow >= 0 else ""
    flow_color = COLORS["good"] if flow >= 0 else COLORS["danger"]

    cards = [
        ("DEBT-TO-INCOME",
         f"{dti:.1f}%",         COLORS["navy"], dti_badge),
        ("SAVINGS RATE",
         f"{sr:.1f}%",          COLORS["navy"], sr_badge),
        (f"MONTHLY CASH FLOW",
         f"M{flow_sign}{flow:,.0f}", flow_color, flow_badge),
        ("EXPENSE RATIO",
         f"{exp:.1f}%",         COLORS["navy"], exp_badge),
        ("MONTHLY INCOME",
         f"M{kpis.monthly_income:,.0f}", COLORS["navy"],
         _badge("b-info", "Reported")),
        ("TOTAL EXPENSES",
         f"M{kpis.total_expenses:,.0f}", COLORS["navy"],
         exp_badge),
    ]

    html = '<div class="metric-grid">'
    for label, value, color, badge in cards:
        html += f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value"
                 style="color:{color};">{value}</div>
            {badge}
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)