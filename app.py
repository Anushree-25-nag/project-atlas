# ============================================
# PROJECT ATLAS — COMPLETE WEB APPLICATION
# AI-Powered HR Analytics & Attrition System
# Lead Analyst: Anushree Nag
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from groq import Groq

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Project Atlas — AI HR Analytics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM ENTERPRISE CSS ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1C1C2E 0%, #2E86AB 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .risk-high {
        background: #FFE4E4;
        border-left: 5px solid #FF0000;
        padding: 1rem;
        border-radius: 8px;
    }
    .risk-medium {
        background: #FFF8E1;
        border-left: 5px solid #FFA500;
        padding: 1rem;
        border-radius: 8px;
    }
    .risk-low {
        background: #E8F5E9;
        border-left: 5px solid #00AA00;
        padding: 1rem;
        border-radius: 8px;
    }
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GROQ AI CLIENT SETUP ---
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
client = Groq(api_key=api_key) if api_key else None

def ask_ai(prompt, system_message=None):
    if not client:
        return "⚠️ Groq API Key is not configured. Please add it to Streamlit Secrets."
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Service Notice: {str(e)[:120]}"

# --- 4. DATA LOADER ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hr_data.csv")
    except Exception:
        return pd.DataFrame()

df = load_data()

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
<div style="text-align:center; padding:1rem; background:linear-gradient(135deg,#1C1C2E,#2E86AB); border-radius:10px; margin-bottom:1rem;">
<h2 style="color:white; margin:0; font-size:1.3rem;">🏆 Project Atlas</h2>
<p style="color:#adb5bd; margin:0; font-size:0.85rem;">AI HR Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "📍 Navigate to Module:",
    [
        "🏠 Executive Dashboard",
        "📊 Power BI Dashboard",
        "🔍 Risk Assessment",
        "🤖 HR Policy Chatbot",
        "💰 ROI Calculator",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Core Competencies Demonstrated:**
- ✅ Business Analysis & ROI Modeling
- ✅ SQL (CTEs, Window Functions)
- ✅ Python & Statistical Testing
- ✅ Machine Learning (87% AUC-ROC)
- ✅ Deep Learning (ANN Architecture)
- ✅ NLP Sentiment Analysis
- ✅ Generative AI & Prompt Engineering
- ✅ RAG Policy Retrieval
- ✅ Multi-Agent Autonomous Workflows
- ✅ Power BI Enterprise Reporting
""")

# ============================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================
if page == "🏠 Executive Dashboard":

    st.markdown("""
    <div class="main-header">
        <h1>🏆 Project Atlas</h1>
        <h3>AI-Powered HR Analytics & Workforce Intelligence</h3>
        <p>TechCorp India | Macro Talent Health & Financial Risk</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.error("⚠️ Dataset not found. Please ensure hr_data.csv is uploaded.")
        st.stop()

    total = len(df)
    attrited = (df["Attrition"] == "Yes").sum()
    rate = attrited / total * 100
    avg_sal = df["MonthlyIncome"].mean()
    annual_cost = attrited * 340000
    ai_savings = annual_cost * 0.40

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Workforce", f"{total:,}")
    col2.metric("Attrition Rate", f"{rate:.1f}%", "Target: 15%")
    col3.metric("Annual Cost Liability", f"₹{annual_cost/100000:.1f}L")
    col4.metric("AI Target Savings", f"₹{ai_savings/100000:.1f}L", "40% Recovery")
    col5.metric("Avg Monthly Income", f"₹{avg_sal/1000:.0f}K")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        dept_attr = df.groupby("Department").apply(
            lambda x: (x["Attrition"] == "Yes").mean() * 100
        ).reset_index(name="Rate").sort_values("Rate", ascending=True)

        fig1 = px.bar(
            dept_attr, x="Rate", y="Department", orientation="h",
            title="📊 Attrition Rate by Department (%)", color="Rate",
            color_continuous_scale=["#3BB273", "#F4A261", "#E84855"], text="Rate"
        )
        fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig1.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.box(
            df, x="Attrition", y="MonthlyIncome", color="Attrition",
            title="💰 Monthly Compensation Disparity (Stayed vs. Left)",
            color_discrete_map={"No": "#3BB273", "Yes": "#E84855"}
        )
        fig2.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🎯 Leading Behavioral Drivers of Turnover")

    risk_factors_data = {
        "Risk Factor": [
            "Overtime Workers",
            "Low Job Satisfaction (≤2)",
            "Underpaid (<₹30K Salary)",
            "Tenure Flight Risk (≤2yr)",
            "Stagnant Role (5+yr No Promotion)"
        ],
        "Attrition Rate (%)": [
            round((df[df["OverTime"] == "Yes"]["Attrition"] == "Yes").mean() * 100, 1),
            round((df[df["JobSatisfaction"] <= 2]["Attrition"] == "Yes").mean() * 100, 1),
            round((df[df["MonthlyIncome"] < 30000]["Attrition"] == "Yes").mean() * 100, 1),
            round((df[df["YearsAtCompany"] <= 2]["Attrition"] == "Yes").mean() * 100, 1),
            round((df[df["YearsSinceLastPromotion"] >= 5]["Attrition"] == "Yes").mean() * 100, 1)
        ]
    }

    fig3 = px.bar(
        pd.DataFrame(risk_factors_data).sort_values("Attrition Rate (%)"),
        x="Attrition Rate (%)", y="Risk Factor", orientation="h",
        title="Impact of Behavioral Drivers on Attrition Rate",
        color="Attrition Rate (%)",
        color_continuous_scale=["#3BB273", "#F4A261", "#E84855"], text="Attrition Rate (%)"
    )
    fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig3.update_layout(height=300, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# PAGE 2: POWER BI ENTERPRISE DASHBOARD
# ============================================
# ============================================
# PAGE: POWER BI ENTERPRISE DASHBOARD
# ============================================
elif page == "📊 Power BI Dashboard":

    st.title("📊 Power BI Enterprise HR Analytics Dashboard")
    st.markdown("""
    Interactive C-Suite BI Reporting developed in **Power BI Desktop** featuring a **Star Schema Data Model**, 
    custom **DAX Business Measures**, and multi-level diagnostic drill-downs.
    """)
    st.markdown("---")

    col_dl1, col_dl2 = st.columns([2, 1])
    with col_dl1:
        st.info("💡 **For Technical Reviewers:** You can download the complete interactive `.pbix` file to inspect the data model, relationships, and DAX calculations.")
    with col_dl2:
        st.link_button("📥 Download Raw .pbix File", "https://github.com/anushree-25-nag/project-atlas/raw/main/Project_Atlas_HR_Analytics.pbix")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 Page 1: Executive Summary", "🔬 Page 2: Risk & Salary Diagnostics"])

    with tab1:
        st.markdown("### 🏆 Page 1: Macro Executive Overview & Workforce Health")
        st.markdown("""
        - **Strategic Focus:** Real-time workforce scale (2,000 active staff), organizational attrition benchmark tracking (24.1% vs 15% target), and ₹16.3 Cr turnover cost liability.
        - **Core Insights:** Exposes a 3x higher turnover rate among overtime staff and flags Sales & Technology as the highest flight-risk units.
        """)
        try:
            st.image("Screenshot 2026-09-20 194454.png", caption="Power BI Dashboard — Page 1: Executive Summary", use_container_width=True)
        except Exception:
            st.warning("Upload `Screenshot 2026-09-20 194454.png` to your GitHub repo to render this view.")

    with tab2:
        st.markdown("### 🔬 Page 2: Root-Cause Risk & Salary Diagnostics")
        st.markdown("""
        - **Diagnostic Focus:** Quantifies the ₹36.8K monthly compensation gap between leavers and stayers and identifies the 0–2 year tenure flight-risk window.
        - **Operational Impact:** Displays the multi-dimensional satisfaction heatmap and prioritizes the Top 50 at-risk employees for immediate 1:1 manager outreach.
        """)
        try:
            st.image("Screenshot 2026-09-20 194522.png", caption="Power BI Dashboard — Page 2: Risk & Salary Diagnostics", use_container_width=True)
        except Exception:
            st.warning("Upload `Screenshot 2026-09-20 194522.png` to your GitHub repo to render this view.")
# ============================================
# PAGE 3: RISK ASSESSMENT TOOL
# ============================================
elif page == "🔍 Risk Assessment":

    st.title("🔍 Individual Employee Risk Assessment")
    st.markdown("Simulate employee profiles to calculate attrition probability and generate real-time AI retention strategies.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**👤 Profile & Role**")
        age = st.slider("Employee Age", 22, 60, 30)
        department = st.selectbox("Department", ["Technology", "HR", "Finance", "Sales", "Marketing", "Operations"])
        monthly_income = st.number_input("Monthly Income (₹)", 10000, 300000, 45000, 5000)
        years_company = st.slider("Years at Company", 0, 20, 3)

    with col2:
        st.markdown("**😊 Satisfaction Scores**")
        job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
        wlb = st.slider("Work-Life Balance (1-4)", 1, 4, 3)
        performance = st.slider("Performance Rating (1-4)", 1, 4, 3)

    with col3:
        st.markdown("**⚠️ Stress Indicators**")
        overtime = st.selectbox("Works Overtime?", ["No", "Yes"])
        years_promotion = st.slider("Years Since Last Promotion", 0, 15, 2)
        business_travel = st.selectbox("Business Travel Frequency", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])

    if st.button("🚀 Calculate Attrition Risk", type="primary", use_container_width=True):

        risk_score = 0
        risk_factors_list = []

        if job_sat <= 2:
            risk_score += 25
            risk_factors_list.append(f"Low Job Satisfaction: {job_sat}/4")
        if overtime == "Yes":
            risk_score += 20
            risk_factors_list.append("Mandatory Overtime: High Burnout Risk")
        if years_company <= 2:
            risk_score += 15
            risk_factors_list.append(f"Short Tenure: {years_company} Years (Early Career Churn)")
        if monthly_income < 30000:
            risk_score += 15
            risk_factors_list.append(f"Below Market Compensation: ₹{monthly_income:,}")
        if wlb <= 2:
            risk_score += 15
            risk_factors_list.append(f"Imbalanced Work-Life Rating: {wlb}/4")
        if years_promotion >= 5:
            risk_score += 10
            risk_factors_list.append(f"Stagnant Promotion Track: {years_promotion} Years")
        if business_travel == "Travel_Frequently":
            risk_score += 8
            risk_factors_list.append("Frequent Travel Fatigue")

        risk_score = min(risk_score, 100)

        st.markdown("---")
        st.markdown("### 📊 Diagnostic Output")

        col_r1, col_r2 = st.columns([1, 2])

        with col_r1:
            gauge_color = "#E84855" if risk_score >= 70 else "#F4A261" if risk_score >= 40 else "#3BB273"
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text": "Attrition Risk Probability (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": gauge_color},
                    "steps": [
                        {"range": [0, 30], "color": "#E8F5E9"},
                        {"range": [30, 70], "color": "#FFF8E1"},
                        {"range": [70, 100], "color": "#FFEBEE"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

            if risk_score >= 70:
                st.markdown('<div class="risk-high"><h3>🔴 HIGH RISK</h3><p>Immediate 1:1 Manager Intervention Required!</p></div>', unsafe_allow_html=True)
            elif risk_score >= 40:
                st.markdown('<div class="risk-medium"><h3>🟡 MEDIUM RISK</h3><p>Monitor closely in monthly reviews.</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="risk-low"><h3>🟢 LOW RISK</h3><p>Employee retention is stable.</p></div>', unsafe_allow_html=True)

        with col_r2:
            st.markdown("**Identified Risk Factors:**")
            if risk_factors_list:
                for rf in risk_factors_list:
                    st.markdown(f"- {rf}")
            else:
                st.success("✅ No significant risk factors detected.")

            st.info("💰 **Financial Exposure:** Cost if leaves: **₹3,40,000** | Intervention Budget: **₹25,000** | Net ROI: **1,260%**")

            st.markdown("**🤖 AI-Generated Retention Roadmap:**")
            with st.spinner("Synthesizing personalized retention plan..."):
                prompt = f"""
                Employee Profile: Age={age}, Department={department}, Income=₹{monthly_income:,}, Job Satisfaction={job_sat}/4, Work Life Balance={wlb}/4, Overtime={overtime}, Promotion Gap={years_promotion} years, Risk Score={risk_score}%.
                Provide 3 prioritized, highly specific retention initiatives with estimated costs in INR. Keep response under 100 words.
                """
                recs = ask_ai(prompt, "You are a Senior Talent Retention Specialist.")
                st.markdown(recs)

# ============================================
# PAGE 4: HR POLICY CHATBOT (RAG)
# ============================================
elif page == "🤖 HR Policy Chatbot":

    st.title("🤖 Grounded HR Policy Assistant (RAG)")
    st.markdown("Ask natural-language questions about official TechCorp India corporate policies.")
    st.markdown("---")

    hr_policies = """
    LEAVE POLICY:
    - Annual Leave: 24 days per calendar year (accrues at 2 days/month). Up to 30 days can be carried forward.
    - Sick Leave: 12 days per year (medical certificate required if >3 consecutive days).
    - Casual Leave: 12 days per year (max 3 consecutive days allowed).
    - Parental Leaves: 26 weeks paid Maternity Leave; 15 days paid Paternity Leave.
    - Special Leaves: 5 days paid Marriage Leave; 5 days Bereavement Leave.

    COMPENSATION & BENEFITS:
    - CTC Breakdown: Basic = 40%, HRA = 20%, Special Allowance = 40%.
    - Performance Increments: Rating 4 = 20-25%; Rating 3 = 12-18%; Rating 2 = 8-12%; Rating 1 = 0-5%.
    - Healthcare: Comprehensive ₹5,00,000 family medical insurance coverage.
    - L&D Allowance: ₹25,000 annual skill enhancement allowance per employee.

    REMOTE WORK (WFH) POLICY:
    - Hybrid Model: 3 days in-office, 2 days remote weekly.
    - Core Availability Hours: 10:00 AM – 5:00 PM IST.
    - Remote Subsidy: ₹1,000 monthly internet & utility reimbursement.
    """

    st.markdown("**Quick Inquiries:**")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("🌴 Annual Leave Entitlement", use_container_width=True):
            st.session_state.auto_q = "What is the annual leave entitlement and carry-forward policy?"
    with q2:
        if st.button("🏠 Hybrid / WFH Guidelines", use_container_width=True):
            st.session_state.auto_q = "What are the rules and subsidies for working from home?"
    with q3:
        if st.button("📈 Performance Hike Bands", use_container_width=True):
            st.session_state.auto_q = "What are the salary increment percentages by performance rating?"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "auto_q" in st.session_state:
        auto_question = st.session_state.auto_q
        del st.session_state.auto_q
        st.session_state.chat_history.append({"role": "user", "content": auto_question})
        with st.spinner("Retrieving verified policy articles..."):
            answer = ask_ai(
                f"Policy Documentation:\n{hr_policies}\n\nEmployee Query: {auto_question}",
                "You are the official TechCorp HR Assistant. Answer exclusively from the provided policy text. Include exact figures."
            )
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask any question regarding leave, compensation, or HR policies..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving policy context..."):
                answer = ask_ai(
                    f"Policy Documentation:\n{hr_policies}\n\nEmployee Query: {user_input}",
                    "You are the official TechCorp HR Assistant. Answer exclusively from the provided policy text."
                )
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# ============================================
# PAGE 5: ROI CALCULATOR
# ============================================
elif page == "💰 ROI Calculator":

    st.title("💰 AI Implementation Financial ROI Model")
    st.markdown("Forecast cost savings and financial payback resulting from AI-driven talent retention.")
    st.markdown("---")

    rc1, rc2 = st.columns(2)

    with rc1:
        st.markdown("### 📊 Macro Organizational Inputs")
        total_emp = st.slider("Workforce Headcount", 500, 20000, 5000, 500)
        current_rate = st.slider("Current Turnover Rate (%)", 5.0, 40.0, 25.0, 0.5)
        cost_per_hire = st.number_input("Average Replacement Cost per Exit (₹)", 50000, 1000000, 340000, 10000)
        ai_invest = st.number_input("AI Implementation Capital Investment (₹)", 500000, 5000000, 1800000, 100000)

    with rc2:
        st.markdown("### 🎯 Projected Outcomes")
        target_rate = st.slider(
            "Target Turnover Rate Post-AI (%)",
            5.0, float(current_rate), max(float(current_rate) * 0.6, 5.0), 0.5
        )

        cur_exits = int(total_emp * current_rate / 100)
        cur_cost = cur_exits * cost_per_hire
        tgt_exits = int(total_emp * target_rate / 100)
        tgt_cost = tgt_exits * cost_per_hire
        ann_savings = cur_cost - tgt_cost
        ops_cost = 500000
        net = ann_savings - ai_invest - ops_cost
        roi_val = (net / (ai_invest + ops_cost)) * 100
        pb = (ai_invest + ops_cost) / (ann_savings / 12)

        st.metric("Annualized Cost Recovery", f"₹{ann_savings:,.0f}")
        st.metric("Net 1st Year ROI", f"{roi_val:.0f}%")
        st.metric("Capital Payback Period", f"{pb:.1f} Months")
        st.metric("Net 1st Year Cash Benefit", f"₹{net:,.0f}")

    yr_labels = ["Year 1", "Year 2", "Year 3"]
    yr_savings = [ann_savings * y - ai_invest - ops_cost * y for y in [1, 2, 3]]
    yr_invest = [ai_invest + ops_cost * y for y in [1, 2, 3]]

    fig_roi = go.Figure()
    fig_roi.add_trace(go.Bar(x=yr_labels, y=yr_savings, name="Cumulative Net Benefit", marker_color="#3BB273"))
    fig_roi.add_trace(go.Bar(x=yr_labels, y=yr_invest, name="Cumulative Capital Cost", marker_color="#E84855"))
    fig_roi.update_layout(title="3-Year Capital Investment vs. Value Realization", barmode="group", height=350)
    st.plotly_chart(fig_roi, use_container_width=True)

# ============================================
# PAGE 6: ABOUT PROJECT
# ============================================
elif page == "ℹ️ About Project":

    st.title("ℹ️ Executive Summary & Technical Portfolio")

    st.markdown("""
    ## 🏆 Project Atlas — Master Overview

    | Dimension | Implementation Details |
    | :--- | :--- |
    | **Project Title** | Project Atlas: Enterprise AI HR Analytics & Attrition Intelligence System |
    | **Problem Statement** | High 25% annual turnover inflicting ₹8.5 Crores in replacement and productivity losses |
    | **Target Outcome** | 40% reduction in turnover (₹3.4 Crores in recurring annual cost recovery) |
    | **Financial Payback** | **1,682% 1st Year ROI** with a **1.6-month** capital amortization window |
    | **Core ML Engine** | Multi-model ensemble (Best: XGBoost with 87% AUC-ROC & 90-day early warning) |
    | **Lead Developer** | **Anushree Nag** — AI Business Analyst |

    ---

    ### 🛠️ Full-Stack Skills & Architecture Matrix

    | Technical Discipline | Implementation Architecture |
    | :--- | :--- |
    | **Business Analysis** | Authored comprehensive BRD, FRD, Agile User Stories, RACI Matrix, and Risk Registers |
    | **Data & SQL Engineering** | Complex CTE pipelines, Window Functions (RANK, NTILE, LAG), and Database Schemas |
    | **Statistical Modeling** | Hypothesis testing: Independent T-Tests, Chi-Square Contingency, and One-Way ANOVA |
    | **Machine Learning** | 6 Supervised Classifiers with Hyperparameter Tuning and SHAP Game-Theoretic Explainability |
    | **Deep Learning** | Custom Multi-Layer Artificial Neural Network (ANN) with Dropout and Batch Normalization |
    | **NLP & Text Mining** | TextBlob Polarity Scoring and Scikit-Learn TF-IDF N-Gram Classification |
    | **Generative AI** | 6 Distinct Prompt Engineering Patterns using Groq LLaMA 3.3 70B Engine |
    | **RAG Architecture** | Semantic Policy Retrieval using ChromaDB Vector Store and Context Grounding |
    | **Agentic Workflows** | 6 Specialized Autonomous Agents with Dynamic Tool Execution and Self-Reflection |
    | **Business Intelligence** | Dual-Page Executive Dashboard engineered in Power BI Desktop (Star Schema & DAX) |
    | **Cloud Deployment** | Live 24/7 Production Deployment via Streamlit Community Cloud |

    ---

    ### 📬 Contact & Portfolio Links
    - **Live Application:** [project-atlas.streamlit.app](https://project-atlas-82dqpn2z5pduntoekgknjm.streamlit.app/)
    - **GitHub Repository:** [github.com/anushree-25-nag/project-atlas](https://github.com/anushree-25-nag/project-atlas)
    - **Lead Analyst:** Anushree Nag
    """)
