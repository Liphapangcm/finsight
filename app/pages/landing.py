import streamlit as st
from app.styles.theme import COLORS


def render_landing():
    # ── Hero ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 3rem 1rem 2rem 1rem;">
        <div style="font-size:0.9rem; font-weight:600;
                    color:{COLORS['accent']}; letter-spacing:2px;
                    text-transform:uppercase; margin-bottom:1rem;">
            Free · Instant · Private
        </div>
        <h1 style="font-size:2.8rem; font-weight:900;
                   color:{COLORS['primary']}; line-height:1.15;
                   margin-bottom:1rem;">
            Know Your Financial<br/>
            <span style="color:{COLORS['accent']};">Credit Standing</span>
        </h1>
        <p style="font-size:1.1rem; color:#4B5563; max-width:520px;
                  margin:0 auto 2rem auto; line-height:1.7;">
            FinSight analyses your income, expenses, and financial
            behaviour to give you a personalised credit score and
            a clear action plan — in under 3 minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Button ────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get My Free Credit Score", key="cta_main"):
            st.session_state['page'] = 'assessment'
            st.rerun()

    # ── Trust badge ───────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; margin-top:1rem;">
        <span style="font-size:0.82rem; color:#6B7280;">
            🔒 Your data is processed on this device and never stored
            without your consent
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:2.5rem 0; border-color:#E5E7EB;'>",
                unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-size:1.6rem; font-weight:800;
                   color:{COLORS['primary']};">
            How It Works
        </h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    steps = [
        ("📝", "1. Enter Your Details",
         "Fill in your income, expenses, and debt in our secure 3-step form. "
         "Takes less than 3 minutes."),
        ("🤖", "2. AI Analyses Your Profile",
         "Our machine learning model analyses 20+ financial factors "
         "to calculate your personalised credit score."),
        ("📊", "3. Get Your Score & Plan",
         "Receive your score, a breakdown of every factor, "
         "and a prioritised action plan to improve it."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], steps):
        with col:
            st.markdown(f"""
            <div class="fs-card" style="text-align:center; min-height:180px;">
                <div style="font-size:2.2rem; margin-bottom:0.8rem;">{icon}</div>
                <div style="font-weight:700; font-size:1rem;
                            color:{COLORS['primary']};
                            margin-bottom:0.5rem;">{title}</div>
                <div style="font-size:0.88rem; color:#6B7280;
                            line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:2.5rem 0; border-color:#E5E7EB;'>",
                unsafe_allow_html=True)

    # ── Score bands explainer ─────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem; font-weight:800;
                   color:{COLORS['primary']};">
            Understanding Your Score
        </h2>
    </div>
    """, unsafe_allow_html=True)

    bands = [
        ("300–449", "Poor",      "#E53935", "#FFEBEE",
         "High credit risk. Focus on clearing defaults and reducing debt."),
        ("450–579", "Fair",      "#FB8C00", "#FFF3E0",
         "Below average. Improving payment habits will move you up quickly."),
        ("580–699", "Good",      "#43A047", "#E8F5E9",
         "Average risk. You qualify for most basic credit products."),
        ("700–850", "Excellent", "#00897B", "#E0F2F1",
         "Low risk. Best rates and terms from lenders."),
    ]
    cols = st.columns(4)
    for col, (rng, label, color, bg, desc) in zip(cols, bands):
        with col:
            st.markdown(f"""
            <div style="background:{bg}; border-radius:10px;
                        padding:1rem; text-align:center; min-height:140px;">
                <div style="font-size:1.1rem; font-weight:800;
                            color:{color};">{rng}</div>
                <div style="font-weight:700; color:{color};
                            margin:0.3rem 0;">{label}</div>
                <div style="font-size:0.78rem; color:#4B5563;
                            line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Bottom CTA ────────────────────────────────────────────────
    st.markdown("<div style='margin-top:2.5rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Check My Score Now — It's Free",
                     key="cta_bottom"):
            st.session_state['page'] = 'assessment'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)