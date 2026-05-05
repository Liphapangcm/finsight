
"""
Assessment form — Enhanced UI/UX
- Animated step transitions
- Real-time validation & feedback
- Progress tracking with animations
- Smart defaults & tooltips
- Mobile-optimized
"""

import streamlit as st
from app.styles.theme import COLORS
import time

DISTRICTS = [
    "Maseru",
    "Berea",
    "Leribe",
    "Butha-Buthe",
    "Mokhotlong",
    "Thaba-Tseka",
    "Qacha's Nek",
    "Quthing",
    "Mohale's Hoek",
    "Mafeteng",
]
STEP_LABELS = ["Personal Info", "Income & Expenses", "Debt & Savings"]
STEP_ICONS = ["👤", "💰", "📊"]


def _step_indicator(step: int, total: int = 3):
    """Animated step indicator with icons and labels"""
    
    # Create animated progress bar
    progress_pct = ((step - 1) / (total - 1)) * 100
    
    steps_html = ""
    for i in range(1, total + 1):
        is_active = i == step
        is_completed = i < step
        status_class = "active" if is_active else ("completed" if is_completed else "pending")
        icon = STEP_ICONS[i-1]
        
        steps_html += f"""
        <div class="step-item {status_class}" data-step="{i}">
            <div class="step-circle">
                {icon if is_completed else i}
            </div>
            <div class="step-label">{STEP_LABELS[i-1]}</div>
        </div>
        """
    
    st.markdown(f"""
    <style>
        .step-container {{
            margin: 1.5rem 0 2rem 0;
            padding: 0.5rem;
        }}
        .step-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            margin-bottom: 1rem;
        }}
        .step-item {{
            flex: 1;
            text-align: center;
            position: relative;
            z-index: 2;
        }}
        .step-circle {{
            width: 40px;
            height: 40px;
            margin: 0 auto 8px auto;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}
        .step-item.completed .step-circle {{
            background: {COLORS['success']};
            color: white;
            transform: scale(1.05);
        }}
        .step-item.active .step-circle {{
            background: {COLORS['primary']};
            color: white;
            box-shadow: 0 0 0 4px {COLORS['primary']}20;
            animation: pulse 2s infinite;
        }}
        .step-item.pending .step-circle {{
            background: #E5E7EB;
            color: #9CA3AF;
        }}
        .step-label {{
            font-size: 0.75rem;
            color: {COLORS['text_secondary']};
            font-weight: 500;
        }}
        .step-item.active .step-label {{
            color: {COLORS['primary']};
            font-weight: 600;
        }}
        .step-progress-bar {{
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            height: 2px;
            background: #E5E7EB;
            z-index: 1;
        }}
        .step-progress-fill {{
            height: 100%;
            background: {COLORS['success']};
            width: {progress_pct}%;
            transition: width 0.5s ease;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
    </style>
    
    <div class="step-container">
        <div class="step-row">
            <div class="step-progress-bar">
                <div class="step-progress-fill"></div>
            </div>
            {steps_html}
        </div>
    </div>
    
    <div style="margin: 0.5rem 0 1.5rem 0; text-align: center;">
        <span style="background: {COLORS['primary']}10; 
                     padding: 0.25rem 1rem; 
                     border-radius: 20px;
                     font-size: 0.8rem;
                     color: {COLORS['primary']};">
            Step {step} of {total}: {STEP_LABELS[step-1]}
        </span>
    </div>
    """, unsafe_allow_html=True)


def _trust_badge():
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 1rem; margin: 0.5rem 0 1.5rem 0;">
        <span style="background: {COLORS['success']}10; 
                     color: {COLORS['success']};
                     padding: 0.25rem 0.75rem;
                     border-radius: 20px;
                     font-size: 0.7rem;">
            🔒 GDPR Compliant
        </span>
        <span style="background: {COLORS['success']}10; 
                     color: {COLORS['success']};
                     padding: 0.25rem 0.75rem;
                     border-radius: 20px;
                     font-size: 0.7rem;">
            🤖 AI-Powered
        </span>
        <span style="background: {COLORS['success']}10; 
                     color: {COLORS['success']};
                     padding: 0.25rem 0.75rem;
                     border-radius: 20px;
                     font-size: 0.7rem;">
            ⚡ 2-Minute Read
        </span>
    </div>
    """, unsafe_allow_html=True)


def _help_tooltip(text, help_text):
    """Display a help tooltip next to a label"""
    return f"""
    <div style="display: inline-flex; align-items: center; gap: 0.25rem;">
        <span>{text}</span>
        <span style="cursor: help; 
                     color: {COLORS['text_muted']};
                     border: 1px solid {COLORS['text_muted']}40;
                     border-radius: 50%;
                     width: 16px;
                     height: 16px;
                     display: inline-flex;
                     align-items: center;
                     justify-content: center;
                     font-size: 11px;"
              title="{help_text}">?</span>
    </div>
    """


def _nav_buttons(back_step: int, next_step: int, next_label: str = "Continue →"):
    """Enhanced navigation buttons with animations"""
    
    col_back, col_next = st.columns([1, 1])
    
    with col_back:
        if st.button("← Back", key=f"back_{back_step}", use_container_width=True):
            st.session_state["form_step"] = back_step
            st.rerun()
    
    with col_next:
        if st.button(next_label, key=f"next_{next_step}", 
                    type="primary" if next_label != "Continue →" else "secondary",
                    use_container_width=True):
            return True
    return False


# ── Step 1 with Enhanced UX ────────────────────────────────────────
def render_step1():
    _step_indicator(1)
    _trust_badge()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']}05 0%, transparent 100%);
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 1.5rem;">
        <h3 style="margin: 0 0 0.5rem 0; color: {COLORS['primary']};">👋 Welcome!</h3>
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.9rem;">
            Let's get to know you better. This helps us provide personalized recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=st.session_state.get("age", 30),
            help="We need your age to assess appropriate financial products"
        )
        
        # Real-time age validation
        if age < 18:
            st.warning("⚠️ You must be at least 18 years old to use this service")
        elif age > 70:
            st.info("💡 Senior citizens may qualify for special banking products")
    
    with col2:
        district = st.selectbox(
            "District",
            options=DISTRICTS,
            index=DISTRICTS.index(st.session_state.get("district", "Maseru")),
            help="Your district helps us understand regional economic factors"
        )

    employment = st.selectbox(
        "Employment Status",
        options=["employed", "self_employed", "unemployed", "student"],
        format_func=lambda x: {
            "employed": "💼 Employed (salary / wages)",
            "self_employed": "🏪 Self-Employed / Business Owner",
            "unemployed": "🔍 Currently Unemployed",
            "student": "📚 Student",
        }[x],
        index=["employed", "self_employed", "unemployed", "student"].index(
            st.session_state.get("employment_type", "employed")
        ),
        help="Your employment type affects creditworthiness assessment"
    )
    
    # Smart dependent suggestion based on age
    default_deps = st.session_state.get("num_dependents", 1)
    if age < 25 and default_deps > 2:
        default_deps = 1
        
    num_dep = st.slider(
        "Number of Dependents",
        min_value=0,
        max_value=10,
        value=default_deps,
        help="People financially dependent on your income (children, elderly parents, etc.)"
    )
    
    # Show contextual message
    if num_dep == 0:
        st.caption("💡 Having no dependents means more disposable income for savings")
    elif num_dep > 3:
        st.info(f"🏠 With {num_dep} dependents, budgeting becomes crucial for financial health")

    st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
    
    if _nav_buttons(back_step=1, next_step=2):
        # Validation
        errors = []
        if age < 18:
            errors.append("You must be at least 18 years old")
        if age > 100:
            errors.append("Please enter a valid age")
            
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state.update({
                "age": age,
                "district": district,
                "employment_type": employment,
                "num_dependents": num_dep,
                "form_step": 2,
            })
            st.rerun()


# ── Step 2 with Real-time Calculator ────────────────────────────────
def render_step2():
    _step_indicator(2)
    
    st.markdown(f"""
    <div style="background: {COLORS['success']}08;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1.5rem;
                border-left: 3px solid {COLORS['success']};">
        <span style="font-size: 0.9rem;">💡 </span>
        <span style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
            <strong>Tip:</strong> Be as accurate as possible. Round up expenses to be conservative.
        </span>
    </div>
    """, unsafe_allow_html=True)

    monthly_income = st.number_input(
        "💰 Monthly Income (LSL — Maloti)",
        min_value=0.0,
        max_value=500_000.0,
        step=100.0,
        value=float(st.session_state.get("monthly_income", 5000)),
        help="Total take-home pay after tax (what hits your bank account)"
    )
    
    # Real-time income feedback
    if monthly_income > 0:
        if monthly_income < 2000:
            st.warning("⚠️ Your income is below the national average. Focus on budgeting and savings strategies.")
        elif monthly_income > 30000:
            st.success("🌟 Excellent income! Let's optimize your savings and investments.")

    with st.expander("📖 How to calculate your income"):
        st.markdown("""
        - **Salary**: Your monthly paycheck after taxes
        - **Business Income**: Average monthly profit
        - **Side Hustles**: Freelance, part-time work
        - **Rental Income**: Money from properties
        - **Remittances**: Money from family abroad
        """)

    st.markdown('<div style="margin: 1.5rem 0 1rem 0;">', unsafe_allow_html=True)
    st.markdown("### 💸 Monthly Expenses")
    st.caption("Enter 0 for any category that does not apply.")

    col1, col2 = st.columns(2)
    
    with col1:
        housing = st.number_input(
            "🏠 Housing / Rent",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.get("housing_expense", 1500)),
            help="Rent, mortgage, property taxes"
        )
        transport = st.number_input(
            "🚗 Transport",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.get("transport_expense", 500)),
            help="Fuel, public transport, car maintenance"
        )
        other = st.number_input(
            "📱 Other Expenses",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.get("other_expense", 500)),
            help="Entertainment, subscriptions, dining out"
        )
    with col2:
        food = st.number_input(
            "🍎 Food & Groceries",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.get("food_expense", 1200)),
        )
        utilities = st.number_input(
            "💡 Utilities & Airtime",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.get("utilities_expense", 400)),
            help="Electricity, water, internet, mobile data"
        )

    total_exp = housing + food + transport + utilities + other
    remaining = monthly_income - total_exp
    savings_rate = (remaining / monthly_income * 100) if monthly_income > 0 else 0
    
    # Enhanced balance widget with color coding
    rem_color = COLORS["success"] if remaining >= 0 else COLORS["danger"]
    rem_sign = "+" if remaining >= 0 else ""
    
    # Calculate DTI ratio (Debt-to-Income)
    dti = (total_exp / monthly_income * 100) if monthly_income > 0 else 0
    
    st.markdown(f"""
    <div style="background: #F9FAFB;
                border-radius: 12px;
                padding: 1rem;
                margin: 1rem 0;
                border: 1px solid #E5E7EB;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 0.25rem;">Total Expenses</div>
                <div style="font-size: 1.5rem; font-weight: bold;">M{total_exp:,.0f}</div>
                <div style="font-size: 0.7rem; color: #6B7280;">{dti:.1f}% of income</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 0.25rem;">Monthly Balance</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {rem_color};">M{rem_sign}{remaining:,.0f}</div>
                <div style="font-size: 0.7rem; color: {rem_color};">
                    {savings_rate:.1f}% savings rate
                </div>
            </div>
        </div>
        <div style="margin-top: 0.75rem; height: 6px; background: #E5E7EB; border-radius: 3px; overflow: hidden;">
            <div style="width: {min(100, max(0, savings_rate))}%; 
                        height: 100%; 
                        background: {rem_color if remaining >= 0 else COLORS['danger']};
                        transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Health recommendations based on savings rate
    if remaining > 0:
        if savings_rate < 10:
            st.info("📊 **Savings Tip:** Aim to save at least 10-20% of your income. Consider cutting non-essential expenses.")
        elif savings_rate < 20:
            st.success("👍 **Good job!** You're on the right track. Consider investing your surplus.")
        else:
            st.balloons()
            st.success("🏆 **Excellent savings discipline!** You're building wealth effectively.")
    else:
        st.error("⚠️ **Budget Alert:** Your expenses exceed income. Let's find ways to reduce costs or increase income.")

    if _nav_buttons(back_step=1, next_step=3):
        if monthly_income <= 0:
            st.error("Please enter your monthly income to continue")
        else:
            st.session_state.update({
                "monthly_income": monthly_income,
                "housing_expense": housing,
                "food_expense": food,
                "transport_expense": transport,
                "utilities_expense": utilities,
                "other_expense": other,
                "form_step": 3,
            })
            st.rerun()


# ── Step 3 with Smart Defaults ────────────────────────────────────────
def render_step3():
    _step_indicator(3)
    
    st.markdown(f"""
    <div style="background: {COLORS['primary']}08;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1.5rem;
                border-left: 3px solid {COLORS['primary']};">
        <span style="font-size: 0.9rem;">🎯 </span>
        <span style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
            <strong>Almost there!</strong> Your answers help us generate an accurate credit score and personalized recommendations.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💳 Debt & Credit History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_debt = st.number_input(
            "📉 Total Outstanding Debt (LSL)",
            min_value=0.0,
            step=500.0,
            value=float(st.session_state.get("total_debt", 0)),
            help="All loans, credit cards, hire purchase agreements combined"
        )
        
        # Debt warning
        monthly_income = st.session_state.get("monthly_income", 1)
        if total_debt > monthly_income * 6:
            st.warning("⚠️ Your debt is quite high. Prioritize debt reduction strategies.")
        
        has_defaulted = st.radio(
            "⚠️ Ever failed to repay a loan?",
            options=[False, True],
            format_func=lambda x: "✅ No — clean record" if not x else "❌ Yes — previous default",
            index=int(st.session_state.get("has_defaulted", False)),
            horizontal=True,
        )
        
    with col2:
        num_loans = st.number_input(
            "📋 Active Loans (count)",
            min_value=0,
            max_value=15,
            value=int(st.session_state.get("num_active_loans", 0)),
            help="Number of currently active loan accounts"
        )
        
        payment_reg = st.selectbox(
            "⏰ Payment Regularity",
            options=["always", "sometimes", "rarely"],
            format_func=lambda x: {
                "always": "✅ Always on time",
                "sometimes": "⚠️ Sometimes late",
                "rarely": "❌ Rarely on time",
            }[x],
            index=["always", "sometimes", "rarely"].index(
                st.session_state.get("payment_regularity", "always")
            ),
            help="How often do you make payments on time?"
        )

    st.markdown("### 💰 Savings & Digital Finance")
    
    has_savings = st.radio(
        "Do you save money regularly?",
        options=[True, False],
        format_func=lambda x: "✅ Yes, I save regularly" if x else "❌ No savings currently",
        index=0 if st.session_state.get("has_savings", False) else 1,
        horizontal=True,
    )
    
    monthly_savings = 0.0
    if has_savings:
        monthly_savings = st.number_input(
            "Monthly Savings Amount (LSL)",
            min_value=0.0,
            step=100.0,
            value=float(st.session_state.get("monthly_savings", 500)),
            help="Consistent saving is a positive credit factor"
        )

    mm_freq = st.selectbox(
        "📱 Mobile Money Usage",
        options=["daily", "weekly", "monthly", "never"],
        format_func=lambda x: {
            "daily": "📱 Daily",
            "weekly": "📱 Weekly",
            "monthly": "📱 Monthly",
            "never": "❌ I don't use mobile money",
        }[x],
        index=["daily", "weekly", "monthly", "never"].index(
            st.session_state.get("mobile_money_frequency", "weekly")
        ),
        help="Mobile money usage shows digital financial literacy"
    )
    
    # Summary card before submission
    with st.expander("📋 Review Your Answers (Click to expand)", expanded=False):
        st.markdown(f"""
        **Personal Info**  
        • Age: {st.session_state.get('age', 'N/A')}  
        • District: {st.session_state.get('district', 'N/A')}  
        • Employment: {st.session_state.get('employment_type', 'N/A')}  
        • Dependents: {st.session_state.get('num_dependents', 'N/A')}  
        
        **Income & Expenses**  
        • Monthly Income: M{st.session_state.get('monthly_income', 0):,.0f}  
        • Total Expenses: M{housing + food + transport + utilities + other:,.0f}  
        
        **Credit Profile**  
        • Total Debt: M{total_debt:,.0f}  
        • Active Loans: {num_loans}  
        • Payment History: {payment_reg}  
        • Regular Savings: {"Yes" if has_savings else "No"}
        """)
    
    if _nav_buttons(back_step=2, next_step=3, next_label="🚀 Calculate My Score →"):
        # Final validation
        errors = []
        monthly_income = st.session_state.get("monthly_income", 0)
        
        if total_debt > monthly_income * 12:
            errors.append("Your total debt exceeds one year's income. Consider debt counseling.")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Show loading animation
            with st.spinner("🔮 Analyzing your financial profile..."):
                time.sleep(0.5)  # Small delay for UX
                
                st.session_state.update({
                    "total_debt": total_debt,
                    "num_active_loans": num_loans,
                    "has_defaulted": has_defaulted,
                    "payment_regularity": payment_reg,
                    "has_savings": has_savings,
                    "monthly_savings": monthly_savings,
                    "mobile_money_frequency": mm_freq,
                    "form_step": "submitted",
                })
                st.rerun()


# ── Router with Enhanced Feedback ────────────────────────────────────────
def render_assessment():
    step = st.session_state.get("form_step", 1)
    
    if step == 1:
        render_step1()
    elif step == 2:
        render_step2()
    elif step == 3:
        render_step3()
    elif step == "submitted":
        _run_and_redirect()


def _run_and_redirect():
    from core.service import run_assessment
    from core.schemas import AssessmentInput

    # Enhanced loading experience
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        (0.3, "📊 Analyzing your financial data..."),
        (0.6, "🤖 Running AI credit model..."),
        (0.9, "📝 Generating personalized insights..."),
    ]
    
    for progress, message in steps:
        progress_bar.progress(progress)
        status_text.text(message)
        time.sleep(0.3)
    
    try:
        inp = AssessmentInput(
            age=st.session_state["age"],
            employment_type=st.session_state["employment_type"],
            num_dependents=st.session_state["num_dependents"],
            district=st.session_state.get("district", "Maseru"),
            monthly_income=st.session_state["monthly_income"],
            housing_expense=st.session_state["housing_expense"],
            food_expense=st.session_state["food_expense"],
            transport_expense=st.session_state["transport_expense"],
            utilities_expense=st.session_state["utilities_expense"],
            other_expense=st.session_state["other_expense"],
            total_debt=st.session_state["total_debt"],
            num_active_loans=st.session_state["num_active_loans"],
            has_defaulted=st.session_state["has_defaulted"],
            payment_regularity=st.session_state["payment_regularity"],
            has_savings=st.session_state["has_savings"],
            monthly_savings=st.session_state["monthly_savings"],
            mobile_money_frequency=st.session_state["mobile_money_frequency"],
        )
        result, errors = run_assessment(inp)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Complete! Redirecting to your results...")
        time.sleep(0.5)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state["form_step"] = 1
        if st.button("← Return to Form"):
            st.rerun()
        return

    if errors:
        st.error("Please fix the following before continuing:")
        for e in errors:
            st.markdown(f"— {e}")
        st.session_state["form_step"] = 1
        if st.button("← Return to Form"):
            st.rerun()
        return

    st.session_state["result"] = result
    st.session_state["page"] = "results"
    st.rerun()