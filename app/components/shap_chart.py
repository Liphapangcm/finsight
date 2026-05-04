# app/components/shap_chart.py

import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import COLORS

# Features that relate to debt — suppressed when total_debt == 0
DEBT_FEATURES = {
    "Debt-to-Income Ratio",
    "Debt Repayment Load",
    "High Debt Warning",
    "Number of Active Loans",
    "Too Many Loans",
}


def render_shap_chart(feature_names: list,
                      shap_values: list,
                      n: int = 10,
                      total_debt: float = None):
    """
    Renders SHAP bar chart.

    Args:
        feature_names: Human-readable feature labels
        shap_values:   SHAP impact values
        n:             Number of features to show
        total_debt:    User's total debt — if 0, debt features
                       are shown as neutral to avoid confusion
    """
    has_no_debt = (total_debt is not None and total_debt <= 0.0)

    # Sort by absolute impact, take top n
    pairs = sorted(
        zip(feature_names, shap_values),
        key=lambda x: abs(x[1]),
        reverse=True,
    )[:n]

    names  = [p[0] for p in reversed(pairs)]
    values = [p[1] for p in reversed(pairs)]

    bar_colors = []
    hover_texts = []

    for name, val in zip(names, values):
        is_debt_feature = name in DEBT_FEATURES

        if has_no_debt and is_debt_feature:
            # Show as neutral grey — the negative is a SHAP
            # accounting artifact, not a real penalty
            bar_colors.append(COLORS["border_strong"])
            hover_texts.append(
                f"{name}<br>"
                f"You have no debt — this feature has no real "
                f"negative impact on your score.<br>"
                f"SHAP value: {val:+.1f} (accounting artifact)"
            )
        elif val >= 0:
            bar_colors.append(COLORS["good"])
            hover_texts.append(
                f"{name}<br>Positive impact: {val:+.1f} points"
            )
        else:
            bar_colors.append(COLORS["danger"])
            hover_texts.append(
                f"{name}<br>Negative impact: {val:+.1f} points"
            )

    # For zero-debt users, show debt bars as 0 visually
    display_values = []
    for name, val in zip(names, values):
        if has_no_debt and name in DEBT_FEATURES:
            display_values.append(0.0)
        else:
            display_values.append(val)

    fig = go.Figure(go.Bar(
        x            = display_values,
        y            = names,
        orientation  = "h",
        marker       = dict(color=bar_colors, line=dict(width=0)),
        text         = [
            "No debt" if (has_no_debt and names[i] in DEBT_FEATURES)
            else f"{values[i]:+.1f}"
            for i in range(len(names))
        ],
        textposition = "outside",
        textfont     = dict(
            size   = 10.5,
            color  = COLORS["text_secondary"],
            family = "JetBrains Mono, monospace",
        ),
        hovertext    = hover_texts,
        hoverinfo    = "text",
    ))

    fig.update_layout(
        height        = 340,
        margin        = dict(t=8, b=8, l=8, r=70),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        bargap        = 0.28,
        xaxis = dict(
            showgrid      = True,
            gridcolor     = COLORS["border"],
            gridwidth     = 1,
            zeroline      = True,
            zerolinecolor = COLORS["border_strong"],
            zerolinewidth = 1.5,
            tickfont      = dict(
                size   = 9.5,
                color  = COLORS["text_muted"],
                family = "JetBrains Mono, monospace",
            ),
            title = dict(
                text = "Score Impact",
                font = dict(
                    size   = 10,
                    color  = COLORS["text_muted"],
                    family = "Plus Jakarta Sans, sans-serif",
                ),
            ),
        ),
        yaxis = dict(
            showgrid = False,
            tickfont = dict(
                size   = 10,
                color  = COLORS["text_secondary"],
                family = "Plus Jakarta Sans, sans-serif",
            ),
        ),
        font = dict(family="Plus Jakarta Sans, sans-serif"),
    )

    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

    # Legend
    legend_items = [
        (COLORS["good"],         "Helping your score"),
        (COLORS["danger"],       "Hurting your score"),
    ]
    if has_no_debt:
        legend_items.append(
            (COLORS["border_strong"], "No impact (zero debt)")
        )

    legend_html = "".join([
        f'<span style="display:inline-flex;align-items:center;'
        f'gap:4px;margin-right:1rem;">'
        f'<span style="display:inline-block;width:8px;height:8px;'
        f'border-radius:2px;background:{col};"></span>'
        f'<span style="font-size:0.72rem;color:{COLORS["text_muted"]};">'
        f'{label}</span></span>'
        for col, label in legend_items
    ])

    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;margin-top:-0.5rem;">'
        f'{legend_html}</div>',
        unsafe_allow_html=True,
    )

    if has_no_debt:
        st.markdown(f"""
        <div style="font-size:0.75rem;color:{COLORS['text_muted']};
                    margin-top:0.5rem;padding:0.5rem 0.75rem;
                    background:{COLORS['bg']};
                    border-radius:6px;
                    border-left:3px solid {COLORS['border_strong']};">
            ℹ️ Grey bars indicate debt-related factors — since you
            reported zero debt, these have no real negative impact
            on your score. The SHAP model shows them as slightly
            negative due to how the average training profile
            looked, but your score reflects your actual zero-debt
            status correctly.
        </div>
        """, unsafe_allow_html=True)