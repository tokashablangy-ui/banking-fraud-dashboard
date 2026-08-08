import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Risk Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_parquet(
        "data/investigation_transactions.parquet"
    )
    return df


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
        #101724 0%,
        #171B28 50%,
        #21161B 100%
    );
    border: 1px solid #352633;
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 24px;
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

.status {
    display: inline-block;
    margin-top: 16px;
    padding: 7px 14px;
    border-radius: 999px;
    color: #EB5757;
    background-color: rgba(235,87,87,0.10);
    border: 1px solid rgba(235,87,87,0.30);
    font-weight: 700;
    font-size: 13px;
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
<div class="hero-title">🛡️ Risk Monitoring Center</div>
<div class="hero-subtitle">
Prioritize suspicious transactions, monitor investigation workload,
and surface activity requiring immediate review.
</div>
<div class="status">● Investigation Queue Active</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_investigation = len(df)

high_risk = int(
    (df["risk_level"] == "High Risk").sum()
)

medium_risk = int(
    (df["risk_level"] == "Medium Risk").sum()
)

immediate_review = int(
    (df["review_priority"] == "Immediate Review").sum()
)

fraud_cases = int(
    df["is_fraud"].sum()
)

high_risk_amount = df.loc[
    df["risk_level"] == "High Risk",
    "amt"
].sum()

# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Investigation Queue",
    f"{total_investigation:,}"
)

k2.metric(
    "High-Risk Transactions",
    f"{high_risk:,}"
)

k3.metric(
    "Immediate Review",
    f"{immediate_review:,}"
)

k4.metric(
    "High-Risk Value",
    f"${high_risk_amount / 1_000_000:.2f}M"
)

# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.markdown(
    '<div class="section-title">Current Risk Workload</div>',
    unsafe_allow_html=True
)

risk_counts = (
    df["risk_level"]
    .value_counts()
    .rename_axis("risk_level")
    .reset_index(name="transactions")
)

risk_colors = {
    "High Risk": "#EB5757",
    "Medium Risk": "#F2994A",
    "Low Risk": "#27AE60"
}

left_col, right_col = st.columns([1, 1.5])

with left_col:

    fig_risk = px.pie(
        risk_counts,
        names="risk_level",
        values="transactions",
        hole=0.65,
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
            text="Investigation Risk Mix",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        )
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_col:

    category_risk = (
        df.groupby("category")
        .agg(
            transactions=("trans_num", "count"),
            avg_risk_score=("risk_score", "mean"),
            high_risk_transactions=(
                "risk_level",
                lambda x: (x == "High Risk").sum()
            )
        )
        .reset_index()
    )

    top_categories = (
        category_risk
        .sort_values(
            "high_risk_transactions",
            ascending=True
        )
        .tail(8)
    )

    fig_category = px.bar(
        top_categories,
        x="high_risk_transactions",
        y="category",
        orientation="h"
    )

    fig_category.update_traces(
        marker_color="#EB5757",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "High-Risk Transactions: %{x:,}"
            "<extra></extra>"
        )
    )

    fig_category.update_layout(
        height=390,
        paper_bgcolor="#151E2E",
        plot_bgcolor="#151E2E",
        font=dict(color="#AAB4C3"),
        title=dict(
            text="High-Risk Transactions by Category",
            font=dict(
                color="#FFFFFF",
                size=19
            )
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),
        xaxis=dict(
            title="High-Risk Transactions",
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
# FILTERS
# =========================================================

st.markdown(
    '<div class="section-title">Investigation Filters</div>',
    unsafe_allow_html=True
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    selected_risk = st.selectbox(
        "Risk Level",
        [
            "All",
            "High Risk",
            "Medium Risk"
        ]
    )

with f2:
    selected_priority = st.selectbox(
        "Review Priority",
        [
            "All",
            "Immediate Review",
            "Monitor"
        ]
    )

with f3:
    category_options = sorted(
        df["category"]
        .astype(str)
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        ["All"] + category_options
    )

with f4:
    min_amount = st.number_input(
        "Minimum Amount",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df.copy()

if selected_risk != "All":
    filtered = filtered[
        filtered["risk_level"] == selected_risk
    ]

if selected_priority != "All":
    filtered = filtered[
        filtered["review_priority"] == selected_priority
    ]

if selected_category != "All":
    filtered = filtered[
        filtered["category"].astype(str)
        == selected_category
    ]

filtered = filtered[
    filtered["amt"] >= min_amount
]

# =========================================================
# FILTER SUMMARY
# =========================================================

filtered_high_risk = int(
    (filtered["risk_level"] == "High Risk").sum()
)

filtered_fraud = int(
    filtered["is_fraud"].sum()
)

st.caption(
    f"{len(filtered):,} transactions match the selected filters "
    f"• {filtered_high_risk:,} High Risk "
    f"• {filtered_fraud:,} confirmed fraud cases"
)

# =========================================================
# PRIORITY QUEUE
# =========================================================

st.markdown(
    '<div class="section-title">Priority Investigation Queue</div>',
    unsafe_allow_html=True
)

queue = filtered[
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

queue = queue.sort_values(
    ["risk_score", "amt"],
    ascending=[False, False]
).head(50)

st.dataframe(
    queue,
    use_container_width=True,
    hide_index=True,
    height=600,
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
                "Confirmed Fraud"
            )
    }
)

# =========================================================
# OPERATIONS INSIGHT
# =========================================================

st.warning(
    f"{high_risk:,} transactions are classified as High Risk. "
    "These transactions should receive the highest investigation priority, "
    "especially when combined with large transaction amounts and high-risk categories."
)
