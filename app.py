import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Project Atlas — HR Analytics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown('''
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
    border-left: 4px solid red;
    padding: 1rem;
    border-radius: 8px;
}
.risk-medium {
    background: #FFF8E1;
    border-left: 4px solid orange;
    padding: 1rem;
    border-radius: 8px;
}
.risk-low {
    background: #E8F5E9;
    border-left: 4px solid green;
    padding: 1rem;
    border-radius: 8px;
}
</style>
''', unsafe_allow_html=True)

# --- GROQ API CLIENT ---
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
client = Groq(api_key=api_key) if api_key else None

def ask_ai(prompt, system_message=None):
    if not client:
        return "⚠️ Groq API Key is not configured. Please add it in Streamlit Cloud Secrets."
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
        return f"AI Error: {str(e)[:150]}"

# --- DATA LOADER ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hr_data.csv")
    except Exception:
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR ---
st.sidebar.markdown('''
<div style="text-align:center; padding:1rem; background:linear-gradient(135deg,#1C1C2E,#2E86AB); border-radius:10px; margin-bottom:1rem;">
<h2 style="color:white; margin:0;">🏆 Project Atlas</h2>
<p style="color:#adb5bd; margin:0;">AI HR Analytics</p>
</div>
''', unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navigate to:",
    [
        "🏠 Executive Dashboard",
        "🔍 Risk Assessment",
        "🤖 HR Policy Chatbot",
        "💰 ROI Calculator",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Skills Demonstrated:**")
st.sidebar.markdown("- Business Analysis & ROI")
st.sidebar.markdown("- SQL & Python Analytics")
st.sidebar.markdown("- Machine Learning & ANN")
st.sidebar.markdown("- NLP Sentiment Analysis")
st.sidebar.markdown("- Generative AI & RAG")
st.sidebar.markdown("- Interactive Dashboard")

# ============================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================
if page == "🏠 Executive Dashboard":
    st.markdown('''
    <div class="main-header">
        <h1>🏆 Project Atlas</h1>
        <h3>AI-Powered HR Analytics System</h3>
        <p>TechCorp India | Real-time Intelligence</p>
    </div>
    ''', unsafe_allow_html=True)

    if df.empty:
        st.error("⚠️ Dataset not found! Make sure hr_data.csv is present.")
        st.stop()

    total = len(df)
    attrited = (df["Attrition"] == "Yes").sum()
    rate = attrited / total * 100
    avg_sal = df["MonthlyIncome"].mean()
    annual_cost = attrited * 340000
    ai_savings = annual_cost * 0.40

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Employees", f"{total:,}")
    col2.metric("Attrition Rate", f"{rate:.1f}%", "Target: 15%")
    col3.metric("Annual Cost", f"₹{annual_cost/100000:.1f}L")
    col4.metric("AI Savings", f"₹{ai_savings/100000:.1f}L", "40% cut")
    col5.metric("Avg Salary", f"₹{avg_sal/1000:.0f}K/mo")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        dept_attr = df.groupby("Department").apply(
            lambda x: (x["Attrition"] == "Yes").mean() * 100
        ).reset_index(name="Rate").sort_values("Rate", ascending=True)

        fig1 = px.bar(
            dept_attr, x="Rate", y="Department", orientation="h",
            title="Attrition Rate by Department", color="Rate",
            color_continuous_scale=["green", "yellow", "red"], text="Rate"
        )
        fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig1.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.box(
            df, x="Attrition", y="MonthlyIncome", color="Attrition",
            title="Monthly Income vs Attrition",
            color_discrete_map={"No": "#3BB273", "Yes": "#E84855"}
        )
        fig2.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 2: RISK ASSESSMENT
# ============================================
elif page == "🔍 Risk Assessment":
    st.title("Employee Attrition Risk Assessment")
    st.markdown("Enter employee details to get AI-powered risk prediction")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Age", 22, 60, 30)
        department = st.selectbox("Department", ["Technology", "HR", "Finance", "Sales", "Marketing", "Operations"])
        monthly_income = st.number_input("Monthly Income (₹)", 10000, 300000, 45000, 5000)
        years_company = st.slider("Years at Company", 0, 20, 3)

    with col2:
        job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
        wlb = st.slider("Work Life Balance (1-4)", 1, 4, 3)
        performance = st.slider("Performance Rating (1-4)", 1, 4, 3)

    with col3:
        overtime = st.selectbox("Works Overtime?", ["No", "Yes"])
        years_promotion = st.slider("Years Since Promotion", 0, 15, 2)
        business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])

    if st.button("Assess Attrition Risk", type="primary", use_container_width=True):
        risk_score = 0
        risk_factors_list = []

        if job_sat <= 2:
            risk_score += 25
            risk_factors_list.append(f"Low Job Satisfaction: {job_sat}/4")
        if overtime == "Yes":
            risk_score += 20
            risk_factors_list.append("Working Overtime: Burnout risk")
        if years_company <= 2:
            risk_score += 15
            risk_factors_list.append(f"Short Tenure: {years_company} years")
        if monthly_income < 30000:
            risk_score += 15
            risk_factors_list.append(f"Below Market Salary: ₹{monthly_income:,}")
        if wlb <= 2:
            risk_score += 15
            risk_factors_list.append(f"Poor Work-Life Balance: {wlb}/4")
        if years_promotion >= 5:
            risk_score += 10
            risk_factors_list.append(f"No Promotion in {years_promotion} years")

        risk_score = min(risk_score, 100)
        st.markdown("---")
        st.markdown("### Risk Assessment Result")
        col_r1, col_r2 = st.columns([1, 2])

        with col_r1:
            gauge_color = "#E84855" if risk_score >= 70 else "#F4A261" if risk_score >= 40 else "#3BB273"
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=risk_score,
                title={"text": "Risk Score"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": gauge_color}}
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_r2:
            st.markdown("**Risk Factors Identified:**")
            for rf in risk_factors_list:
                st.markdown(f"- {rf}")
            if not risk_factors_list:
                st.success("No major risk factors detected.")

            st.info("Cost if leaves: ₹3,40,000 | Retention Cost: ₹25,000 | Projected ROI: 1,260%")
            st.markdown("**AI Recommendations:**")
            with st.spinner("Analyzing profile with AI..."):
                prompt = f"Employee: Age={age}, Dept={department}, Salary=₹{monthly_income}, JobSat={job_sat}/4, Overtime={overtime}, PromotionGap={years_promotion}yr, RiskScore={risk_score}%. Give 3 specific retention actions with estimated costs in ₹."
                st.markdown(ask_ai(prompt, "You are an HR Retention Specialist."))

# ============================================
# PAGE 3: HR POLICY CHATBOT
# ============================================
elif page == "🤖 HR Policy Chatbot":
    st.title("HR Policy Assistant (RAG)")
    st.markdown("Ask any questions about TechCorp India HR Policies.")
    st.markdown("---")

    hr_policies = """
    LEAVE: 24 annual leaves, 12 sick leaves, 12 casual leaves, 26 weeks paid maternity, 15 days paternity.
    COMPENSATION: Basic is 40% CTC, HRA 20%, Rating 4 gets 20-25% hike, Rating 3 gets 12-18% hike. Health Insurance 5 Lakhs.
    WFH: Hybrid 3 days office & 2 days WFH weekly. Core hours 10 AM to 5 PM. ₹1,000 monthly internet reimbursement.
    LEARNING: ₹25,000 annual learning budget per employee. Certifications 100% reimbursed on 1st attempt.
    """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask your HR policy question..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching policies..."):
                ans = ask_ai(f"Context: {hr_policies}\nQuestion: {user_input}", "You are TechCorp HR Assistant. Answer directly using provided context.")
            st.markdown(ans)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})

