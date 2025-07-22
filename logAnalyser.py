import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def highlight_levels(line):
    """Add emoji to visually distinguish log levels."""
    if "ERROR" in line:
        return f"❌ {line}"
    elif "WARN" in line:
        return f"⚠️ {line}"
    elif "INFO" in line:
        return f"ℹ️ {line}"
    return line

def format_logs_for_prompt(log_content: str, max_lines=100):
    """Clean and format logs before sending to OpenAI."""
    lines = log_content.strip().splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    highlighted = [highlight_levels(line) for line in cleaned_lines[:max_lines]]
    return f"```\n" + "\n".join(highlighted) + "\n```"

def analyze_logs_with_openai(log_content: str) -> str:
    """Send formatted logs to OpenAI for analysis."""
    formatted_logs = format_logs_for_prompt(log_content)

    prompt = f"""
You are a senior DevOps engineer and expert in log analysis.

Analyze the following logs and return the results in a structured and concise format with the following sections:

1. **Summary**
   - High-level overview of what is happening in the logs (e.g., timeframe, components involved, key events)

2. **Error & Warning Count**
   - Total number of errors
   - Total number of warnings

3. **Types of Errors**
   - List unique error or warning types (with brief descriptions if possible)

4. **Insights & Anomalies**
   - Identify unusual patterns, recurring issues, spikes, or unexpected behaviors

5. **Recommended Solutions**
   - For each major error or warning type, provide general troubleshooting steps or best-practice recommendations to resolve or prevent the issue

Respond clearly and professionally for use in a technical report.

Logs:
{formatted_logs}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a log analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def log_analyzer_ui():
    """Streamlit UI for log analysis."""
    st.header("📊 Log Analyzer")
    uploaded_file = st.file_uploader("Upload a log file (.txt or .log)", type=["txt", "log"])

    if uploaded_file is not None:
        log_content = uploaded_file.read().decode("utf-8")

        with st.expander("🔍 Preview: Formatted Logs", expanded=False):
            st.markdown(format_logs_for_prompt(log_content), unsafe_allow_html=True)

        if st.button("Analyze Logs with AI"):
            with st.spinner("Analyzing logs using AI..."):
                analysis_result = analyze_logs_with_openai(log_content)
            st.success("✅ Analysis Complete")
            st.markdown("### 🧠 AI Analysis Result:")
            st.markdown(analysis_result)

# If you want to run directly
if __name__ == "__main__":
    log_analyzer_ui()
