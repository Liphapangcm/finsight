import streamlit as st
from core.schemas import Recommendation
from app.styles.theme import COLORS


def render_recommendations(recommendations: list[Recommendation]):
    st.markdown("""
    <div style="font-size:0.8rem; color:#4A5578;
                margin-bottom:0.8rem; line-height:1.6;">
        Address in order — Priority 1 has the biggest score impact.
    </div>
    """, unsafe_allow_html=True)

    cards_html = ""
    for rec in recommendations:
        cat_class = f"cat-{rec.category}"
        cards_html += f"""
        <div class="rec-card">
            <div style="display:flex; align-items:center;
                        margin-bottom:0.4rem;">
                <span class="rec-number">{rec.priority}</span>
                <span class="rec-title">{rec.title}</span>
                <span class="rec-category {cat_class}">
                    {rec.category.upper()}
                </span>
            </div>
            <div class="rec-desc">{rec.description}</div>
            <div class="rec-impact">{rec.impact_estimate}</div>
        </div>
        """

    st.markdown(cards_html, unsafe_allow_html=True)