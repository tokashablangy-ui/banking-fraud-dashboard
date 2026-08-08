import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fraud Analysis",
    page_icon="🚨",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    daily = pd.read_parquet("data/daily_summary.parquet")
    category = pd.read_parquet("data/category_summary.parquet")
    hour = pd.read_parquet("data/hour_summary.parquet")
    risk = pd.read_parquet("data/risk_summary.parquet")
    return daily, category, hour, risk


daily_df, category_df, hour_df, risk_df = load_data()

daily_df["transaction_date"] = pd.to_datetime(
    daily_df["transaction_date"]
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

fraud_transactions = int(
    daily_df["fraud_transactions"].sum()
)

fraud_amount = daily_df["fraud_amount"].sum()

total_transactions = int(
    daily_df["total_transactions"].sum()
)

fraud_rate = (
    fraud_transactions / total_transactions * 100
)

avg_fraud_amount = (
    fraud_amount / fraud_transactions
)

highest_risk_category = (
    category_df
    .sort_values("fraud_rate", ascending=False)
    .iloc[0]["category"]
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
        #171321 0%,
        #201522 50%,
        #121725 100%
    );
    border: 1px solid #3A2732;
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
<div class="hero-title">🚨 Fraud Analysis</div>
<div class="hero-subtitle">
Analyze fraud concentration, exposure, timing patterns,
and the segments carrying the highest financial risk.
</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# KPIs
# =========================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Fraud Transactions",
    f"{fraud_transactions:,}"
)

k2.metric(
    "Fraud Rate",
    f"{fraud_rate:.2f}%"
)

k3.metric(
    "Fraud Exposure",
    f"${fraud_amount / 1_000_000:.2f}M"
)

k4.metric(
    "Average Fraud Transaction",
    f"${avg_fraud_amount:,.2f}"
)

# =========================================================
# DAILY FRAUD TREND
# =========================================================

st.markdown(
    '<div class="section-title">Fraud Activity Over Time</div>',
    unsafe_allow_html=True
)

fig_daily = px.area(
    daily_df,
    x="transaction_date",
    y="fraud_transactions"
)

fig_daily.update_traces(
    line=dict(
        color="#EB5757",
        width=2.5
    ),
    fillcolor="rgba(235,87,87,0.18)",
    hovertemplate=(
        "<b>%{x|%d %b %Y}</b><br>"
        "Fraud Cases: %{y:,}"
        "<extra></extra>"
    )
)

fig_daily.update_layout(
    height=400,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#151E2E",
    font=dict(color="#AAB4C3"),
    margin=dict(l=30, r=20, t=30, b=30),
    xaxis=dict(
        title="",
        showgrid=False
    ),
    yaxis=dict(
        title="Fraud Cases",
        gridcolor="rgba(170,180,195,0.10)",
        zeroline=False
    ),
    showlegend=False
)

st.plotly_chart(
    fig_daily,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =========================================================
# FRAUD BY HOUR + CATEGORY
# =========================================================

left_col, right_col = st.columns([1, 1.5])

with left_col:

    fig_hour = px.line(
        hour_df,
        x="transaction_hour",
        y="fraud_rate",
        markers=True
    )

    fig_hour.update_traces(
        line=dict(
            color="#F2994A",
            width=3
        ),
        marker=dict(size=7),
        hovertemplate=(
            "Hour: %{x}:00<br>"
            "Fraud Rate: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig_hour.update_layout(
        height=380,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Fraud Rate by Hour",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis=dict(
            title="Hour",
            dtick=2
        ),
        yaxis=dict(
            title="Fraud Rate (%)",
            gridcolor="rgba(170,180,195,0.10)"
        )
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_col:

    top_fraud_categories = (
        category_df
        .sort_values(
            "fraud_rate",
            ascending=True
        )
        .tail(8)
    )

    fig_category = px.bar(
        top_fraud_categories,
        x="fraud_rate",
        y="category",
        orientation="h"
    )

    fig_category.update_traces(
        marker_color="#EB5757",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Fraud Rate: %{x:.2f}%"
            "<extra></extra>"
        )
    )

    fig_category.update_layout(
        height=380,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Highest Fraud Categories",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis=dict(
            title="Fraud Rate (%)",
            gridcolor="rgba(170,180,195,0.10)"
        ),
        yaxis=dict(
            title=""
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =========================================================
# FRAUD BY RISK LEVEL
# =========================================================

st.markdown(
    '<div class="section-title">Fraud Concentration by Risk Level</div>',
    unsafe_allow_html=True
)

risk_order = [
    "Low Risk",
    "Medium Risk",
    "High Risk"
]

risk_plot = risk_df.copy()

risk_plot["risk_level"] = pd.Categorical(
    risk_plot["risk_level"],
    categories=risk_order,
    ordered=True
)

risk_plot = risk_plot.sort_values("risk_level")

fig_risk = px.bar(
    risk_plot,
    x="risk_level",
    y="fraud_rate"
)

fig_risk.update_traces(
    marker_color=[
        "#27AE60",
        "#F2994A",
        "#EB5757"
    ],
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Fraud Rate: %{y:.2f}%"
        "<extra></extra>"
    )
)

fig_risk.update_layout(
    height=370,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#151E2E",
    font=dict(color="#AAB4C3"),
    margin=dict(l=30, r=20, t=30, b=30),
    xaxis=dict(
        title=""
    ),
    yaxis=dict(
        title="Fraud Rate (%)",
        gridcolor="rgba(170,180,195,0.10)"
    )
)

st.plotly_chart(
    fig_risk,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =========================================================
# INSIGHT
# =========================================================

st.info(
    f"Highest-risk category: {highest_risk_category}. "
    "Fraud activity is strongly concentrated in high-risk transactions "
    "and late-night transaction periods."
)
