import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Insights & Recommendations",
    page_icon="💡",
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

# =========================================================
# CALCULATIONS
# =========================================================

total_transactions = int(
    daily_df["total_transactions"].sum()
)

fraud_transactions = int(
    daily_df["fraud_transactions"].sum()
)

fraud_amount = daily_df["fraud_amount"].sum()

fraud_rate = (
    fraud_transactions
    / total_transactions
    * 100
)

top_category_row = (
    category_df
    .sort_values("fraud_rate", ascending=False)
    .iloc[0]
)

top_category = top_category_row["category"]
top_category_rate = top_category_row["fraud_rate"]

top_hour_row = (
    hour_df
    .sort_values("fraud_rate", ascending=False)
    .iloc[0]
)

top_hour = int(top_hour_row["transaction_hour"])
top_hour_rate = top_hour_row["fraud_rate"]

high_risk_row = risk_df[
    risk_df["risk_level"] == "High Risk"
].iloc[0]

high_risk_transactions = int(
    high_risk_row["total_transactions"]
)

high_risk_fraud = int(
    high_risk_row["fraud_transactions"]
)

high_risk_capture = (
    high_risk_fraud
    / fraud_transactions
    * 100
)

high_risk_share = (
    high_risk_transactions
    / total_transactions
    * 100
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
    max-width: 1450px;
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
    margin-bottom: 28px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 800;
}

.hero-subtitle {
    color: #AAB4C3;
    font-size: 15px;
    margin-top: 6px;
}

.section-title {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 750;
    margin-top: 30px;
    margin-bottom: 12px;
}

.insight-card {
    background-color: #151E2E;
    border: 1px solid #26344A;
    border-radius: 18px;
    padding: 22px;
    min-height: 180px;
}

.insight-number {
    font-size: 27px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.insight-label {
    color: #AAB4C3;
    font-size: 13px;
    margin-bottom: 12px;
}

.insight-text {
    color: #D7DCE5;
    font-size: 14px;
    line-height: 1.6;
}

.recommendation-card {
    background-color: #151E2E;
    border-left: 4px solid #2F80ED;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

.recommendation-title {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
}

.recommendation-text {
    color: #AAB4C3;
    font-size: 14px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-title">💡 Insights & Recommendations</div>
<div class="hero-subtitle">
Translate fraud analytics into practical actions for Risk,
Fraud Investigation, and decision-making teams.
</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# EXECUTIVE INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">Executive Insights</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
<div class="insight-card">
<div class="insight-label">FRAUD FINANCIAL EXPOSURE</div>
<div class="insight-number">${fraud_amount / 1_000_000:.2f}M</div>
<div class="insight-text">
Fraud represents only {fraud_rate:.2f}% of all transactions,
but the associated financial exposure exceeds five million dollars.
</div>
</div>
""",
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
<div class="insight-card">
<div class="insight-label">CRITICAL TIME WINDOW</div>
<div class="insight-number">{top_hour:02d}:00</div>
<div class="insight-text">
The highest fraud rate occurs around {top_hour:02d}:00,
reaching approximately {top_hour_rate:.2f}% of transactions
during that hour.
</div>
</div>
""",
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
<div class="insight-card">
<div class="insight-label">HIGHEST-RISK CATEGORY</div>
<div class="insight-number">{top_category}</div>
<div class="insight-text">
This category records the highest fraud rate in the dataset
at approximately {top_category_rate:.2f}%.
</div>
</div>
""",
        unsafe_allow_html=True
    )

st.write("")

c4, c5 = st.columns(2)

with c4:
    st.markdown(
        f"""
<div class="insight-card">
<div class="insight-label">RISK PRIORITIZATION EFFECTIVENESS</div>
<div class="insight-number">{high_risk_capture:.1f}% Fraud Captured</div>
<div class="insight-text">
Only {high_risk_share:.1f}% of all transactions are classified
as High Risk, yet this segment captures approximately
{high_risk_capture:.1f}% of all detected fraud cases.
</div>
</div>
""",
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        """
<div class="insight-card">
<div class="insight-label">GEOGRAPHIC SIGNAL</div>
<div class="insight-number">Weak Standalone Signal</div>
<div class="insight-text">
Customer-to-merchant distance showed limited separation between
fraudulent and legitimate transactions, so geographic distance
should be combined with stronger behavioral indicators.
</div>
</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# BUSINESS STORY
# =========================================================

st.markdown(
    '<div class="section-title">What the Analysis Tells Us</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
The fraud landscape in this transaction history is not defined by
volume alone.

Although only **{fraud_rate:.2f}%** of all transactions were classified
as fraudulent, those transactions created approximately
**${fraud_amount / 1_000_000:.2f}M in financial exposure**.

The analysis also shows that fraud is not randomly distributed.
Risk increases during specific late-night hours and within particular
transaction categories.

Most importantly, the risk-scoring framework successfully concentrates
a large share of detected fraud into a relatively small segment of
transactions. This allows investigation teams to shift from reviewing
every transaction equally toward a more focused **risk-based workflow**.
"""
)

# =========================================================
# RECOMMENDATIONS
# =========================================================

st.markdown(
    '<div class="section-title">Business Recommendations</div>',
    unsafe_allow_html=True
)

recommendations = [
    (
        "1. Prioritize High-Risk Transactions",
        "Route High-Risk transactions to the top of the investigation queue. "
        "This segment contains a disproportionate share of confirmed fraud "
        "and offers the greatest opportunity to reduce manual review effort."
    ),
    (
        "2. Strengthen Late-Night Monitoring",
        "Apply increased monitoring during late-night and early-morning hours, "
        "particularly around the periods identified with the highest fraud rates."
    ),
    (
        "3. Apply Category-Specific Controls",
        "Introduce stronger verification and review rules for high-risk categories "
        "such as online shopping and other transaction types showing elevated fraud exposure."
    ),
    (
        "4. Use Multi-Signal Risk Decisions",
        "Do not depend on one factor alone. Combine transaction amount, transaction hour, "
        "category, customer characteristics, and behavioral signals when assigning risk."
    ),
    (
        "5. Continuously Revalidate Risk Rules",
        "Fraud behavior changes over time. Risk thresholds and rule weights should be "
        "periodically reviewed against new transaction data."
    ),
    (
        "6. Extend the Framework with Machine Learning",
        "The current rule-based framework provides transparent prioritization. "
        "A machine-learning model can later be introduced as a second risk signal "
        "and compared against the existing business rules."
    )
]

for title, text in recommendations:
    st.markdown(
        f"""
<div class="recommendation-card">
<div class="recommendation-title">{title}</div>
<div class="recommendation-text">{text}</div>
</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# BUSINESS IMPACT
# =========================================================

st.markdown(
    '<div class="section-title">Business Impact</div>',
    unsafe_allow_html=True
)

impact1, impact2, impact3, impact4 = st.columns(4)

impact1.metric(
    "Transactions Monitored",
    f"{total_transactions / 1_000_000:.2f}M"
)

impact2.metric(
    "Fraud Cases Detected",
    f"{fraud_transactions:,}"
)

impact3.metric(
    "High-Risk Segment",
    f"{high_risk_share:.1f}%"
)

impact4.metric(
    "Fraud Captured",
    f"{high_risk_capture:.1f}%"
)

st.success(
    "Risk-based monitoring enables investigation teams to focus on the "
    "transactions that matter most, supporting faster review, better "
    "prioritization, and stronger fraud visibility."
)
