import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    create_database,
    register_user,
    login_user,
    add_transaction,
    get_transactions,
    delete_transaction,
    get_all_users,
    get_all_transactions
)

from analytics import calculate_summary
from prediction import predict_next_week


# PAGE CONFIGURATION

st.set_page_config(
    page_title="SmartSpend",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# PROFESSIONAL UI

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fa;
    color: #172033;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #172033 !important;
    font-weight: 700;
    letter-spacing: -0.02em;
}

p {
    color: #667085;
}

hr {
    border: none;
    border-top: 1px solid #e4e7ec;
    margin: 1.5rem 0;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e4e7ec;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

.brand {
    font-size: 1.55rem;
    font-weight: 750;
    color: #172033;
    margin-bottom: 0.15rem;
}

.brand-subtitle {
    font-size: 0.82rem;
    color: #667085;
    margin-bottom: 1.5rem;
}

.sidebar-label {
    color: #98a2b3;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}


/* METRICS */

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 12px;
    padding: 1.1rem;
    box-shadow: 0 2px 5px rgba(16, 24, 40, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #667085 !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #172033 !important;
    font-weight: 700;
}


/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    border-radius: 8px;
    min-height: 42px;
    font-weight: 600;
}


/* INPUTS */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 8px;
}


/* DATAFRAME */

div[data-testid="stDataFrame"] {
    border: 1px solid #e4e7ec;
    border-radius: 10px;
    overflow: hidden;
}


/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 9px;
}


/* LOGIN */

.login-header {
    text-align: center;
    padding: 1rem 0 0.5rem 0;
}

.login-brand {
    font-size: 2.2rem;
    font-weight: 800;
    color: #172033;
}

.login-subtitle {
    color: #667085;
    font-size: 1rem;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}


/* PAGE HEADER */

