# app/pages/landing.py
"""
Landing page — fixes:
- Stats strip now responsive (stacks on mobile)
- Uses stats-strip CSS class defined in theme
"""
import streamlit as st
from app.styles.theme import COLORS


def render_landing():
    # ── Hero ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding:3rem 0 2.5rem;text-align:center;">
        <div style="display:inline-flex;align-items:center;gap:0.5rem;
                    font-size:0.72rem;font-weight:700;letter-spacing:1.2px;
                    text-transform:uppercase;color:{COLORS['blue']};
                    background:{COLORS['blue_light']};
                    border:1px solid {COLORS['blue_mid']};
                    border-radius:100px;padding:0.3rem 0.9rem;
                    margin-bottom:1.5rem;">
            Free · Instant · Private
        </div>
        <h1 style="font-family:'Plus Jakarta Sans',sans-serif;
                   font-size:2.6rem;font-weight:800;
                   color:{COLORS['navy']};letter-spacing:-1.5px;
                   line-height:1.12;margin-bottom:1rem;">
            Understand Your<br/>
            <span style="color:{COLORS['blue']};">Financial Health</span>
        </h1>
        <p style="font-size:1rem;color:{COLORS['text_secondary']};
                  max-width:460px;margin:0 auto 2.5rem;
                  line-height:1.8;font-weight:400;">
            FinSight analyses your income, expenses, and financial
            behaviour to produce a personalised credit score — with
            a clear, prioritised plan to improve it.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1.4, 1.5, 1.4])
    with col2:
        if st.button("Get My Credit Score →",
                     key="hero_cta", use_container_width=True):
            st.session_state['page'] = 'assessment'
            st.rerun()

    st.markdown(f"""
    <div style="text-align:center;margin-top:0.6rem;margin-bottom:2.5rem;
                font-size:0.76rem;color:{COLORS['text_muted']};">
        🔒 Your data is never stored or shared
    </div>
    """, unsafe_allow_html=True)

    # ── Stats strip — responsive via CSS class ────────────────────
    st.markdown(f"""
    <div class="stats-strip">
        <div class="stats-cell">
            <div class="stats-num">3 min</div>
            <div class="stats-desc">Average completion</div>
        </div>
        <div class="stats-cell">
            <div class="stats-num">20+</div>
            <div class="stats-desc">Factors analysed</div>
        </div>
        <div class="stats-cell">
            <div class="stats-num">100%</div>
            <div class="stats-desc">Free, always</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-size:0.7rem;font-weight:700;color:{COLORS['text_muted']};
                text-transform:uppercase;letter-spacing:1px;
                margin-bottom:0.9rem;">How it works</div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Enter Your Details",
         "Fill in your income, expenses, and debt. "
         "No bank login or ID required.",
         COLORS["blue"]),
        ("02", "AI Scores Your Profile",
         "Our ML model analyses 20+ financial factors "
         "to produce your personalised credit score.",
         COLORS["teal"]),
        ("03", "Get Your Score & Plan",
         "See your score, every contributing factor, "
         "and a ranked action plan to improve.",
         COLORS["navy"]),
    ]
    cols = st.columns(3)
    for col, (num, title, desc, accent) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="fs-card" style="min-height:155px;">
                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:0.62rem;font-weight:600;
                            color:{accent};letter-spacing:1.5px;
                            margin-bottom:0.75rem;">STEP {num}</div>
                <div style="font-weight:700;font-size:0.92rem;
                            color:{COLORS['navy']};margin-bottom:0.5rem;">
                    {title}
                </div>
                <div style="font-size:0.82rem;color:{COLORS['text_secondary']};
                            line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>",
                unsafe_allow_html=True)

    # ── Score bands ───────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-size:0.7rem;font-weight:700;color:{COLORS['text_muted']};
                text-transform:uppercase;letter-spacing:1px;
                margin-bottom:0.9rem;">Credit score bands</div>
    """, unsafe_allow_html=True)

    bands = [
        ("300–449", "Poor",      COLORS["poor"],
         COLORS["danger_light"],
         "High risk. Focus on clearing defaults first."),
        ("450–579", "Fair",      COLORS["fair"],
         COLORS["warning_light"],
         "Below average. Payment habits improve quickly."),
        ("580–699", "Good",      COLORS["good"],
         COLORS["success_light"],
         "Solid. Qualifies for most credit products."),
        ("700–850", "Excellent", COLORS["excellent"],
         COLORS["teal_light"],
         "Best rates. Top-tier financial standing."),
    ]
    cols = st.columns(4)
    for col, (rng, label, color, bg, desc) in zip(cols, bands):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {color}30;
                        border-radius:9px;padding:1.1rem 1rem;
                        min-height:125px;transition:transform 0.2s;
                        cursor:default;">
                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:0.8rem;font-weight:600;
                            color:{color};margin-bottom:0.3rem;">{rng}</div>
                <div style="font-weight:800;color:{color};
                            font-size:0.95rem;margin-bottom:0.5rem;">
                    {label}
                </div>
                <div style="font-size:0.77rem;color:{COLORS['text_secondary']};
                            line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem;'></div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.4, 1.5, 1.4])
    with col2:
        if st.button("Start Free Assessment →",
                     key="bottom_cta", use_container_width=True):
            st.session_state['page'] = 'assessment'
            st.rerun()