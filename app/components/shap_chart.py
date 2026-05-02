import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import COLORS


def render_shap_chart(feature_names: list, shap_values: list, n: int = 10):
    """
    Renders a horizontal bar chart of SHAP values.
    Green bars = factors helping the score.
    Red bars   = factors hurting the score.
    Shows top N features by absolute impact.
    """
    # Take top N by absolute value
    pairs  = sorted(zip(feature_names, shap_values),
                    key=lambda x: abs(x[1]), reverse=True)[:n]
    names  = [p[0] for p in reversed(pairs)]
    values = [p[1] for p in reversed(pairs)]
    colors = [COLORS['success'] if v >= 0 else COLORS['danger']
              for v in values]

    fig = go.Figure(go.Bar(
        x           = values,
        y           = names,
        orientation = 'h',
        marker_color= colors,
        text        = [f"{v:+.1f}" for v in values],
        textposition= 'outside',
        textfont    = {'size': 11, 'color': COLORS['text']},
    ))

    fig.update_layout(
        title       = dict(
            text    = "What's Affecting Your Score",
            font    = {'size': 15, 'color': COLORS['primary'],
                       'family': 'Inter, sans-serif'},
            x       = 0,
        ),
        height      = 380,
        margin      = dict(t=50, b=20, l=10, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor ='rgba(0,0,0,0)',
        xaxis       = dict(
            showgrid     = True,
            gridcolor    = COLORS['border'],
            zeroline     = True,
            zerolinecolor= COLORS['muted'],
            zerolinewidth= 1.5,
            title        = "Impact on Score",
            titlefont    = {'size': 11},
        ),
        yaxis       = dict(
            showgrid     = False,
            tickfont     = {'size': 11, 'color': COLORS['text']},
        ),
        font        = {'family': 'Inter, sans-serif'},
    )

    st.plotly_chart(fig, use_container_width=True,
                    config={'displayModeBar': False})

    st.markdown("""
    <div style="font-size:0.78rem; color:#6B7280; margin-top:-1rem;">
        🟢 Green = helping your score &nbsp;&nbsp;
        🔴 Red = hurting your score
    </div>
    """, unsafe_allow_html=True)