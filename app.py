import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ToS Risk Summarizer", page_icon="⚖️", layout="wide")
st.title("⚖️ Terms of Service & Contract Risk Analyzer")

def display_results(data):
    st.subheader("Summary Verdict")
    risk_color = {"HIGH": "‼️", "MEDIUM": "⚠️", "LOW": "🟢"}.get(data.get("overall_risk_rating", "LOW"), "⚪")
    st.markdown(f"### Overall Risk Rating: {risk_color} **{data.get('overall_risk_rating')}**")
    st.info(data.get("executive_summary"))

    st.subheader("Flags & Problematic Clauses")
    flags = data.get("red_flags", [])
    if not flags:
        st.success("No severe red flags detected!")
        return

    for flag in flags:
        severity = flag.get("severity", "LOW")
        badge = "🔴 HIGH RISK" if severity == "HIGH" else ("🟡 MEDIUM RISK" if severity == "MEDIUM" else "🟢 LOW RISK")
        with st.expander(f"{badge} | {flag.get('flag_title')} ({flag.get('category')})"):
            st.markdown(f"**Plain-English Explanation:**\n{flag.get('plain_english')}")
            st.markdown(f"**Original Legal Quote:**\n> *\"{flag.get('original_quote')}\"*")



tab1, tab2 = st.tabs(["📄 Upload PDF", "📝 Paste Text"])

with tab1:
    uploaded_file = st.file_uploader("Choose a PDF contract", type=["pdf"])
    if uploaded_file and st.button("Analyze PDF Contract", type="primary"):
        with st.spinner("Analyzing document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            res = requests.post(f"{API_URL}/analyze-pdf", files=files)
            if res.status_code == 200:
                display_results(res.json())
            else:
                st.error("Error analyzing document.")

with tab2:
    user_text = st.text_area("Paste contract text here:", height=250)
    if user_text and st.button("Analyze Text", type="primary"):
        with st.spinner("Scanning text for risky clauses..."):
            res = requests.post(f"{API_URL}/analyze-text", json={"text": user_text})
            if res.status_code == 200:
                display_results(res.json())
            else:
                st.error("Error analyzing text.")

