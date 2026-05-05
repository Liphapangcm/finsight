import streamlit as st
from core.schemas import FinancialKPIs
from app.styles.theme import COLORS


def render_kpi_cards(kpis: FinancialKPIs, show_drilldown: bool = True):
    """
    Renders interactive KPI cards with animations and drill-down capabilities.
    
    Args:
        kpis: Financial KPIs data
        show_drilldown: Whether to show detailed info on click
    """
    dti = max(kpis.debt_to_income, 0)
    sr = max(kpis.savings_rate, 0)
    flow = kpis.net_cash_flow
    exp = kpis.expense_ratio
    
    # Industry benchmarks for comparison
    benchmarks = {
        "dti": {"good": 35, "average": 43, "poor": 50},
        "savings": {"good": 20, "average": 10, "poor": 5},
        "expense": {"good": 50, "average": 70, "poor": 85},
    }
    
    def _get_trend(metric_type: str, value: float):
        """Calculate trend vs benchmark"""
        if metric_type == "dti":
            if value <= benchmarks["dti"]["good"]:
                return ("📈", "Excellent", COLORS["success"])
            elif value <= benchmarks["dti"]["average"]:
                return ("📊", "Average", COLORS["warning"])
            else:
                return ("📉", "Needs Work", COLORS["danger"])
        elif metric_type == "savings":
            if value >= benchmarks["savings"]["good"]:
                return ("🚀", "Excellent", COLORS["success"])
            elif value >= benchmarks["savings"]["average"]:
                return ("📈", "Good", COLORS["info"])
            else:
                return ("⚠️", "Low", COLORS["warning"])
        elif metric_type == "expense":
            if value <= benchmarks["expense"]["good"]:
                return ("✅", "Great", COLORS["success"])
            elif value <= benchmarks["expense"]["average"]:
                return ("📊", "Moderate", COLORS["warning"])
            else:
                return ("⚠️", "High", COLORS["danger"])
        return ("•", "Info", COLORS["muted"])
    
    def _badge(cls, label, icon=""):
        return f'<div class="metric-badge {cls}">{icon} {label}</div>'
    
    def _tooltip(text):
        return f'<span class="tooltip-icon" title="{text}">ⓘ</span>'
    
    # Generate badges with trends
    if dti == 0:
        dti_badge = _badge("b-good", "No Debt", "✅")
        dti_trend = ("🎉", "Perfect", COLORS["success"])
    elif dti < 35:
        dti_badge = _badge("b-good", "Healthy", "✅")
        dti_trend = _get_trend("dti", dti)
    elif dti < 50:
        dti_badge = _badge("b-warn", "Moderate", "⚠️")
        dti_trend = _get_trend("dti", dti)
    else:
        dti_badge = _badge("b-bad", "High Risk", "🔴")
        dti_trend = _get_trend("dti", dti)
    
    if sr == 0:
        sr_badge = _badge("b-bad", "None", "❌")
        sr_trend = ("⚠️", "Critical", COLORS["danger"])
    elif sr < 3:
        sr_badge = _badge("b-bad", "Very Low", "⚠️")
        sr_trend = _get_trend("savings", sr)
    elif sr < 10:
        sr_badge = _badge("b-warn", "Low", "📊")
        sr_trend = _get_trend("savings", sr)
    else:
        sr_badge = _badge("b-good", "Strong", "💪")
        sr_trend = _get_trend("savings", sr)
    
    flow_badge = (
        _badge("b-good", "Surplus", "✅") if flow >= 0 else _badge("b-bad", "Deficit", "⚠️")
    )
    
    if exp < 70:
        exp_badge = _badge("b-good", "Healthy", "✅")
        exp_trend = _get_trend("expense", exp)
    elif exp < 90:
        exp_badge = _badge("b-warn", "Elevated", "⚠️")
        exp_trend = _get_trend("expense", exp)
    else:
        exp_badge = _badge("b-bad", "High", "🔴")
        exp_trend = _get_trend("expense", exp)
    
    flow_sign = "+" if flow >= 0 else ""
    flow_color = COLORS["good"] if flow >= 0 else COLORS["danger"]
    
    # Create progress bar for DTI
    dti_progress = min(100, (dti / 60) * 100)  # Max DTI considered is 60%
    dti_progress_color = COLORS["success"] if dti < 35 else (COLORS["warning"] if dti < 50 else COLORS["danger"])
    
    # Create progress bar for Savings Rate
    sr_progress = min(100, (sr / 25) * 100)  # 25% savings rate is excellent
    sr_progress_color = COLORS["success"] if sr >= 20 else (COLORS["warning"] if sr >= 10 else COLORS["danger"])
    
    # Create progress bar for Expense Ratio (inverted - lower is better)
    exp_progress = min(100, exp)
    exp_progress_color = COLORS["success"] if exp < 70 else (COLORS["warning"] if exp < 85 else COLORS["danger"])
    
    cards = [
        {
            "label": "DEBT-TO-INCOME",
            "value": f"{dti:.1f}%",
            "color": COLORS["navy"],
            "badge": dti_badge,
            "trend": dti_trend,
            "tooltip": "Total monthly debt payments divided by monthly income. Lower is better.",
            "progress": dti_progress,
            "progress_color": dti_progress_color,
            "progress_label": f"Target: <{benchmarks['dti']['good']}%",
            "detail": f"Your DTI of {dti:.1f}% means {dti:.1f}% of your income goes to debt. Ideally keep below 35%."
        },
        {
            "label": "SAVINGS RATE",
            "value": f"{sr:.1f}%",
            "color": COLORS["navy"],
            "badge": sr_badge,
            "trend": sr_trend,
            "tooltip": "Percentage of income saved each month. Aim for 20% or more.",
            "progress": sr_progress,
            "progress_color": sr_progress_color,
            "progress_label": f"Target: {benchmarks['savings']['good']}%+",
            "detail": f"You save {sr:.1f}% of your income. Financial experts recommend saving 20% or more."
        },
        {
            "label": "MONTHLY CASH FLOW",
            "value": f"M{flow_sign}{flow:,.0f}",
            "color": flow_color,
            "badge": flow_badge,
            "trend": None,
            "tooltip": "Income minus expenses. Positive cash flow means you're living within your means.",
            "progress": None,
            "detail": f"Your cash flow is {flow_sign}M{abs(flow):,.0f} per month. {'Great job!' if flow >= 0 else 'Consider reducing expenses or increasing income.'}"
        },
        {
            "label": "EXPENSE RATIO",
            "value": f"{exp:.1f}%",
            "color": COLORS["navy"],
            "badge": exp_badge,
            "trend": exp_trend,
            "tooltip": "Percentage of income spent on expenses. Lower is better.",
            "progress": exp_progress,
            "progress_color": exp_progress_color,
            "progress_label": f"Target: <{benchmarks['expense']['good']}%",
            "detail": f"You spend {exp:.1f}% of your income on expenses. Aim to keep below 50% for financial freedom."
        },
        {
            "label": "MONTHLY INCOME",
            "value": f"M{kpis.monthly_income:,.0f}",
            "color": COLORS["navy"],
            "badge": _badge("b-info", "Reported", "💰"),
            "trend": None,
            "tooltip": "Total monthly income after taxes",
            "progress": None,
            "detail": f"Your monthly income is M{kpis.monthly_income:,.0f}. Consider ways to increase this through side hustles or career growth."
        },
        {
            "label": "TOTAL EXPENSES",
            "value": f"M{kpis.total_expenses:,.0f}",
            "color": COLORS["navy"],
            "badge": exp_badge,
            "trend": None,
            "tooltip": "Total monthly spending across all categories",
            "progress": None,
            "detail": f"Your monthly expenses are M{kpis.total_expenses:,.0f}. Review the breakdown to identify savings opportunities."
        },
    ]
    
    # Add custom CSS for enhanced cards
    st.markdown(f"""
    <style>
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin: 1rem 0;
        }}
        
        .metric-card {{
            background: white;
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #E5E7EB;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['accent']});
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0,0,0,0.15);
            border-color: transparent;
        }}
        
        .metric-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .metric-label {{
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            color: #6B7280;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .metric-badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }}
        
        .b-good {{
            background: #E8F5E9;
            color: #2E7D32;
        }}
        
        .b-warn {{
            background: #FFF3E0;
            color: #E65100;
        }}
        
        .b-bad {{
            background: #FFEBEE;
            color: #C62828;
        }}
        
        .b-info {{
            background: #E3F2FD;
            color: #1565C0;
        }}
        
        .trend-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.7rem;
            padding: 0.2rem 0.5rem;
            border-radius: 20px;
            background: #F9FAFB;
        }}
        
        .progress-bar-container {{
            margin-top: 0.75rem;
            margin-bottom: 0.5rem;
        }}
        
        .progress-bar {{
            height: 6px;
            background: #E5E7EB;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.5s ease;
        }}
        
        .progress-label {{
            font-size: 0.65rem;
            color: #6B7280;
            margin-top: 0.25rem;
            display: flex;
            justify-content: space-between;
        }}
        
        .tooltip-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #E5E7EB;
            color: #6B7280;
            font-size: 10px;
            cursor: help;
            margin-left: 0.25rem;
            transition: all 0.2s ease;
        }}
        
        .tooltip-icon:hover {{
            background: {COLORS['primary']};
            color: white;
            transform: scale(1.1);
        }}
        
        .drilldown-detail {{
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid #E5E7EB;
            font-size: 0.75rem;
            color: #6B7280;
            display: none;
        }}
        
        .metric-card.active .drilldown-detail {{
            display: block;
        }}
        
        @media (max-width: 640px) {{
            .metric-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}
            .metric-value {{
                font-size: 1.4rem;
            }}
        }}
    </style>
    
    <script>
    // JavaScript for card click handling with session storage
    document.addEventListener('DOMContentLoaded', function() {{
        const cards = document.querySelectorAll('.metric-card');
        cards.forEach((card, index) => {{
            card.addEventListener('click', function(e) {{
                // Don't trigger if clicking on tooltip
                if (e.target.classList.contains('tooltip-icon')) return;
                
                // Toggle active class
                this.classList.toggle('active');
                
                // Store in session storage
                const activeCards = JSON.parse(sessionStorage.getItem('activeMetricCards') || '[]');
                if (this.classList.contains('active')) {{
                    if (!activeCards.includes(index)) activeCards.push(index);
                }} else {{
                    const pos = activeCards.indexOf(index);
                    if (pos > -1) activeCards.splice(pos, 1);
                }}
                sessionStorage.setItem('activeMetricCards', JSON.stringify(activeCards));
            }});
            
            // Restore active state from session storage
            const activeCards = JSON.parse(sessionStorage.getItem('activeMetricCards') || '[]');
            if (activeCards.includes(index)) {{
                card.classList.add('active');
            }}
        }});
    }})();
    </script>
    """, unsafe_allow_html=True)
    
    # Generate HTML for cards
    html = '<div class="metric-grid">'
    for idx, card in enumerate(cards):
        trend_html = ""
        if card["trend"]:
            trend_icon, trend_label, trend_color = card["trend"]
            trend_html = f'<div class="trend-indicator" style="color: {trend_color};">{trend_icon} {trend_label}</div>'
        
        progress_html = ""
        if card["progress"] is not None:
            progress_html = f'''
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {card['progress']}%; background: {card['progress_color']};"></div>
                </div>
                <div class="progress-label">
                    <span>{card['progress_label']}</span>
                    <span>{card['progress']:.0f}%</span>
                </div>
            </div>
            '''
        
        html += f"""
        <div class="metric-card" data-card-idx="{idx}">
            <div class="metric-label">
                {card['label']}
                {_tooltip(card['tooltip'])}
            </div>
            <div class="metric-value" style="color:{card['color']};">{card['value']}</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                {card['badge']}
                {trend_html}
            </div>
            {progress_html}
            <div class="drilldown-detail">
                💡 <strong>Insight:</strong> {card.get('detail', 'Click for more information')}
            </div>
        </div>"""
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Optional: Add summary recommendation
    if show_drilldown:
        st.markdown(f"""
        <div style="background: {COLORS['primary']}08;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-top: 1rem;
                    border-left: 3px solid {COLORS['primary']};">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">📊</span>
                <span style="font-weight: 600; color: {COLORS['primary']};">Quick Summary</span>
            </div>
            <div style="font-size: 0.85rem; color: #6B7280; margin-top: 0.5rem;">
                {"✅ Your DTI is healthy! Keep debt manageable." if dti < 35 else "⚠️ Your DTI is high. Focus on debt reduction."}
                {" 💪 Great savings discipline!" if sr >= 20 else " 🎯 Try to increase your savings rate."}
                {" 💰 Positive cash flow is excellent!" if flow >= 0 else " 📉 Your expenses exceed income. Create a budget."}
            </div>
        </div>
        """, unsafe_allow_html=True)