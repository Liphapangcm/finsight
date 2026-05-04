# app/components/shap_chart.py
"""
SHAP Chart — fixes:
- Debt-related features no longer show misleading negatives
  when user has zero debt (filtered from display if near-zero impact)
- Clean professional bar chart
"""

import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import COLORS


def render_shap_chart(feature_names: list, shap_values: list, n: int = 10):
    # Pair and sort by absolute impact; filter out near-zero impacts
    # to avoid misleading negative bars for zero debt / strong financial state
    pairs = [
        (name, val)
        for name, val in zip(feature_names, shap_values)
        if abs(val) > 0.1  # threshold: ignore impacts < 0.1 points
    ]
    pairs = sorted(
        pairs,
        key=lambda x: abs(x[1]),
        reverse=True,
    )[:n]

    names = [p[0] for p in reversed(pairs)]
    values = [p[1] for p in reversed(pairs)]

    bar_colors = [COLORS["good"] if v >= 0 else COLORS["danger"] for v in values]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=names,
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:+.1f}" for v in values],
            textposition="outside",
            textfont=dict(
                size=10.5,
                color=COLORS["text_secondary"],
                family="JetBrains Mono, monospace",
            ),
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(t=8, b=8, l=8, r=55),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        bargap=0.28,
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS["border"],
            gridwidth=1,
            zeroline=True,
            zerolinecolor=COLORS["border_strong"],
            zerolinewidth=1.5,
            tickfont=dict(
                size=9.5,
                color=COLORS["text_muted"],
                family="JetBrains Mono, monospace",
            ),
            title=dict(
                text="Score Impact",
                font=dict(
                    size=10,
                    color=COLORS["text_muted"],
                    family="Plus Jakarta Sans, sans-serif",
                ),
            ),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(
                size=10,
                color=COLORS["text_secondary"],
                family="Plus Jakarta Sans, sans-serif",
            ),
        ),
        font=dict(family="Plus Jakarta Sans, sans-serif"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        f"""
    <div style="display:flex;gap:1.25rem;font-size:0.72rem;
                color:{COLORS["text_muted"]};margin-top:-0.5rem;">
        <span style="display:flex;align-items:center;gap:4px;">
            <span style="display:inline-block;width:8px;height:8px;
                         border-radius:2px;
                         background:{COLORS["good"]};"></span>
            Positive impact
        </span>
        <span style="display:flex;align-items:center;gap:4px;">
            <span style="display:inline-block;width:8px;height:8px;
                         border-radius:2px;
                         background:{COLORS["danger"]};"></span>
            Negative impact
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )
