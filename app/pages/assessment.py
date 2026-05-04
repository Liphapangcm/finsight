# app/pages/assessment.py
"""
Assessment form — fixes:
- Back/Continue buttons always perfectly side-by-side on desktop
- Consistent column widths across all 3 steps
- No layout shift between steps
"""
import streamlit as st
from app.styles.theme import COLORS
from core.schemas import AssessmentInput

DISTRICTS = [
    "Maseru", "Berea", "Leribe", "Butha-Buthe", "Mokhotlong",
    "Thaba-Tseka", "Qacha's Nek", "Quthing",
    "Mohale's Hoek", "Mafeteng",
]
STEP_LABELS = ["Personal Info", "Income & Expenses", "Debt & Savings"]


def _step_indicator(step: int, total: int = 3):
    segs = "".join(
        f'<div class="step-seg{"  done" if i <= step else ""}"></div>'
        for i in range(1, total + 1)
    )
    st.markdown(f"""
    <div class="step-meta">
        Step <strong>{step} of {total}</strong>
        &nbsp;—&nbsp; {STEP_LABELS[step - 1]}
    </div>
    <div class="step-row">{segs}</div>
    """, unsafe_allow_html=True)


def _trust():
    st.markdown("""
    <div class="trust-note">
        🔒 Your data is processed privately and never shared or sold
    </div>
    """, unsafe_allow_html=True)


def _nav_buttons(back_key: str, next_key: str,
                 next_label: str, back_step: int,
                 next_action=None):
    """
    Renders Back + Next buttons in a fixed 2-column layout.
    Guarantees horizontal alignment on all screen sizes.
    """
    col_back, col_next = st.columns([1, 1])
    with col_back:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("← Back", key=back_key,
                     use_container_width=True):
            st.session_state['form_step'] = back_step
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_next:
        if st.button(next_label, key=next_key,
                     use_container_width=True):
            if next_action:
                next_action()


# ── Step 1 ────────────────────────────────────────────────────────
def render_step1():
    _step_indicator(1)
    _trust()
    st.markdown('<div class="form-section">Personal Information</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age", min_value=18, max_value=100,
            value=st.session_state.get('age', 30),
        )
    with col2:
        district = st.selectbox(
            "District", options=DISTRICTS,
            index=DISTRICTS.index(
                st.session_state.get('district', 'Maseru')),
        )

    employment = st.selectbox(
        "Employment Status",
        options=["employed", "self_employed", "unemployed", "student"],
        format_func=lambda x: {
            "employed":      "Employed (salary / wages)",
            "self_employed": "Self-Employed / Business Owner",
            "unemployed":    "Currently Unemployed",
            "student":       "Student",
        }[x],
        index=["employed", "self_employed",
               "unemployed", "student"].index(
            st.session_state.get('employment_type', 'employed')),
    )
    num_dep = st.slider(
        "Number of Dependents", min_value=0, max_value=10,
        value=st.session_state.get('num_dependents', 1),
        help="People financially dependent on your income",
    )

    st.markdown("<div style='margin-top:1.5rem;'>",
                unsafe_allow_html=True)
    if st.button("Continue →", key="s1_next",
                 use_container_width=True):
        st.session_state.update({
            'age': age, 'district': district,
            'employment_type': employment,
            'num_dependents': num_dep,
            'form_step': 2,
        })
        st.rerun()


