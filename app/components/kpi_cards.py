# app/components/kpi_cards.py
import streamlit as st
from core.schemas import FinancialKPIs
from app.styles.theme import COLORS


def render_kpi_cards(kpis: FinancialKPIs):
    dti  = max(kpis.debt_to_income, 0)
    sr   = max(kpis.savings_rate,   0)
    flow = kpis.net_cash_flow
    exp  = kpis.expense_ratio

    def _badge(cls, label):
        return f'<div class="metric-badge {cls}">{label}</div>'

    if dti == 0:
        dti_badge = _badge("b-good", "No Debt")
    elif dti < 35:
        dti_badge = _badge("b-good", "Healthy")
    elif dti < 50:
        dti_badge = _badge("b-warn", "Moderate")
    else:
        dti_badge = _badge("b-bad",  "High Risk")

    if sr == 0:
        sr_badge = _badge("b-bad",  "None")
    elif sr < 3:
        sr_badge = _badge("b-bad",  "Very Low")
    elif sr < 10:
        sr_badge = _badge("b-warn", "Low")
    else:
        sr_badge = _badge("b-good", "Strong")

    flow_badge = (_badge("b-good", "Surplus")
                  if flow >= 0 else _badge("b-bad", "Deficit ⚠"))

    if exp < 70:
        exp_badge = _badge("b-good", "Healthy")
    elif exp < 90:
        exp_badge = _badge("b-warn", "Elevated")
    else:
        exp_badge = _badge("b-bad", "High")

    flow_sign  = "+" if flow >= 0 else ""
    flow_color = COLORS["good"] if flow >= 0 else COLORS["danger"]

    cards = [
        ("DEBT-TO-INCOME",    f"{dti:.1f}%",
         COLORS["navy"],      dti_badge),
        ("SAVINGS RATE",      f"{sr:.1f}%",
         COLORS["navy"],      sr_badge),
        ("MONTHLY CASH FLOW", f"M{flow_sign}{flow:,.0f}",
         flow_color,          flow_badge),
        ("EXPENSE RATIO",     f"{exp:.1f}%",
         COLORS["navy"],      exp_badge),
        ("MONTHLY INCOME",    f"M{kpis.monthly_income:,.0f}",
         COLORS["navy"],      _badge("b-info", "Reported")),
        ("TOTAL EXPENSES",    f"M{kpis.total_expenses:,.0f}",
         COLORS["navy"],      exp_badge),
    ]

    html = '<div class="metric-grid">'
    for label, value, color, badge in cards:
        html += f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color};">{value}</div>
            {badge}
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
