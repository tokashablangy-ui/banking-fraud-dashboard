# 💳 Banking Fraud & Transaction Risk Dashboard

A professional interactive web dashboard for monitoring banking transactions, identifying suspicious activity, prioritizing high-risk operations, and supporting fraud investigation teams with data-driven insights.

---

## 🚀 Project Overview

This project analyzes more than **1.85 million financial transactions** to uncover fraud patterns, assess transaction risk, and provide an operational investigation workflow.

The dashboard was built as a lightweight fraud intelligence system that transforms raw transaction data into actionable insights for Risk, Fraud Investigation, and Banking Security teams.

---

## 🎯 Business Problem

Fraud investigation teams often deal with very large transaction volumes, making it difficult to manually review every transaction.

The main goal of this project is to:

- Detect suspicious transaction patterns
- Identify high-risk transaction categories and time periods
- Prioritize transactions requiring investigation
- Reduce unnecessary manual review
- Provide management with a clear fraud monitoring view

---

## 📊 Dataset

Source: Kaggle Fraud Detection Dataset

Main files used:

- `fraudTrain.csv`
- `fraudTest.csv`

Combined analytical dataset:

- **1,852,394 Transactions**
- **9,651 Fraudulent Transactions**
- **$129.8M Transaction Value**
- **$5.12M Fraudulent Amount**
- **0.52% Fraud Rate**

---

## 🧹 Data Preparation

The preprocessing workflow included:

- Removing unnecessary columns
- Datetime conversion
- Data type optimization
- Missing value validation
- Duplicate transaction validation
- Feature engineering
- Risk scoring
- Train/Test validation
- Dashboard-ready analytical data layers

---

## ⚙️ Feature Engineering

Several analytical features were created, including:

- Transaction Date
- Transaction Hour
- Day of Week
- Month
- Weekend Indicator
- Transaction Period
- Customer Age
- Age Group
- Customer-Merchant Distance
- Risk Score
- Risk Level
- Review Priority

---

## 🛡️ Risk Scoring Framework

The dashboard uses a transparent **Business Rule-Based Risk Prioritization Framework**.

Risk signals include:

- High transaction amount
- High-risk transaction hours
- High-risk transaction categories
- Customer age group
- Customer-to-merchant distance

Transactions are classified into:

- 🟢 Low Risk
- 🟠 Medium Risk
- 🔴 High Risk

> The Risk Score is a business rule-based prioritization system and is not presented as a machine learning prediction model.

---

## 🔍 Risk Scoring Validation

### Training Data

| Risk Level | Fraud Rate |
|---|---:|
| Low Risk | 0.14% |
| Medium Risk | 1.00% |
| High Risk | 8.19% |

The High-Risk segment represented only about **3.5% of transactions**, while capturing nearly **50% of detected fraud cases**.

### Unseen Test Data

| Risk Level | Fraud Rate |
|---|---:|
| Low Risk | 0.09% |
| Medium Risk | 0.67% |
| High Risk | 5.44% |

The same risk rules were applied to unseen data without redesigning the scoring framework.

---

## 💡 Key Insights

- Fraud represents only **0.52%** of total transactions but creates more than **$5.12M** in financial exposure.
- Fraud activity increases significantly during late-night hours.
- `shopping_net` is among the highest-risk transaction categories.
- High-Risk transactions represent a small share of transaction volume but contain a large concentration of detected fraud.
- Geographic distance alone is not a strong fraud indicator and should be combined with other behavioral signals.

---

## 🖥️ Dashboard Pages

### 1. Executive Overview
High-level fraud KPIs, activity trends, risk distribution, and investigation queue.

### 2. Transaction Analysis
Transaction volume, financial value, hourly behavior, and transaction category analysis.

### 3. Fraud Analysis
Fraud trends, fraud rate by hour, category-level fraud exposure, and fraud concentration.

### 4. Customer & Merchant Risk
Customer and merchant risk profiling, risk exposure, merchant fraud rates, and risk watchlists.

### 5. Risk Monitoring
Operational investigation queue, risk filters, immediate-review transactions, and high-risk workload monitoring.

### 6. Insights & Recommendations
Executive findings, business recommendations, risk-scoring effectiveness, and business impact.

---

## 🛠️ Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- PyArrow
- Google Colab
- VS Code
- GitHub

---

## 📁 Project Structure

```text
banking-fraud-dashboard/
│
├── Overview.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── daily_summary.parquet
│   ├── category_summary.parquet
│   ├── hour_summary.parquet
│   ├── risk_summary.parquet
│   └── investigation_transactions.parquet
│
└── pages/
    ├── 1_📊_Transaction_Analysis.py
    ├── 2_🚨_Fraud_Analysis.py
    ├── 3_👥_Customer_Merchant_Risk.py
    ├── 4_🛡️_Risk_Monitoring.py
    └── 5_💡_Insights_Recommendations.py
    



## 📌 Business Impact

The dashboard demonstrates how fraud analytics can support:

- Faster investigation prioritization
- Improved visibility into fraud exposure
- Focused review of high-risk transactions
- Reduced manual investigation workload
- Better risk-based decision making

---

## 🌐 Live Dashboard

Live Streamlit Application:

`Coming Soon`

---

## 📓 Analysis Notebook

Complete preprocessing, EDA, feature engineering, risk scoring, and validation notebook:

`Coming Soon`

---

## 🔗 Project Case Study

Detailed project case study and documentation:

`Coming Soon`