import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Transaction Analysis",
    page_icon="📊",
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
<div class="hero-title">📊 Transaction Analysis</div>
<div class="hero-subtitle">
Explore transaction volume, financial value, timing patterns,
and category-level behavior.
</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# KPIs
# =========================================================

total_transactions = int(
    daily_df["total_transactions"].sum()
)

total_amount = daily_df["total_amount"].sum()

avg_transaction_value = (
    total_amount / total_transactions
)

peak_hour_row = hour_df.loc[
    hour_df["total_transactions"].idxmax()
]

peak_hour = int(
    peak_hour_row["transaction_hour"]
)

peak_hour_transactions = int(
    peak_hour_row["total_transactions"]
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

k2.metric(
    "Transaction Value",
    f"${total_amount / 1_000_000:.1f}M"
)

k3.metric(
    "Average Transaction",
    f"${avg_transaction_value:.2f}"
)

k4.metric(
    "Peak Transaction Hour",
    f"{peak_hour:02d}:00",
    f"{peak_hour_transactions:,} transactions"
)

# =========================================================
# TRANSACTION VOLUME TREND
# =========================================================

st.markdown(
    '<div class="section-title">Transaction Volume Trend</div>',
    unsafe_allow_html=True
)

fig_volume = px.area(
    daily_df,
    x="transaction_date",
    y="total_transactions"
)

fig_volume.update_traces(
    line=dict(
        color="#2F80ED",
        width=2.5
    ),
    fillcolor="rgba(47,128,237,0.16)",
    hovertemplate=(
        "<b>%{x|%d %b %Y}</b><br>"
        "Transactions: %{y:,}"
        "<extra></extra>"
    )
)

fig_volume.update_layout(
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
        title="Transactions",
        gridcolor="rgba(170,180,195,0.10)",
        zeroline=False
    ),
    showlegend=False
)

st.plotly_chart(
    fig_volume,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =========================================================
# HOUR + CATEGORY
# =========================================================

left_col, right_col = st.columns([1, 1.5])

with left_col:

    fig_hour = px.bar(
        hour_df,
        x="transaction_hour",
        y="total_transactions"
    )

    fig_hour.update_traces(
        marker_color="#2F80ED",
        hovertemplate=(
            "Hour: %{x}:00<br>"
            "Transactions: %{y:,}"
            "<extra></extra>"
        )
    )

    fig_hour.update_layout(
        height=380,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Transactions by Hour",
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
            title="Transactions",
            gridcolor="rgba(170,180,195,0.10)"
        )
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_col:

    top_categories_volume = (
        category_df
        .sort_values(
            "total_transactions",
            ascending=True
        )
        .tail(8)
    )

    fig_category_volume = px.bar(
        top_categories_volume,
        x="total_transactions",
        y="category",
        orientation="h"
    )

    fig_category_volume.update_traces(
        marker_color="#27AE60",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Transactions: %{x:,}"
            "<extra></extra>"
        )
    )

    fig_category_volume.update_layout(
        height=380,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="Highest Transaction Categories",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis=dict(
            title="Transactions",
            gridcolor="rgba(170,180,195,0.10)"
        ),
        yaxis=dict(
            title=""
        )
    )

    st.plotly_chart(
        fig_category_volume,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =========================================================
# TRANSACTION VALUE BY CATEGORY
# =========================================================

st.markdown(
    '<div class="section-title">Transaction Value by Category</div>',
    unsafe_allow_html=True
)

value_categories = (
    category_df
    .sort_values(
        "total_amount",
        ascending=False
    )
    .head(10)
)

fig_value = px.bar(
    value_categories,
    x="category",
    y="total_amount"
)

fig_value.update_traces(
    marker_color="#F2994A",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Transaction Value: $%{y:,.2f}"
        "<extra></extra>"
    )
)

fig_value.update_layout(
    height=390,
    paper_bgcolor="#0B1220",
    plot_bgcolor="#151E2E",
    font=dict(color="#AAB4C3"),
    margin=dict(l=30, r=20, t=30, b=50),
    xaxis=dict(
        title="",
        tickangle=-30
    ),
    yaxis=dict(
        title="Transaction Value ($)",
        gridcolor="rgba(170,180,195,0.10)"
    )
)

st.plotly_chart(
    fig_value,
    use_container_width=True,
    config={"displayModeBar": False}
)