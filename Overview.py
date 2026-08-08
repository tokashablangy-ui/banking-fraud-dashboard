import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    daily = pd.read_parquet("data/daily_summary.parquet")
    category = pd.read_parquet("data/category_summary.parquet")
    risk = pd.read_parquet("data/risk_summary.parquet")
    investigation = pd.read_parquet(
        "data/investigation_transactions.parquet"
    )

    return daily, category, risk, investigation


daily_df, category_df, risk_df, investigation_df = load_data()

daily_df["transaction_date"] = pd.to_datetime(
    daily_df["transaction_date"]
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Fraud Intelligence Center",
    page_icon="💳",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    daily = pd.read_parquet("data/daily_summary.parquet")
    category = pd.read_parquet("data/category_summary.parquet")
    risk = pd.read_parquet("data/risk_summary.parquet")
    investigation = pd.read_parquet(
        "data/investigation_transactions.parquet"
    )
    return daily, category, risk, investigation


daily_df, category_df, risk_df, investigation_df = load_data()

daily_df["transaction_date"] = pd.to_datetime(
    daily_df["transaction_date"]
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_transactions = int(
    daily_df["total_transactions"].sum()
)

total_amount = daily_df["total_amount"].sum()

fraud_transactions = int(
    daily_df["fraud_transactions"].sum()
)

fraud_amount = daily_df["fraud_amount"].sum()

fraud_rate = (
    fraud_transactions / total_transactions * 100
)

high_risk_transactions = int(
    risk_df.loc[
        risk_df["risk_level"] == "High Risk",
        "total_transactions"
    ].sum()
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1220;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}

.hero {
    background: linear-gradient(
        120deg,
        #111A2A 0%,
        #151E2E 55%,
        #101827 100%
    );
    border: 1px solid #26344A;
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 26px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.20);
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 6px;
}

.hero-subtitle {
    color: #AAB4C3;
    font-size: 16px;
}

.status {
    display: inline-block;
    margin-top: 18px;
    padding: 8px 15px;
    border-radius: 999px;
    background-color: rgba(39,174,96,0.12);
    border: 1px solid rgba(39,174,96,0.35);
    color: #5DDB8B;
    font-size: 13px;
    font-weight: 700;
}

.kpi-card {
    background-color: #151E2E;
    border: 1px solid #26344A;
    border-radius: 18px;
    padding: 20px;
    min-height: 128px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.18);
    transition: transform 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
}

.kpi-label {
    color: #AAB4C3;
    font-size: 13px;
    margin-bottom: 10px;
}

.kpi-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: 800;
}

.kpi-blue {
    border-top: 3px solid #2F80ED;
}

.kpi-red {
    border-top: 3px solid #EB5757;
}

.kpi-orange {
    border-top: 3px solid #F2994A;
}

.kpi-green {
    border-top: 3px solid #27AE60;
}

.section-title {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 750;
    margin-top: 32px;
    margin-bottom: 8px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #26344A;
    border-radius: 14px;
    overflow: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-title">🛡️ Fraud Intelligence Center</div>
<div class="hero-subtitle">
Monitor transactions, detect suspicious behavior, and prioritize financial risk.
</div>
<div class="status">● Risk Engine Active</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
<div class="kpi-card kpi-blue">
<div class="kpi-label">TOTAL TRANSACTIONS</div>
<div class="kpi-value">{total_transactions:,}</div>
</div>
""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
<div class="kpi-card kpi-green">
<div class="kpi-label">TOTAL TRANSACTION VALUE</div>
<div class="kpi-value">${total_amount / 1_000_000:.1f}M</div>
</div>
""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
<div class="kpi-card kpi-red">
<div class="kpi-label">FRAUDULENT TRANSACTIONS</div>
<div class="kpi-value">{fraud_transactions:,}</div>
</div>
""",
        unsafe_allow_html=True
    )

st.write("")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(
        f"""
<div class="kpi-card kpi-orange">
<div class="kpi-label">FRAUD RATE</div>
<div class="kpi-value">{fraud_rate:.2f}%</div>
</div>
""",
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
<div class="kpi-card kpi-red">
<div class="kpi-label">FRAUD EXPOSURE</div>
<div class="kpi-value">${fraud_amount / 1_000_000:.2f}M</div>
</div>
""",
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
<div class="kpi-card kpi-orange">
<div class="kpi-label">HIGH-RISK TRANSACTIONS</div>
<div class="kpi-value">{high_risk_transactions:,}</div>
</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Fraud Operations Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    "Monitor fraud trends, risk concentration, "
    "high-risk categories, and investigation activity."
)

# =========================================================
# FRAUD TREND
# =========================================================

fig_trend = px.area(
    daily_df,
    x="transaction_date",
    y="fraud_transactions"
)

fig_trend.update_traces(
    line=dict(
        color="#2F80ED",
        width=2.5
    ),
    fillcolor="rgba(47,128,237,0.18)",
    hovertemplate=(
        "<b>%{x|%d %b %Y}</b><br>"
        "Fraud Cases: %{y:,}"
        "<extra></extra>"
    )
)

