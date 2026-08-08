import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer & Merchant Risk",
    page_icon="👥",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    investigation = pd.read_parquet(
        "data/investigation_transactions.parquet"
    )
    return investigation


df = load_data()

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
    padding: 28px 32px;
    margin-bottom: 25px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 800;
}

.hero-subtitle {
    color: #AAB4C3;
    font-size: 15px;
    margin-top: 5px;
}

.section-title {
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 750;
    margin-top: 28px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-title">👥 Customer & Merchant Risk</div>
<div class="hero-subtitle">
Identify customers, merchants, and transaction segments associated
with elevated fraud and risk exposure.
</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# PREPARE SUMMARIES
# =========================================================

merchant_summary = (
    df.groupby("merchant")
    .agg(
        transactions=("trans_num", "count"),
        avg_risk_score=("risk_score", "mean"),
        total_amount=("amt", "sum"),
        fraud_transactions=("is_fraud", "sum")
    )
    .reset_index()
)

merchant_summary["fraud_rate"] = (
    merchant_summary["fraud_transactions"]
    / merchant_summary["transactions"]
    * 100
)

customer_summary = (
    df.groupby(["cc_num", "customer_name"])
    .agg(
        transactions=("trans_num", "count"),
        avg_risk_score=("risk_score", "mean"),
        total_amount=("amt", "sum"),
        fraud_transactions=("is_fraud", "sum")
    )
    .reset_index()
)

customer_summary["fraud_rate"] = (
    customer_summary["fraud_transactions"]
    / customer_summary["transactions"]
    * 100
)

# =========================================================
# KPIs
# =========================================================

elevated_risk_merchants = (
    merchant_summary["avg_risk_score"] >= 45
).sum()

high_risk_customers = (
    customer_summary["avg_risk_score"] >= 60
).sum()

highest_merchant_risk = (
    merchant_summary["avg_risk_score"].max()
)

highest_customer_risk = (
    customer_summary["avg_risk_score"].max()
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Elevated-Risk Merchants",
    f"{elevated_risk_merchants:,}"
)

k2.metric(
    "High-Risk Customers",
    f"{high_risk_customers:,}"
)

k3.metric(
    "Highest Merchant Risk",
    f"{highest_merchant_risk:.1f}"
)

k4.metric(
    "Highest Customer Risk",
    f"{highest_customer_risk:.1f}"
)

# =========================================================
# MERCHANT ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">Merchant Risk Analysis</div>',
    unsafe_allow_html=True
)

left_col, right_col = st.columns([1.3, 1])

with left_col:

    top_merchants = (
        merchant_summary
        .sort_values(
            "avg_risk_score",
            ascending=True
        )
        .tail(10)
    )

    fig_merchants = px.bar(
        top_merchants,
        x="avg_risk_score",
        y="merchant",
        orientation="h"
    )

    fig_merchants.update_traces(
        marker_color="#EB5757",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average Risk Score: %{x:.2f}"
            "<extra></extra>"
        )
    )

    fig_merchants.update_layout(
        height=420,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Highest-Risk Merchants",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis=dict(
            title="Average Risk Score",
            gridcolor="rgba(170,180,195,0.10)"
        ),
        yaxis=dict(
            title=""
        )
    )

    st.plotly_chart(
        fig_merchants,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_col:

    merchant_fraud = (
        merchant_summary
        .sort_values(
            "fraud_rate",
            ascending=False
        )
        .head(8)
    )

    fig_fraud = px.bar(
        merchant_fraud,
        x="merchant",
        y="fraud_rate"
    )

    fig_fraud.update_traces(
        marker_color="#F2994A",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Fraud Rate: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig_fraud.update_layout(
        height=420,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Highest Merchant Fraud Rates",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(l=20, r=20, t=60, b=80),
        xaxis=dict(
            title="",
            tickangle=-35
        ),
        yaxis=dict(
            title="Fraud Rate (%)",
            gridcolor="rgba(170,180,195,0.10)"
        )
    )

    st.plotly_chart(
        fig_fraud,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">Customer Risk Analysis</div>',
    unsafe_allow_html=True
)

top_customers = (
    customer_summary
    .sort_values(
        ["avg_risk_score", "total_amount"],
        ascending=[False, False]
    )
    .head(10)
)

fig_customers = px.scatter(
    top_customers,
    x="total_amount",
    y="avg_risk_score",
    size="transactions",
    hover_name="customer_name"
)

fig_customers.update_traces(
    marker=dict(
        color="#2F80ED",
        opacity=0.8,
        line=dict(
            width=1,
            color="#FFFFFF"
        )
    )
)

fig_customers.update_layout(
    height=420,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#151E2E",
    font=dict(color="#AAB4C3"),
    title=dict(
        text="High-Risk Customer Exposure",
        font=dict(
            color="#FFFFFF",
            size=19
        )
    ),
    margin=dict(l=30, r=20, t=60, b=30),
    xaxis=dict(
        title="Total Transaction Amount ($)",
        gridcolor="rgba(170,180,195,0.10)"
    ),
    yaxis=dict(
        title="Average Risk Score",
        gridcolor="rgba(170,180,195,0.10)"
    )
)

st.plotly_chart(
    fig_customers,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =========================================================
# RISK WATCHLIST
# =========================================================

st.markdown(
    '<div class="section-title">Risk Watchlist</div>',
    unsafe_allow_html=True
)

watchlist = merchant_summary[
    [
        "merchant",
        "transactions",
        "avg_risk_score",
        "fraud_transactions",
        "fraud_rate",
        "total_amount"
    ]
].copy()

watchlist = watchlist.sort_values(
    ["avg_risk_score", "fraud_rate"],
    ascending=[False, False]
).head(20)

st.dataframe(
    watchlist,
    use_container_width=True,
    hide_index=True,
    height=500,
    column_config={
        "merchant":
            st.column_config.TextColumn(
                "Merchant"
            ),

        "transactions":
            st.column_config.NumberColumn(
                "Transactions",
                format="%d"
            ),

        "avg_risk_score":
            st.column_config.ProgressColumn(
                "Average Risk Score",
                min_value=0,
                max_value=100,
                format="%.1f"
            ),

        "fraud_transactions":
            st.column_config.NumberColumn(
                "Fraud Cases",
                format="%d"
            ),

        "fraud_rate":
            st.column_config.NumberColumn(
                "Fraud Rate",
                format="%.2f%%"
            ),

        "total_amount":
            st.column_config.NumberColumn(
                "Transaction Value",
                format="$%.2f"
            )
    }
)
