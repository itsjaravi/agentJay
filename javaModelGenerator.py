import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# AI Prompt: Expert System Message
system_prompt = (
    "You are a highly experienced Java backend engineer. Given JSON request and response structures, your tasks are:\n"
    "1. Generate well-structured Java POJO (Plain Old Java Object) or model classes with appropriate data types for both request and response, including nested objects and collections.\n"
    "2. Include getter and setter methods following standard Java conventions.\n"
    "3. Generate JUnit 5 test cases that:\n"
    "   - Use realistic mock data\n"
    "   - Cover both normal and edge cases\n"
    "   - Validate object construction, field values, and null handling\n"
    "Your response should be production-ready Java code with clear formatting, comments where appropriate, and follow Java best practices."
)

def generate_java_code(request_json, response_json):
    prompt = f"""
REQUEST JSON:
{request_json}

RESPONSE JSON:
{response_json}

Now generate the following:
1. Java POJO/model classes for both Request and Response
2. Getter and Setter methods
3. JUnit 5 test class covering both with mock data and all edge cases
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def java_model_generator_ui():
    st.header("☕ Java POJO + JUnit Generator")

    st.markdown("### 📨 Request JSON")
    request_json = st.text_area("Paste your **Request JSON**", height=200)

    st.markdown("### 📬 Response JSON")
    response_json = st.text_area("Paste your **Response JSON**", height=200)

    if not request_json or not response_json:
        st.info("Please paste both Request and Response JSON to proceed.")
        return

    # Validate JSON formats
    try:
        json.loads(request_json)
        json.loads(response_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format detected in one of the inputs.")
        return

    if st.button("🛠️ Generate POJOs + JUnit Test"):
        with st.spinner("Generating Java classes and test cases..."):
            result = generate_java_code(request_json, response_json)
        st.subheader("📄 Generated Java Code")
        st.code(result, language="java")