fig_trend.update_layout(
    height=420,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#151E2E",
    font=dict(
        color="#AAB4C3",
        size=12
    ),
    title=dict(
        text="Fraud Activity Trend",
        font=dict(
            color="#FFFFFF",
            size=20
        ),
        x=0.01
    ),
    margin=dict(
        l=30,
        r=20,
        t=70,
        b=30
    ),
    hovermode="x unified",
    xaxis=dict(
        title="",
        showgrid=False,
        linecolor="#26344A"
    ),
    yaxis=dict(
        title="Fraud Cases",
        gridcolor="rgba(170,180,195,0.10)",
        zeroline=False
    ),
    showlegend=False
)

st.plotly_chart(
    fig_trend,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =========================================================
# RISK DISTRIBUTION + CATEGORIES
# =========================================================

left_col, right_col = st.columns([1, 1.6])

with left_col:

    risk_colors = {
        "High Risk": "#EB5757",
        "Medium Risk": "#F2994A",
        "Low Risk": "#27AE60"
    }

    fig_risk = px.pie(
        risk_df,
        names="risk_level",
        values="total_transactions",
        hole=0.68,
        color="risk_level",
        color_discrete_map=risk_colors
    )

    fig_risk.update_traces(
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Transactions: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig_risk.update_layout(
        height=390,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Risk Distribution",
            font=dict(
                color="#FFFFFF",
                size=19
            ),
            x=0.05
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),
        legend=dict(
            orientation="h",
            y=-0.08,
            x=0.05
        )
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_col:

    top_categories = (
        category_df
        .sort_values(
            "fraud_rate",
            ascending=True
        )
        .tail(7)
    )

    fig_categories = px.bar(
        top_categories,
        x="fraud_rate",
        y="category",
        orientation="h"
    )

    fig_categories.update_traces(
        marker_color="#EB5757",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Fraud Rate: %{x:.2f}%"
            "<extra></extra>"
        )
    )

    fig_categories.update_layout(
        height=390,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Highest-Risk Categories",
            font=dict(
                color="#FFFFFF",
                size=19
            ),
            x=0.03
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),
        xaxis=dict(
            title="Fraud Rate (%)",
            gridcolor="rgba(170,180,195,0.10)"
        ),
        yaxis=dict(
            title=""
        )
    )

    st.plotly_chart(
        fig_categories,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =========================================================
# INVESTIGATION QUEUE
# =========================================================

st.markdown(
    '<div class="section-title">Investigation Queue</div>',
    unsafe_allow_html=True
)

st.caption(
    "Prioritized transactions requiring investigation "
    "based on risk score and transaction characteristics."
)

# =========================================================
# FILTERS
# =========================================================

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    selected_risk = st.selectbox(
        "Risk Level",
        [
            "All",
            "High Risk",
            "Medium Risk"
        ]
    )

with filter_col2:

    category_options = (
        investigation_df["category"]
        .astype(str)
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted(category_options)
    )

with filter_col3:

    min_amount = st.number_input(
        "Minimum Amount",
        min_value=0.0,
        value=0.0,
        step=50.0
    )

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_investigation = investigation_df.copy()

if selected_risk != "All":
    filtered_investigation = filtered_investigation[
        filtered_investigation["risk_level"]
        == selected_risk
    ]

if selected_category != "All":
    filtered_investigation = filtered_investigation[
        filtered_investigation["category"].astype(str)
        == selected_category
    ]

filtered_investigation = filtered_investigation[
    filtered_investigation["amt"] >= min_amount
]

st.caption(
    f"{len(filtered_investigation):,} transactions "
    "match the selected filters."
)

# =========================================================
# TABLE
# =========================================================

investigation_view = filtered_investigation[
    [
        "trans_num",
        "customer_name",
        "merchant",
        "category",
        "amt",
        "transaction_hour",
        "risk_score",
        "risk_level",
        "review_priority",
        "is_fraud"
    ]
].copy()

investigation_view = investigation_view.sort_values(
    ["risk_score", "amt"],
    ascending=[False, False]
)

investigation_view = investigation_view.head(20)

st.dataframe(
    investigation_view,
    use_container_width=True,
    hide_index=True,
    height=510,
    column_config={
        "trans_num":
            st.column_config.TextColumn(
                "Transaction ID"
            ),

        "customer_name":
            st.column_config.TextColumn(
                "Customer"
            ),

        "merchant":
            st.column_config.TextColumn(
                "Merchant"
            ),

        "category":
            st.column_config.TextColumn(
                "Category"
            ),

        "amt":
            st.column_config.NumberColumn(
                "Amount",
                format="$%.2f"
            ),

        "transaction_hour":
            st.column_config.NumberColumn(
                "Hour"
            ),

        "risk_score":
            st.column_config.ProgressColumn(
                "Risk Score",
                min_value=0,
                max_value=100,
                format="%d"
            ),

        "risk_level":
            st.column_config.TextColumn(
                "Risk Level"
            ),

        "review_priority":
            st.column_config.TextColumn(
                "Review Priority"
            ),

        "is_fraud":
            st.column_config.NumberColumn(
                "Fraud"
            )
    }
)