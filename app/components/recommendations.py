import streamlit as st
from core.schemas import Recommendation


def render_recommendations(recommendations: list[Recommendation]):
    """Renders styled recommendation cards."""

    st.markdown("""
    <div style="font-size:1.1rem; font-weight:700;
                color:#0B1F3A; margin-bottom:1rem;">
        📋 Your Action Plan
    </div>
    <div style="font-size:0.85rem; color:#6B7280; margin-bottom:1rem;">
        Address these in order — Priority 1 will have the biggest impact
        on your score.
    </div>
    """, unsafe_allow_html=True)

    for rec in recommendations:
        cat_class = f"cat-{rec.category}"
        cat_label = rec.category.upper()

        st.markdown(f"""
        <div class="rec-card">
            <div>
                <span class="rec-priority">{rec.priority}</span>
                <span class="rec-title">{rec.title}</span>
                <span class="rec-category {cat_class}">{cat_label}</span>
            </div>
            <div class="rec-description">{rec.description}</div>
            <div class="rec-impact">🎯 Estimated impact: {rec.impact_estimate}</div>
        </div>
        """, unsafe_allow_html=True)