# ── Step 2 ────────────────────────────────────────────────────────
def render_step2():
    _step_indicator(2)
    st.markdown('<div class="form-section">Income</div>',
                unsafe_allow_html=True)

    monthly_income = st.number_input(
        "Monthly Income (LSL — Maloti)",
        min_value=0.0, max_value=500_000.0, step=100.0,
        value=float(st.session_state.get('monthly_income', 5000)),
        help="Total take-home pay after tax",
    )

    st.markdown('<div class="form-section">Monthly Expenses</div>',
                unsafe_allow_html=True)
    st.caption("Enter 0 for any category that does not apply.")

    col1, col2 = st.columns(2)
    with col1:
        housing = st.number_input(
            "Housing / Rent", min_value=0.0, step=50.0,
            value=float(st.session_state.get('housing_expense', 1500)))
        transport = st.number_input(
            "Transport", min_value=0.0, step=50.0,
            value=float(st.session_state.get('transport_expense', 500)))
        other = st.number_input(
            "Other Expenses", min_value=0.0, step=50.0,
            value=float(st.session_state.get('other_expense', 500)))
    with col2:
        food = st.number_input(
            "Food & Groceries", min_value=0.0, step=50.0,
            value=float(st.session_state.get('food_expense', 1200)))
        utilities = st.number_input(
            "Utilities & Airtime", min_value=0.0, step=50.0,
            value=float(st.session_state.get('utilities_expense', 400)))

    total_exp = housing + food + transport + utilities + other
    remaining = monthly_income - total_exp
    rem_color = COLORS['success'] if remaining >= 0 else COLORS['danger']
    rem_sign  = "+" if remaining >= 0 else ""
    rem_label = "available" if remaining >= 0 else "OVER BUDGET"

    st.markdown(f"""
    <div class="balance-widget">
        <div>
            <div class="bal-label">Total Expenses</div>
            <div class="bal-value">M{total_exp:,.0f}</div>
        </div>
        <div style="text-align:right;">
            <div class="bal-label">Balance</div>
            <div class="bal-value" style="color:{rem_color};">
                M{rem_sign}{remaining:,.0f}
            </div>
            <div style="font-size:0.66rem;color:{rem_color};
                        font-weight:600;margin-top:1px;">{rem_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fixed button row ──────────────────────────────────────────
    st.markdown("<div style='margin-top:1.25rem;'>",
                unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 1])
    with col_back:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("← Back", key="s2_back",
                     use_container_width=True):
            st.session_state['form_step'] = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_next:
        if st.button("Continue →", key="s2_next",
                     use_container_width=True):
            st.session_state.update({
                'monthly_income':    monthly_income,
                'housing_expense':   housing,
                'food_expense':      food,
                'transport_expense': transport,
                'utilities_expense': utilities,
                'other_expense':     other,
                'form_step':         3,
            })
            st.rerun()


# ── Step 3 ────────────────────────────────────────────────────────
def render_step3():
    _step_indicator(3)
    st.markdown('<div class="form-section">Debt & Credit</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        total_debt = st.number_input(
            "Total Outstanding Debt (LSL)",
            min_value=0.0, step=500.0,
            value=float(st.session_state.get('total_debt', 0)),
            help="All loans, credit, hire purchase combined",
        )
        has_defaulted = st.radio(
            "Ever failed to repay a loan?",
            options=[False, True],
            format_func=lambda x:
                "Yes — previous default" if x else "No — clean record",
            index=int(st.session_state.get('has_defaulted', False)),
            horizontal=True,
        )
    with col2:
        num_loans = st.number_input(
            "Active Loans (count)", min_value=0, max_value=15,
            value=int(st.session_state.get('num_active_loans', 0)),
        )
        payment_reg = st.selectbox(
            "Payment Regularity",
            options=["always", "sometimes", "rarely"],
            format_func=lambda x: {
                "always":    "Always on time",
                "sometimes": "Sometimes late",
                "rarely":    "Rarely on time",
            }[x],
            index=["always", "sometimes", "rarely"].index(
                st.session_state.get('payment_regularity', 'always')),
        )

    st.markdown('<div class="form-section">Savings & Mobile Money</div>',
                unsafe_allow_html=True)

    has_savings = st.radio(
        "Do you save money regularly?",
        options=[True, False],
        format_func=lambda x:
            "Yes, I save regularly" if x else "No savings currently",
        index=0 if st.session_state.get('has_savings', False) else 1,
        horizontal=True,
    )
    monthly_savings = 0.0
    if has_savings:
        monthly_savings = st.number_input(
            "Monthly Savings Amount (LSL)",
            min_value=0.0, step=100.0,
            value=float(st.session_state.get('monthly_savings', 0)),
        )

    mm_freq = st.selectbox(
        "Mobile Money Usage (M-Pesa, EcoCash, etc.)",
        options=["daily", "weekly", "monthly", "never"],
        format_func=lambda x: {
            "daily":   "Daily",
            "weekly":  "Weekly",
            "monthly": "Monthly",
            "never":   "I don't use mobile money",
        }[x],
        index=["daily", "weekly", "monthly", "never"].index(
            st.session_state.get('mobile_money_frequency', 'weekly')),
    )

    # ── Fixed button row ──────────────────────────────────────────
    st.markdown("<div style='margin-top:1.25rem;'>",
                unsafe_allow_html=True)
    col_back, col_submit = st.columns([1, 1])
    with col_back:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("← Back", key="s3_back",
                     use_container_width=True):
            st.session_state['form_step'] = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_submit:
        if st.button("Calculate My Score →", key="s3_submit",
                     use_container_width=True):
            st.session_state.update({
                'total_debt':             total_debt,
                'num_active_loans':       num_loans,
                'has_defaulted':          has_defaulted,
                'payment_regularity':     payment_reg,
                'has_savings':            has_savings,
                'monthly_savings':        monthly_savings,
                'mobile_money_frequency': mm_freq,
                'form_step':              'submitted',
            })
            st.rerun()


# ── Router ────────────────────────────────────────────────────────
def render_assessment():
    step = st.session_state.get('form_step', 1)
    if step == 1:             render_step1()
    elif step == 2:           render_step2()
    elif step == 3:           render_step3()
    elif step == 'submitted': _run_and_redirect()


def _run_and_redirect():
    from core.service import run_assessment
    from core.schemas import AssessmentInput

    with st.spinner("Analysing your financial profile..."):
        inp = AssessmentInput(
            age                    = st.session_state['age'],
            employment_type        = st.session_state['employment_type'],
            num_dependents         = st.session_state['num_dependents'],
            district               = st.session_state.get(
                                         'district', 'Maseru'),
            monthly_income         = st.session_state['monthly_income'],
            housing_expense        = st.session_state['housing_expense'],
            food_expense           = st.session_state['food_expense'],
            transport_expense      = st.session_state['transport_expense'],
            utilities_expense      = st.session_state['utilities_expense'],
            other_expense          = st.session_state['other_expense'],
            total_debt             = st.session_state['total_debt'],
            num_active_loans       = st.session_state['num_active_loans'],
            has_defaulted          = st.session_state['has_defaulted'],
            payment_regularity     = st.session_state['payment_regularity'],
            has_savings            = st.session_state['has_savings'],
            monthly_savings        = st.session_state['monthly_savings'],
            mobile_money_frequency = st.session_state[
                                         'mobile_money_frequency'],
        )
        result, errors = run_assessment(inp)

    if errors:
        st.error("Please fix the following before continuing:")
        for e in errors:
            st.markdown(f"— {e}")
        st.session_state['form_step'] = 1
        if st.button("← Return to Form"):
            st.rerun()
        return

    st.session_state['result'] = result
    st.session_state['page']   = 'results'
    st.rerun()