.page-label {
    color: #667085;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}

.page-description {
    color: #667085;
    margin-top: -0.4rem;
    margin-bottom: 1.2rem;
}


/* INFO CARD */

.info-card {
    background: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(16, 24, 40, 0.03);
}

</style>
""", unsafe_allow_html=True)


# DATABASE

create_database()


# SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# LOGIN / SIGNUP

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="login-header">
            <div class="login-brand">SmartSpend</div>
            <div class="login-subtitle">
                Personal Finance & Expense Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        login_tab, signup_tab = st.tabs(
            ["Login", "Create Account"]
        )

        # LOGIN

        with login_tab:

            st.subheader("Welcome back")

            st.caption(
                "Sign in to continue to your SmartSpend account."
            )

            email = st.text_input(
                "Email",
                key="login_email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
                placeholder="Enter your password"
            )

            st.write("")

            if st.button(
                "Login",
                use_container_width=True
            ):

                if not email or not password:

                    st.error(
                        "Please enter email and password."
                    )

                else:

                    user = login_user(
                        email,
                        password
                    )

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.user_name = user[1]
                        st.session_state.user_email = user[2]

                        if len(user) >= 4:
                            st.session_state.is_admin = bool(user[3])
                        else:
                            st.session_state.is_admin = False

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )


        # SIGNUP

        with signup_tab:

            st.subheader("Create your account")

            st.caption(
                "Create an account to start managing your finances."
            )

            name = st.text_input(
                "Name",
                key="signup_name",
                placeholder="Enter your name"
            )

            email = st.text_input(
                "Email",
                key="signup_email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password",
                placeholder="Minimum 6 characters"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm_password",
                placeholder="Confirm your password"
            )

            st.write("")

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if not name or not email or not password:

                    st.error(
                        "Please fill all fields."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(password) < 6:

                    st.error(
                        "Password must contain at least 6 characters."
                    )

                else:

                    success = register_user(
                        name,
                        email,
                        password
                    )

                    if success:

                        st.success(
                            "Account created successfully. "
                            "You can now login."
                        )

                    else:

                        st.error(
                            "An account with this email already exists."
                        )


# MAIN APPLICATION

else:

    # SIDEBAR

    st.sidebar.markdown(
        '<div class="brand">SmartSpend</div>',
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        '<div class="brand-subtitle">'
        'Personal Finance'
        '</div>',
        unsafe_allow_html=True
    )

    st.sidebar.write(
        f"Welcome, **{st.session_state.user_name}**"
    )

    if st.session_state.is_admin:

        st.sidebar.success(
            "Administrator"
        )

    else:

        st.sidebar.info(
            "User Account"
        )

    st.sidebar.markdown(
        '<div class="sidebar-label">Navigation</div>',
        unsafe_allow_html=True
    )

    navigation_pages = [
        "Dashboard",
        "Add Transaction",
        "Analytics",
        "Prediction",
        "Transaction History"
    ]

    if st.session_state.is_admin:
        navigation_pages.append(
            "Admin Dashboard"
        )

    page = st.sidebar.radio(
        "Go to",
        navigation_pages
    )

    st.sidebar.divider()


    # LOGOUT

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None
        st.session_state.is_admin = False

        st.rerun()


    # GET USER TRANSACTIONS

    df = get_transactions(
        st.session_state.user_id
    )

    if df is None:
        df = pd.DataFrame()


    # CSV DOWNLOAD

    if not df.empty:

        st.sidebar.divider()

        st.sidebar.download_button(
            label="Download My Transactions",
            data=df.to_csv(index=False),
            file_name="smartspend_transactions.csv",
            mime="text/csv",
            use_container_width=True
        )


    # DASHBOARD

    if page == "Dashboard":

        st.markdown(
            '<div class="page-label">Overview</div>',
            unsafe_allow_html=True
        )

        st.title("Financial Dashboard")

        st.markdown(
            f"""
            <div class="page-description">
                Welcome back, {st.session_state.user_name}.
                Here is your current financial overview.
            </div>
            """,
            unsafe_allow_html=True
        )

        income, expenses, balance, savings_rate = (
            calculate_summary(df)
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Income",
            f"₹{income:,.2f}"
        )

        col2.metric(
            "Total Expenses",
            f"₹{expenses:,.2f}"
        )

        col3.metric(
            "Current Balance",
            f"₹{balance:,.2f}"
        )

        col4.metric(
            "Savings Rate",
            f"{savings_rate:.2f}%"
        )

        st.divider()

        if df.empty:

            st.info(
                "No transactions yet. "
                "Add your first transaction to see your "
                "financial overview."
            )

        else:

            if "transaction_type" in df.columns:

                expense_df = df[
                    df["transaction_type"] == "Expense"
                ]

            else:

                expense_df = pd.DataFrame()

            if expense_df.empty:

                st.info(
                    "No expenses available yet."
                )

            else:

                category_data = (
                    expense_df
                    .groupby("category")["amount"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "amount",
                        ascending=False
                    )
                )

                st.subheader(
                    "Spending by Category"
                )

                fig = px.pie(
                    category_data,
                    names="category",
                    values="amount",
                    template="plotly_white",
                    hole=0.35
                )

                fig.update_layout(
                    margin=dict(
                        l=20,
                        r=20,
                        t=40,
                        b=20
                    ),
                    legend_title_text=""
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


    # ADD TRANSACTION

    elif page == "Add Transaction":

        st.markdown(
            '<div class="page-label">Transactions</div>',
            unsafe_allow_html=True
        )

        st.title("Add Transaction")

        st.markdown(
            """
            <div class="page-description">
                Record your income or expenses.
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("transaction_form"):

            col1, col2 = st.columns(2)

            with col1:

                transaction_type = st.selectbox(
                    "Transaction Type",
                    [
                        "Income",
                        "Expense"
                    ]
                )

                amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    step=100.0
                )

                category = st.selectbox(
                    "Category",
                    [
                        "Salary",
                        "Food",
                        "Travel",
                        "Shopping",
                        "Education",
                        "Bills",
                        "Entertainment",
                        "Healthcare",
                        "Pocket Money",
                        "Other"
                    ]
                )

            with col2:

                transaction_date = st.date_input(
                    "Date",
                    date.today()
                )

                description = st.text_input(
                    "Description",
                    placeholder="Enter transaction description"
                )

            st.write("")

            submitted = st.form_submit_button(
                "Add Transaction",
                use_container_width=True
            )

            if submitted:

                if amount <= 0:

                    st.error(
                        "Amount must be greater than zero."
                    )

                else:

                    add_transaction(
                        st.session_state.user_id,
                        transaction_type,
                        amount,
                        category,
                        str(transaction_date),
                        description
                    )

                    st.success(
                        "Transaction added successfully."
                    )


    # ANALYTICS

    elif page == "Analytics":

        st.markdown(
            '<div class="page-label">Insights</div>',
            unsafe_allow_html=True
        )

        st.title("Spending Analytics")

        st.markdown(
            """
            <div class="page-description">
                Understand your spending patterns and trends.
            </div>
            """,
            unsafe_allow_html=True
        )

        if df.empty:

            st.warning(
                "Add transactions to view analytics."
            )

        elif "transaction_type" not in df.columns:

            st.error(
                "Transaction data format is not supported."
            )

        else:

            expense_df = df[
                df["transaction_type"] == "Expense"
            ].copy()

            if expense_df.empty:

                st.info(
                    "No expenses available for analysis."
                )

            else:

                expense_df["date"] = pd.to_datetime(
                    expense_df["date"],
                    errors="coerce"
                )

                # CATEGORY ANALYSIS

                category_data = (
                    expense_df
                    .groupby("category")["amount"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "amount",
                        ascending=False
                    )
                )

                st.subheader(
                    "Expenses by Category"
                )

                fig1 = px.bar(
                    category_data,
                    x="category",
                    y="amount",
                    template="plotly_white"
                )

                fig1.update_layout(
                    xaxis_title="Category",
                    yaxis_title="Amount (₹)",
                    showlegend=False
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )


                # WEEKLY TREND

                expense_df["week"] = (
                    expense_df["date"]
                    .dt.to_period("W")
                    .astype(str)
                )

                weekly_data = (
                    expense_df
                    .groupby("week")["amount"]
                    .sum()
                    .reset_index()
                )

                st.subheader(
                    "Weekly Spending Trend"
                )

                fig2 = px.line(
                    weekly_data,
                    x="week",
                    y="amount",
                    markers=True,
                    template="plotly_white"
                )

                fig2.update_layout(
                    xaxis_title="Week",
                    yaxis_title="Amount (₹)"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )


                # MONTHLY TREND

                expense_df["month"] = (
                    expense_df["date"]
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly_data = (
                    expense_df
                    .groupby("month")["amount"]
                    .sum()
                    .reset_index()
                )

                st.subheader(
                    "Monthly Spending Trend"
                )

                fig3 = px.line(
                    monthly_data,
                    x="month",
                    y="amount",
                    markers=True,
                    template="plotly_white"
                )

                fig3.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Amount (₹)"
                )

                st.plotly_chart(
                    fig3,
                    use_container_width=True
                )


    # PREDICTION

    elif page == "Prediction":

        st.markdown(
            '<div class="page-label">Forecast</div>',
            unsafe_allow_html=True
        )

        st.title(
            "Next Week Spending Prediction"
        )

        st.markdown(
            """
            <div class="page-description">
                Estimate your next week spending using
                your previous spending patterns.
            </div>
            """,
            unsafe_allow_html=True
        )

        if df.empty:

            st.warning(
                "Add some expense transactions first "
                "to generate a prediction."
            )

        else:

            try:

                prediction = predict_next_week(df)

                if prediction is None:

                    st.warning(
                        "Add expenses from at least 2 "
                        "different weeks to generate "
                        "a prediction."
                    )

                else:

                    col1, col2 = st.columns([1, 2])

                    with col1:

                        st.metric(
                            "Estimated Next Week Spending",
                            f"₹{prediction:,.2f}"
                        )

                    with col2:

                        st.info(
                            "This prediction is based on "
                            "your previous weekly spending "
                            "patterns."
                        )

            except Exception as e:

                st.error(
                    "Unable to generate the prediction."
                )

                st.caption(
                    f"Prediction error: {e}"
                )


    # TRANSACTION HISTORY

    elif page == "Transaction History":

        st.markdown(
            '<div class="page-label">Records</div>',
            unsafe_allow_html=True
        )

        st.title(
            "Transaction History"
        )

        st.markdown(
            """
            <div class="page-description">
                View and manage your recorded transactions.
            </div>
            """,
            unsafe_allow_html=True
        )

        if df.empty:

            st.info(
                "You don't have any transactions yet."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader(
                "Delete Transaction"
            )

            id_column = None

            possible_id_columns = [
                "id",
                "transaction_id",
                "ID",
                "Transaction ID"
            ]

            for column in possible_id_columns:

                if column in df.columns:

                    id_column = column
                    break

            if id_column is not None:

                transaction_ids = (
                    pd.to_numeric(
                        df[id_column],
                        errors="coerce"
                    )
                    .dropna()
                    .astype(int)
                    .tolist()
                )

                if transaction_ids:

                    selected_transaction = st.selectbox(
                        "Select Transaction",
                        transaction_ids
                    )

                    if st.button(
                        "Delete Transaction",
                        use_container_width=True
                    ):

                        delete_transaction(
                            selected_transaction,
                            st.session_state.user_id
                        )

                        st.success(
                            "Transaction deleted successfully."
                        )

                        st.rerun()

            else:

                st.warning(
                    "Transaction ID column was not found. "
                    "Your transactions can still be viewed."
                )


    # ADMIN DASHBOARD

    elif page == "Admin Dashboard":

        if not st.session_state.is_admin:

            st.error(
                "Access denied."
            )

            st.stop()

        st.markdown(
            '<div class="page-label">Administration</div>',
            unsafe_allow_html=True
        )

        st.title(
            "Admin Dashboard"
        )

        st.markdown(
            """
            <div class="page-description">
                Monitor users, transactions and overall
                system activity.
            </div>
            """,
            unsafe_allow_html=True
        )

        try:

            users_df = get_all_users()

            all_transactions_df = (
                get_all_transactions()
            )

            if users_df is None:
                users_df = pd.DataFrame()

            if all_transactions_df is None:
                all_transactions_df = pd.DataFrame()

        except Exception as e:

            st.error(
                "Unable to load admin data."
            )

            st.code(
                str(e)
            )

            st.stop()


        # ADMIN SUMMARY

        total_users = len(users_df)

        total_income = 0
        total_expenses = 0

        if not all_transactions_df.empty:

            if "transaction_type" in all_transactions_df.columns:

                income_rows = all_transactions_df[
                    all_transactions_df["transaction_type"]
                    == "Income"
                ]

                expense_rows = all_transactions_df[
                    all_transactions_df["transaction_type"]
                    == "Expense"
                ]

                if "amount" in all_transactions_df.columns:

                    total_income = income_rows[
                        "amount"
                    ].sum()

                    total_expenses = expense_rows[
                        "amount"
                    ].sum()

        total_balance = (
            total_income - total_expenses
        )


        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Users",
            total_users
        )

        col2.metric(
            "Total Income",
            f"₹{total_income:,.2f}"
        )

        col3.metric(
            "Total Expenses",
            f"₹{total_expenses:,.2f}"
        )

        col4.metric(
            "Total Balance",
            f"₹{total_balance:,.2f}"
        )


        st.divider()


        # USERS

        st.subheader(
            "Registered Users"
        )

        if users_df.empty:

            st.info(
                "No registered users found."
            )

        else:

            st.dataframe(
                users_df,
                use_container_width=True,
                hide_index=True
            )


        st.divider()


        # ALL TRANSACTIONS

        st.subheader(
            "All User Transactions"
        )

        if all_transactions_df.empty:

            st.info(
                "No transactions found."
            )

        else:

            admin_df = (
                all_transactions_df.copy()
            )


            # USER FILTER

            if "user_name" in admin_df.columns:

                user_options = (
                    ["All Users"]
                    +
                    sorted(
                        admin_df["user_name"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )
                )

                selected_user = st.selectbox(
                    "Filter by User",
                    user_options
                )

                if selected_user != "All Users":

                    admin_df = admin_df[
                        admin_df["user_name"].astype(str)
                        == selected_user
                    ]


            # TRANSACTION TYPE FILTER

            if "transaction_type" in admin_df.columns:

                type_options = [
                    "All",
                    "Income",
                    "Expense"
                ]

                selected_type = st.selectbox(
                    "Filter by Transaction Type",
                    type_options
                )

                if selected_type != "All":

                    admin_df = admin_df[
                        admin_df["transaction_type"]
                        == selected_type
                    ]


            st.dataframe(
                admin_df,
                use_container_width=True,
                hide_index=True
            )


            st.download_button(
                label="Download All Transaction Data",
                data=admin_df.to_csv(
                    index=False
                ),
                file_name=(
                    "smartspend_admin_transactions.csv"
                ),
                mime="text/csv"
            )


        st.divider()


        # USER-WISE EXPENSES

        if not all_transactions_df.empty:

            if (
                "user_name" in all_transactions_df.columns
                and
                "transaction_type" in all_transactions_df.columns
                and
                "amount" in all_transactions_df.columns
            ):

                expense_admin_df = (
                    all_transactions_df[
                        all_transactions_df[
                            "transaction_type"
                        ] == "Expense"
                    ]
                )

                if not expense_admin_df.empty:

                    st.subheader(
                        "User-wise Expenses"
                    )

                    user_expenses = (
                        expense_admin_df
                        .groupby("user_name")["amount"]
                        .sum()
                        .reset_index()
                        .sort_values(
                            "amount",
                            ascending=False
                        )
                    )

                    fig_admin = px.bar(
                        user_expenses,
                        x="user_name",
                        y="amount",
                        template="plotly_white"
                    )

                    fig_admin.update_layout(
                        xaxis_title="User",
                        yaxis_title="Expenses (₹)",
                        showlegend=False
                    )

                    st.plotly_chart(
                        fig_admin,
                        use_container_width=True
                    )


        # CATEGORY ANALYSIS

        if not all_transactions_df.empty:

            required_columns = [
                "transaction_type",
                "category",
                "amount"
            ]

            if all(
                column in all_transactions_df.columns
                for column in required_columns
            ):

                expense_admin_df = (
                    all_transactions_df[
                        all_transactions_df[
                            "transaction_type"
                        ] == "Expense"
                    ]
                )

                if not expense_admin_df.empty:

                    st.subheader(
                        "Overall Spending by Category"
                    )

                    category_admin = (
                        expense_admin_df
                        .groupby("category")["amount"]
                        .sum()
                        .reset_index()
                        .sort_values(
                            "amount",
                            ascending=False
                        )
                    )

                    fig_category = px.pie(
                        category_admin,
                        names="category",
                        values="amount",
                        template="plotly_white",
                        hole=0.35
                    )

                    fig_category.update_layout(
                        margin=dict(
                            l=20,
                            r=20,
                            t=40,
                            b=20
                        ),
                        legend_title_text=""
                    )

                    st.plotly_chart(
                        fig_category,
                        use_container_width=True
                    )
