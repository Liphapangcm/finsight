import streamlit as st
from core.schemas import FinancialKPIs
from app.styles.theme import COLORS


def render_kpi_cards(kpis: FinancialKPIs):
    dti  = kpis.debt_to_income
    sr   = kpis.savings_rate
    flow = kpis.net_cash_flow
    exp  = kpis.expense_ratio

    def delta_class(val, good_threshold, warn_threshold, reverse=False):
        if not reverse:
            if val <= good_threshold: return "delta-good", "Healthy"
            if val <= warn_threshold: return "delta-warn", "Moderate"
            return "delta-bad", "High Risk"
        else:
            if val >= good_threshold: return "delta-good", "Strong"
            if val >= warn_threshold: return "delta-warn", "Low"
            return "delta-bad", "None"

    dti_cls, dti_lbl  = delta_class(dti, 35, 50)
    sr_cls,  sr_lbl   = delta_class(sr,  10,  3, reverse=True)
    exp_cls, exp_lbl  = delta_class(exp, 70, 90)

    flow_cls   = "delta-good" if flow >= 0 else "delta-bad"
    flow_lbl   = "Surplus" if flow >= 0 else "Deficit ⚠"
    flow_prefix= "+" if flow >= 0 else ""

    cards = [
        {
            "value": f"{dti:.1f}%",
            "label": "Debt-to-Income",
            "delta_cls": dti_cls,
            "delta_lbl": dti_lbl,
        },
        {
            "value": f"{sr:.1f}%",
            "label": "Savings Rate",
            "delta_cls": sr_cls,
            "delta_lbl": sr_lbl,
        },
        {
            "value": f"M{flow_prefix}{flow:,.0f}",
            "label": "Monthly Cash Flow",
            "delta_cls": flow_cls,
            "delta_lbl": flow_lbl,
        },
        {
            "value": f"{exp:.1f}%",
            "label": "Expense Ratio",
            "delta_cls": exp_cls,
            "delta_lbl": exp_lbl,
        },
        {
            "value": f"M{kpis.monthly_income:,.0f}",
            "label": "Monthly Income",
            "delta_cls": "delta-neutral",
            "delta_lbl": "Reported",
        },
        {
            "value": f"M{kpis.total_expenses:,.0f}",
            "label": "Total Expenses",
            "delta_cls": exp_cls,
            "delta_lbl": "Per Month",
        },
    ]

    # Render as 3-column grid via HTML
    cards_html = '<div class="kpi-grid">'
    for card in cards:
        cards_html += f"""
        <div class="kpi-card">
            <div class="kpi-value">{card['value']}</div>
            <div class="kpi-label">{card['label']}</div>
            <div class="kpi-delta {card['delta_cls']}">
                {card['delta_lbl']}
            </div>
        </div>
        """
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)