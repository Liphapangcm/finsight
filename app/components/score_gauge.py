import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import SCORE_COLORS, COLORS


def render_score_gauge(score: int, band: str, risk_level: str):
    """
    Renders a professional credit score gauge chart.
    """
    band_color = SCORE_COLORS.get(band, COLORS["accent"])

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "font": {
                    "size": 64,
                    "color": band_color,
                    "family": "Inter, sans-serif",
                },
                "suffix": "",
            },
            gauge={
                "axis": {
                    "range": [300, 850],
                    "tickwidth": 1,
                    "tickcolor": COLORS["muted"],
                    "tickvals": [300, 450, 580, 700, 850],
                    "ticktext": ["300", "450", "580", "700", "850"],
                    "tickfont": {"size": 11, "color": COLORS["muted"]},
                },
                "bar": {"color": band_color, "thickness": 0.25},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [300, 450], "color": "#FFEBEE"},
                    {"range": [450, 580], "color": "#FFF3E0"},
                    {"range": [580, 700], "color": "#E8F5E9"},
                    {"range": [700, 850], "color": "#E0F2F1"},
                ],
                "threshold": {
                    "line": {"color": band_color, "width": 4},
                    "thickness": 0.8,
                    "value": score,
                },
            },
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )

    fig.update_layout(
        height=280,
        margin=dict(t=40, b=0, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
    )

    # Band label below chart
    badge_class = f"badge-{band.lower()}"
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        f"""
    <div style="text-align:center; margin-top:-1rem; margin-bottom:1rem;">
        <span class="score-badge {badge_class}">{band.upper()}</span>
        <div style="color:#6B7280; font-size:0.82rem; margin-top:0.4rem;">
            Risk Level: <strong>{risk_level}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
