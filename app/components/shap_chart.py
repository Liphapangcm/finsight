# app/components/shap_chart.py
import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import COLORS


def render_shap_chart(feature_names: list, shap_values: list, n: int = 10):
    pairs  = sorted(zip(feature_names, shap_values),
                    key=lambda x: abs(x[1]), reverse=True)[:n]
    names  = [p[0] for p in reversed(pairs)]
    values = [p[1] for p in reversed(pairs)]

    colors = []
    for v in values:
        if v >= 0:
            # Teal gradient for positive
            intensity = min(abs(v) / 60, 1)
            colors.append(f"rgba(0,212,170,{0.4 + intensity*0.6})")
        else:
            # Red gradient for negative
            intensity = min(abs(v) / 60, 1)
            colors.append(f"rgba(255,77,106,{0.4 + intensity*0.6})")

    fig = go.Figure(go.Bar(
        x            = values,
        y            = names,
        orientation  = 'h',
        marker       = dict(
            color         = colors,
            line          = dict(width=0),
        ),
        text         = [f"{v:+.1f}" for v in values],
        textposition = 'outside',
        textfont     = dict(
            size  = 11,
            color = COLORS['text_secondary'],
            family= 'Space Grotesk, sans-serif',
        ),
    ))

    fig.update_layout(
        height        = 360,
        margin        = dict(t=10, b=10, l=10, r=50),
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor  = 'rgba(0,0,0,0)',
        xaxis         = dict(
            showgrid      = True,
            gridcolor     = 'rgba(255,255,255,0.04)',
            gridwidth     = 1,
            zeroline      = True,
            zerolinecolor = 'rgba(255,255,255,0.1)',
            zerolinewidth = 1,
            tickfont      = dict(
                size   = 10,
                color  = COLORS['text_muted'],
                family = 'JetBrains Mono, monospace',
            ),
            title         = dict(
                text = "Score Impact",
                font = dict(
                    size   = 10,
                    color  = COLORS['text_muted'],
                    family = 'Space Grotesk, sans-serif',
                ),
            ),
        ),
        yaxis         = dict(
            showgrid  = False,
            tickfont  = dict(
                size   = 10,
                color  = COLORS['text_secondary'],
                family = 'Space Grotesk, sans-serif',
            ),
        ),
        font          = dict(family='Space Grotesk, sans-serif'),
        bargap        = 0.25,
    )

    st.plotly_chart(fig, use_container_width=True,
                    config={'displayModeBar': False})

    st.markdown(f"""
    <div style="display:flex; gap:1rem; font-size:0.72rem;
                color:{COLORS['text_muted']}; margin-top:-0.8rem;">
        <span style="color:rgba(0,212,170,0.8);">
            ● Helping your score
        </span>
        <span style="color:rgba(255,77,106,0.8);">
            ● Hurting your score
        </span>
    </div>
    """, unsafe_allow_html=True)