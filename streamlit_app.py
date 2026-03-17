import streamlit as st

from agents import project_agent
from agents import market_agent
from agents import risk_agent
from agents import reporting_agent

# Initialize agents
project_agent = project_agent.ProjectAgent()
market_agent = market_agent.MarketAgent()
risk_agent = risk_agent.RiskAgent()
reporting_agent = reporting_agent.ReportingAgent()

st.set_page_config(page_title="AI Risk Analyzer", layout="centered")

st.title("🧠 AI Project Risk Analyzer")
st.markdown("Enter project details and market conditions to assess risk.")

# -------------------------------
# USER INPUT
# -------------------------------

# -------------------------------
# MARKET FETCHER
# -------------------------------
API_KEY = "ed9d428902504be4858a8711675b30d7"  # 🔥 put your NewsAPI key here


def fetch_market_news():
    url = f"https://newsapi.org/v2/everything?q=market OR supply OR inflation&language=en&pageSize=5&apiKey={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        articles = data.get("articles", [])
        news_list = []

        for article in articles:
            title = article.get("title")
            if title:
                news_list.append(title)

        if not news_list:
            raise Exception("No news found")

        return news_list

    except Exception as e:
        print("❌ News fetch failed:", e)

        # fallback (VERY IMPORTANT)
        return [
            "Global supply chain disruption reported",
            "Inflation increasing across markets",
            "Raw material costs rising globally"
        ]


# -------------------------------
# PROJECT INPUT
# -------------------------------
st.header("📊 Project Details")

project_id = st.text_input("Project ID", "1")

deadline = st.date_input("Deadline")
completion_date = st.date_input("Completion Date")

budget_allocated = st.number_input("Budget Allocated", value=10000)
budget_used = st.number_input("Budget Used", value=12000)

# -------------------------------
# AUTO MARKET DATA
# -------------------------------
st.header("🌐 Market Conditions (Auto Fetched)")

if "news" not in st.session_state:
    st.session_state.news = fetch_market_news()

if st.button("🔄 Refresh Market News"):
    st.session_state.news = fetch_market_news()

st.write("Latest Market Signals:")
for news in st.session_state.news:
    st.write("•", news)

# -------------------------------
# RUN ANALYSIS
# -------------------------------
if st.button("🚀 Analyze Risk"):

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

            market_news = st.session_state.news[:2]  # limit for LLM stability

            # ---------------------------
            # AGENT PIPELINE
            # ---------------------------
            project_result = project_agent.analyze(project_data)
            market_result = market_agent.analyze(market_news)
            final_result = risk_agent.analyze(project_result, market_result)
            report = reporting_agent.generate_report(project_data, final_result)

            # ---------------------------
            # OUTPUT
            # ---------------------------
            st.success("✅ Analysis Complete")

            # Risk indicator
            risk_level = final_result.get("risk_level", "UNKNOWN")

            if risk_level == "HIGH":
                st.error(f"🚨 HIGH RISK")
            elif risk_level == "MEDIUM":
                st.warning(f"⚠️ MEDIUM RISK")
            else:
                st.success(f"✅ LOW RISK")

            st.subheader("📊 Risk Details")
            st.json(final_result)

            st.subheader("📝 AI Generated Report")
            st.write(report)

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")