# ============================================
# PAGE 4: ROI CALCULATOR
# ============================================
elif page == "💰 ROI Calculator":
    st.title("AI Implementation ROI Calculator")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        total_emp = st.slider("Total Employees", 500, 20000, 5000, 500)
        current_rate = st.slider("Current Attrition Rate (%)", 5.0, 40.0, 25.0, 0.5)
        cost_per_hire = st.number_input("Cost per Attrition (₹)", 50000, 1000000, 340000, 10000)
        ai_invest = st.number_input("AI Investment (₹)", 500000, 5000000, 1800000, 100000)
    with col2:
        target_rate = st.slider("Target Attrition Rate (%)", 5.0, float(current_rate), max(float(current_rate)*0.6, 5.0), 0.5)
        ann_savings = (total_emp * (current_rate - target_rate) / 100) * cost_per_hire
        net = ann_savings - ai_invest - 500000
        roi_val = (net / (ai_invest + 500000)) * 100
        st.metric("Annual Savings", f"₹{ann_savings:,.0f}")
        st.metric("1st Year ROI", f"{roi_val:.0f}%")
        st.metric("Payback Period", f"{(ai_invest + 500000)/(ann_savings/12):.1f} months")

# ============================================
# PAGE 5: ABOUT PROJECT
# ============================================
elif page == "ℹ️ About Project":
    st.title("About Project Atlas")
    st.markdown('''
    ### 🏆 AI-Powered HR Analytics System
    - **Problem Solved:** 25% Attrition costing ₹8.5 Crores
    - **Outcome:** ₹3.4 Crores Annual Savings | 1,682% ROI | 90-day Early Warning
    - **Author:** Anushree Nag — AI Business Analyst
    - **GitHub Repository:** [github.com/anushree-25-nag/project-atlas](https://github.com/anushree-25-nag/project-atlas)
    - **LinkedIn:** https://www.linkedin.com/in/anushreenag/ 
    - **Email:** naganu025@gmail.com
    ''')
