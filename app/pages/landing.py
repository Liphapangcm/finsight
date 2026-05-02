# app/pages/landing.py
import streamlit as st
from app.styles.theme import COLORS


def render_landing():
    # ── Hero ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 3.5rem 1rem 2.5rem;">

        <div style="
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: {COLORS['primary']};
            background: rgba(0,212,170,0.08);
            border: 1px solid rgba(0,212,170,0.2);
            border-radius: 100px;
            padding: 0.35rem 1rem;
            margin-bottom: 1.8rem;
        ">Free · Instant · Private</div>

        <h1 style="
            font-family: 'Syne', sans-serif;
            font-size: 3.2rem;
            font-weight: 800;
            color: {COLORS['text_primary']};
            line-height: 1.1;
            letter-spacing: -2px;
            margin-bottom: 1.2rem;
        ">
            Know Your
            <span style="
                background: linear-gradient(135deg,
                    {COLORS['primary']}, {COLORS['gold']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">Credit Score</span><br/>
            in 3 Minutes
        </h1>

        <p style="
            font-size: 1.05rem;
            color: {COLORS['text_secondary']};
            max-width: 480px;
            margin: 0 auto 2.5rem auto;
            line-height: 1.8;
        ">
            FinSight uses AI to analyse your financial profile
            and give you a personalised credit score — with a
            clear plan to improve it.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1.2, 1.5, 1.2])
    with col2:
        if st.button("Get My Free Score →",
                     key="cta_hero", use_container_width=True):
            st.session_state['page'] = 'assessment'
            st.rerun()

    # ── Trust ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-top:0.8rem;
                margin-bottom:3rem;">
        <span style="font-size:0.78rem;
                     color:{COLORS['text_muted']};">
            🔒 Your data is never shared or sold
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-bottom: 3.5rem;
        padding: 1.5rem;
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
    ">
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif;
                        font-size:1.8rem; font-weight:800;
                        color:{COLORS['primary']};">3 min</div>
            <div style="font-size:0.75rem;
                        color:{COLORS['text_muted']};
                        letter-spacing:1px;
                        text-transform:uppercase;
                        margin-top:0.2rem;">Average time</div>
        </div>
        <div style="width:1px;
                    background:rgba(255,255,255,0.06);"></div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif;
                        font-size:1.8rem; font-weight:800;
                        color:{COLORS['gold']};">20+</div>
            <div style="font-size:0.75rem;
                        color:{COLORS['text_muted']};
                        letter-spacing:1px;
                        text-transform:uppercase;
                        margin-top:0.2rem;">Factors analysed</div>
        </div>
        <div style="width:1px;
                    background:rgba(255,255,255,0.06);"></div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif;
                        font-size:1.8rem; font-weight:800;
                        color:{COLORS['success']};">100%</div>
            <div style="font-size:0.75rem;
                        color:{COLORS['text_muted']};
                        letter-spacing:1px;
                        text-transform:uppercase;
                        margin-top:0.2rem;">Free forever</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <span style="font-family:'Syne',sans-serif;
                     font-size:1.3rem; font-weight:800;
                     color:{COLORS['text_primary']};">
            How it works
        </span>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Enter Your Details",
         "Fill in your income, expenses, and debt. "
         "No sensitive data required — no ID, no bank login.",
         COLORS['primary']),
        ("02", "AI Analyses Your Profile",
         "Our machine learning model scores 20+ financial factors "
         "in real time to calculate your personalised score.",
         COLORS['gold']),
        ("03", "Get Your Score & Plan",
         "See your score, every factor that affected it, "
         "and a prioritised action plan to improve.",
         COLORS['success']),
    ]

    cols = st.columns(3)
    for col, (num, title, desc, color) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="fs-card" style="
                text-align: center;
                min-height: 200px;
                padding: 1.8rem 1.4rem;
            ">
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.65rem;
                    font-weight: 600;
                    color: {color};
                    letter-spacing: 2px;
                    margin-bottom: 0.8rem;
                    opacity: 0.8;
                ">STEP {num}</div>
                <div style="
                    font-family: 'Syne', sans-serif;
                    font-weight: 700;
                    font-size: 1rem;
                    color: {COLORS['text_primary']};
                    margin-bottom: 0.7rem;
                ">{title}</div>
                <div style="
                    font-size: 0.85rem;
                    color: {COLORS['text_secondary']};
                    line-height: 1.7;
                ">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>",
                unsafe_allow_html=True)

    # ── Score bands ───────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <span style="font-family:'Syne',sans-serif;
                     font-size:1.3rem; font-weight:800;
                     color:{COLORS['text_primary']};">
            Credit score bands
        </span>
    </div>
    """, unsafe_allow_html=True)

    bands = [
        ("300–449", "Poor",      COLORS['danger'],  "#FF4D6A18",
         "High risk. Focus on clearing defaults."),
        ("450–579", "Fair",      COLORS['warning'], "#F5A62318",
         "Improving. Payment habits help fast."),
        ("580–699", "Good",      COLORS['success'], "#10D98A18",
         "Solid. Qualifies for most products."),
        ("700–850", "Excellent", COLORS['primary'], "#00D4AA18",
         "Best rates. Top tier standing."),
    ]

    cols = st.columns(4)
    for col, (rng, label, color, bg, desc) in zip(cols, bands):
        with col:
            st.markdown(f"""
            <div style="
                background: {bg};
                border: 1px solid {color}22;
                border-radius: 14px;
                padding: 1.2rem 1rem;
                text-align: center;
                min-height: 130px;
            ">
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.85rem;
                    font-weight: 600;
                    color: {color};
                    margin-bottom: 0.3rem;
                ">{rng}</div>
                <div style="
                    font-family: 'Syne', sans-serif;
                    font-weight: 800;
                    color: {color};
                    font-size: 1rem;
                    margin-bottom: 0.5rem;
                ">{label}</div>
                <div style="
                    font-size: 0.78rem;
                    color: {COLORS['text_muted']};
                    line-height: 1.5;
                ">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Bottom CTA ────────────────────────────────────────────────
    st.markdown("<div style='height:2.5rem;'></div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1.5, 1.2])
    with col2:
        if st.button("Check My Score — Free →",
                     key="cta_bottom", use_container_width=True):
            st.session_state['page'] = 'assessment'
            st.rerun()