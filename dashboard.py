# dashboard.py

import streamlit as st
from apicontractcreator import api_contract_creator_ui
from logAnalyser import log_analyzer_ui

st.set_page_config(page_title="AI Agents Dashboard", layout="wide")
st.title("🤖 AI-Powered Agents Dashboard")

# Create two tabs
tab1, tab2 = st.tabs(["📄 API Contract Creator", "📊 Log Analyzer"])

with tab1:
    api_contract_creator_ui()

with tab2:
    log_analyzer_ui()
