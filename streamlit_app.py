
import streamlit as st
import requests
import time

from agents import project_agent
from agents import market_agent
from agents import risk_agent
from agents import reporting_agent

# -------------------------------
# INIT AGENTS
# -------------------------------
project_agent = project_agent.ProjectAgent()
market_agent = market_agent.MarketAgent()
risk_agent = risk_agent.RiskAgent()
reporting_agent = reporting_agent.ReportingAgent()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Risk Analyzer", layout="wide")

# -------------------------------
# CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.news-box {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("🧠 AI Project Risk Analyzer")

# -------------------------------
# API KEY
# -------------------------------
API_KEY = "YOUR_API_KEY"

# -------------------------------
# FETCH NEWS
# -------------------------------
def fetch_market_news():
    timestamp = int(time.time())

    url = f"https://newsapi.org/v2/everything?q=market OR supply OR inflation&language=en&pageSize=5&sortBy=publishedAt&apiKey={API_KEY}&t={timestamp}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        articles = data.get("articles", [])
        news_list = [a.get("title") for a in articles if a.get("title")]

        if not news_list:
            raise Exception("No news")

        return news_list

    except:
        return [
            "Supply chain disruption",
            "Inflation rising",
            "Market instability detected"
        ]

# -------------------------------
# SESSION STATE
# -------------------------------
if "news" not in st.session_state:
    st.session_state.news = fetch_market_news()

# -------------------------------
# PROJECT INPUT
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.header("📊 Project Details")

col1, col2 = st.columns(2)

with col1:
    project_id = st.text_input("Project ID", "1")
    deadline = st.date_input("Deadline")
    topics = st.multiselect("Project Topics", ["AI", "Cloud", "Security", "IoT", "Electronics"], default=["AI", "Cloud"])

with col2:
    completion_date = st.date_input("Completion Date")
    budget_allocated = st.number_input("Budget Allocated", value=10000)
    budget_used = st.number_input("Budget Used", value=12000)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# MARKET NEWS
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.header("🌐 Market Conditions")

if st.button("🔄 Refresh News"):
    st.session_state.news = fetch_market_news()
    st.rerun()

for news in st.session_state.news:
    st.markdown(f'<div class="news-box">📰 {news}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
analyze_clicked = st.button("🚀 Analyze Risk")

# -------------------------------
# OUTPUT
# -------------------------------
if analyze_clicked:

    with st.spinner("Running AI Agents..."):

        try:
            # Prepare data
            project_data = {
                "project_id": project_id,
                "deadline": str(deadline),
                "completion_date": str(completion_date),
                "budget_allocated": budget_allocated,
                "budget_used": budget_used
            }

            market_news = st.session_state.news[:2]

            # ---------------------------
            # AGENT PIPELINE
            # ---------------------------
            project_result = project_agent.analyze(project_data)
            market_result = market_agent.analyze(market_news)
            final_result = risk_agent.analyze(project_result, market_result)

            report = reporting_agent.generate_report(project_data, final_result)

            # ---------------------------
            # FIXED DATA MAPPING
            # ---------------------------
            risk_level = final_result.get("risk_level", "UNKNOWN")

            risk_score = float(final_result.get("final_risk_score", 0)) * 100
            risk_score = int(risk_score)

            key_factors = final_result.get("key_factors", [])
            justification = final_result.get("justification", "")

            # Safe delay calculation
            if deadline and completion_date:
                delay = max((completion_date - deadline).days, 0)
            else:
                delay = 0

            budget_ratio = budget_used / budget_allocated if budget_allocated > 0 else 0

            # ---------------------------
            # KPI CARDS
            # ---------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🚨 Risk Level")
                st.write(risk_level)
                st.progress(risk_score / 100)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("💰 Budget Usage")
                st.write(f"{budget_used}/{budget_allocated}")
                st.progress(min(budget_ratio, 1.0))
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("⏳ Delay")
                st.write(f"{delay} days")
                st.markdown('</div>', unsafe_allow_html=True)

            # ---------------------------
            # REPORT SECTION
            # ---------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)

            color = "#ff4b4b" if risk_level=="HIGH" else "#ffa500" if risk_level=="MEDIUM" else "#00ff9f"

            st.markdown(f"<h2 style='color:{color};'>🚨 Risk Level: {risk_level}</h2>", unsafe_allow_html=True)
            st.markdown(f"### Risk Score: {risk_score}/100")

            st.subheader("📝 AI Generated Report")
            st.write(report)

            st.subheader("🔑 Key Factors")
            for f in key_factors:
                st.write(f"✔️ {f.replace('_',' ').title()}")

            st.subheader("📊 Analysis")
            st.info(justification)

            st.subheader("💡 Recommendations")

            if "budget" in str(key_factors):
                st.write("✔️ Optimize project budget and reduce overspending.")
            if "market" in str(key_factors):
                st.write("✔️ Prepare contingency plans for market changes.")
            if not key_factors:
                st.write("✔️ Project is stable. Continue monitoring.")

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")