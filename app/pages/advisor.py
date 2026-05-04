# app/pages/advisor.py
import streamlit as st
from app.styles.theme import COLORS


def render_advisor():
    result = st.session_state.get("result")

    st.markdown(
        """
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div class="fs-page-title">🤖 AI Financial Advisor</div>
        <div class="fs-page-subtitle">
            Ask anything about your score, finances, or how to improve.
            Your advisor knows your full financial profile.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not result:
        st.info(
            "Complete your credit assessment first. The advisor uses "
            "your score and financial data to give personalised answers."
        )
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("← Take Assessment", use_container_width=True):
                st.session_state["page"] = "assessment"
                st.rerun()
        return

    # Check API key
    import os

    api_key = None
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        st.warning(
            "ANTHROPIC_API_KEY not configured. "
            "Add it to your Render environment variables."
        )
        if st.button("← Back to Score", use_container_width=True):
            st.session_state["page"] = "results"
            st.rerun()
        return

    try:
        from core.ai_advisor import (
            ChatMessage,
            get_advisor_response,
            get_opening_message,
            get_suggested_questions,
        )
    except ImportError:
        st.error("AI advisor module not found. Ensure core/ai_advisor.py exists.")
        return

    score_color = {
        "Poor": COLORS["danger"],
        "Fair": COLORS["warning"],
        "Good": COLORS["good"],
        "Excellent": COLORS["teal"],
    }.get(result.score_band, COLORS["blue"])

    st.markdown(
        f"""
    <div style="background:{COLORS["navy"]};border-radius:8px;
                padding:0.7rem 1.2rem;margin-bottom:1.2rem;
                display:flex;justify-content:space-between;
                align-items:center;">
        <div style="color:rgba(255,255,255,0.6);font-size:0.82rem;">
            Advising based on your profile
        </div>
        <div style="font-family:'JetBrains Mono',monospace;
                    font-weight:600;font-size:0.98rem;
                    color:{score_color};">
            {result.credit_score} —
            <span style="color:white;font-weight:400;">
                {result.score_band}
            </span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if "chat_messages" not in st.session_state:
        opening = get_opening_message(result)
        st.session_state["chat_messages"] = [
            ChatMessage(role="assistant", content=opening)
        ]

    messages = st.session_state["chat_messages"]

    # Suggested questions (show only early in conversation)
    if len(messages) <= 2:
        suggestions = get_suggested_questions(result)
        st.markdown(
            f"""
        <div style="font-size:0.78rem;color:{COLORS["text_muted"]};
                    margin-bottom:0.5rem;">💬 Suggested questions:</div>
        """,
            unsafe_allow_html=True,
        )
        cols = st.columns(min(len(suggestions), 3))
        for i, (col, q) in enumerate(zip(cols, suggestions[:3])):
            with col:
                if st.button(q, key=f"sq_{i}", use_container_width=True):
                    st.session_state["chat_messages"].append(
                        ChatMessage(role="user", content=q)
                    )
                    st.session_state["pending_ai"] = True
                    st.rerun()

    # Chat history
    for msg in st.session_state["chat_messages"]:
        if msg.role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg.content)
        else:
            with st.chat_message("user"):
                st.markdown(msg.content)

    # Handle pending response from suggestion click
    if st.session_state.get("pending_ai"):
        st.session_state.pop("pending_ai", None)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full = ""
                placeholder = st.empty()
                for chunk in get_advisor_response(
                    st.session_state["chat_messages"], result, stream=True
                ):
                    full += chunk
                    placeholder.markdown(full + "▌")
                placeholder.markdown(full)
        st.session_state["chat_messages"].append(
            ChatMessage(role="assistant", content=full)
        )
        st.rerun()

    # Chat input
    user_input = st.chat_input("Ask your advisor anything about your finances...")
    if user_input and user_input.strip():
        st.session_state["chat_messages"].append(
            ChatMessage(role="user", content=user_input.strip())
        )
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full = ""
                placeholder = st.empty()
                for chunk in get_advisor_response(
                    st.session_state["chat_messages"], result, stream=True
                ):
                    full += chunk
                    placeholder.markdown(full + "▌")
                placeholder.markdown(full)
        st.session_state["chat_messages"].append(
            ChatMessage(role="assistant", content=full)
        )
        st.rerun()

    # Footer
    st.markdown(
        "<hr style='margin:1.5rem 0;border-color:#E5E7EB;'>", unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Score", use_container_width=True):
            st.session_state["page"] = "results"
            st.rerun()
    with col2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.pop("chat_messages", None)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True):
            st.session_state["page"] = "landing"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
