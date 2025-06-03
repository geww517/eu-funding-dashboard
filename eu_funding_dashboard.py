import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode


def get_eu_funding_opportunities(keyword, max_results=10):
    base_url = "https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities"
    query = urlencode({"q": keyword})
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Placeholder logic: actual site may require Selenium
    response = requests.get(f"{base_url}?{query}", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select(".opportunity-item")[:max_results]:
        title = item.select_one(".opportunity-title")
        deadline = item.select_one(".opportunity-deadline")
        budget = item.select_one(".opportunity-budget")

        results.append({
            "Title": title.text.strip() if title else "N/A",
            "Deadline": deadline.text.strip() if deadline else "N/A",
            "Budget": budget.text.strip() if budget else "N/A"
        })

    return pd.DataFrame(results)


st.set_page_config(page_title="EU Funding Scraper", layout="centered")
st.title("🔍 EU Funding Opportunity Scanner")

with st.form("search_form"):
    keyword = st.text_input("Enter a keyword (e.g., green energy, SMEs)")
    max_results = st.slider("Number of results", min_value=1, max_value=50, value=10)
    submitted = st.form_submit_button("Search")

if submitted:
    with st.spinner("Fetching opportunities..."):
        df = get_eu_funding_opportunities(keyword, max_results)
        if not df.empty:
            st.success(f"Found {len(df)} opportunities.")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "eu_funding_opportunities.csv", "text/csv")
        else:
            st.warning("No opportunities found. Try a different keyword.")
