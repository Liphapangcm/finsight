import streamlit as st
from core.schemas import Recommendation
from app.styles.theme import COLORS


def render_recommendations(recommendations: list[Recommendation]):
    st.markdown(f"""
    <div style="font-size:0.78rem;color:{COLORS['text_muted']};
                margin-bottom:0.9rem;line-height:1.6;">
        Ranked by impact — address Priority 1 first for the
        fastest score improvement.
    </div>
    """, unsafe_allow_html=True)

    html = ""
    for rec in recommendations:
        tag_class = f"tag-{rec.category}"
        html += f"""
        <div class="rec-item">
            <div class="rec-num">{rec.priority}</div>
            <div class="rec-body">
                <div class="rec-title-row">
                    {rec.title}
                    <span class="rec-tag {tag_class}">
                        {rec.category}
                    </span>
                </div>
                <div class="rec-desc">{rec.description}</div>
                <div class="rec-impact">{rec.impact_estimate}</div>
            </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)