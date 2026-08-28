
import os
import json
import subprocess
from pathlib import Path
from typing import List

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

from google.adk.agents import LlmAgent as Agent
from google.adk.tools import FunctionTool
from google.adk.apps import App
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ==========================================
# PAGE CONFIGURATION & ENTERPRISE CRM THEMING
# ==========================================
st.set_page_config(
    page_title="CRM Data & BigQuery Analytics",
    page_icon="💼",
    layout="wide"
)

# Enterprise Navy & Slate Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1E293B;
        color: #F8FAFC;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #F8FAFC !important;
    }

    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #E2E8F0;
        border: 1px solid #CBD5E1;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
    }

    div.stButton > button:first-child {
        background-color: #2563EB;
        color: white;
        border-radius: 6px;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #1D4ED8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIGURATION & CREDENTIAL RESOLUTION
# ==========================================

def get_secret(key: str, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

# 1. Resolve Gemini API Key
api_key = get_secret("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

# 2. Resolve Model Identifier (Defaults explicitly to gemini-3.6-flash)
MODEL_ID = get_secret("GEMINI_MODEL", "gemini-2.0-flash")

# 3. Resolve BigQuery Parameters
GCP_PROJECT = get_secret("GCP_PROJECT", os.environ.get("GCP_PROJECT", "notebooklm-491108"))
DATASET_ID = get_secret("BQ_DATASET", os.environ.get("BQ_DATASET", "crm_data"))
TABLE_ID = get_secret("BQ_TABLE", os.environ.get("BQ_TABLE", "leads"))

FULL_TABLE_PATH = f"`{GCP_PROJECT}.{DATASET_ID}.{TABLE_ID}`"

# 4. Sandbox execution check
SANDBOX_CLI = '/usr/local/gcp/bin/sandbox'
IS_LOCAL_MODE = not Path(SANDBOX_CLI).exists()


def get_bigquery_client() -> bigquery.Client:
    """Initializes BigQuery client using Streamlit Secrets or default ADC credentials."""
    try:
        if "gcp_service_account" in st.secrets:
            secret_val = st.secrets["gcp_service_account"]
            creds_dict = json.loads(secret_val) if isinstance(secret_val, str) else dict(secret_val)
            credentials = service_account.Credentials.from_service_account_info(creds_dict)
            return bigquery.Client(credentials=credentials, project=GCP_PROJECT)
    except Exception:
        pass
    
    return bigquery.Client(project=GCP_PROJECT)


def run_bigquery_sql(query: str) -> str:
    """Executes a SQL query against the BigQuery CRM table and returns the results formatted as text."""
    try:
        client = get_bigquery_client()
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        if not rows:
            return "Query executed successfully, but returned 0 rows."
        return str(rows)
    except Exception as e:
        return f"BigQuery Execution Error: {str(e)}"


def run_sandbox_process(args: list[str]):
    cmd = args[2:] if IS_LOCAL_MODE and args[:2] == ['do', '--'] else ([SANDBOX_CLI] + args if not IS_LOCAL_MODE else args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10)


def execute_sandbox_command(command: str) -> str:
    """Executes shell commands in local environment or sandbox container."""
    try:
        res = run_sandbox_process(['do', '--', '/bin/sh', '-c', command])
        if res.returncode != 0:
            return f"Execution Failed!\nExit Code: {res.returncode}\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"
        return res.stdout
    except Exception as err:
        return f"Sandbox Tool Error: {str(err)}"

# ==========================================
# ADK AGENT & RUNNER INITIALIZATION
# ==========================================
@st.cache_resource(show_spinner=False)
def get_runner(model_name: str):
    root_agent = Agent(
        name='crm_bigquery_assistant',
        description='ADK agent capable of querying BigQuery datasets and running python scripts to analyze CRM records.',
        model=model_name,
        instruction=(
            f'You are an expert AI CRM Strategy Analyst.\n'
            f'You have access to a BigQuery table containing CRM leads at path: {FULL_TABLE_PATH}.\n\n'
            '1. Table Schema Awareness:\n'
            '   Columns: CustomerID (INT), FirstName (STRING), LastName (STRING), Email (STRING), Phone (STRING), '
            'Address (STRING), City (STRING), State (STRING), ZipCode (STRING), Country (STRING), SignupDate (STRING/DATE), '
            'LastPurchaseDate (STRING/DATE), TotalSpent (NUMERIC), LeadSource (STRING), Notes (STRING).\n\n'
            '2. Query Policy:\n'
            '   - Use `run_bigquery_sql` to execute SQL queries on BigQuery.\n'
            '   - Use `execute_sandbox_command` for Python code when complex data manipulation is required.\n\n'
            '3. Output Policy:\n'
            '   - Summarize insights concisely in clear markdown tables or bullet points.\n'
            '   - Always suggest concrete next steps for sales managers based on data findings.'
        ),
        tools=[
            FunctionTool(func=run_bigquery_sql),
            FunctionTool(func=execute_sandbox_command)
        ]
    )

    adk_app = App(name="crm_bq_sandbox_app", root_agent=root_agent)
    return Runner(app=adk_app, session_service=InMemorySessionService(), auto_create_session=True)

# Explicit parameter binding forces cache invalidation when model changes
runner = get_runner(MODEL_ID)

# ==========================================
# STREAMLIT UI & CHAT INTERFACE
# ==========================================

# Sidebar Dashboard
with st.sidebar:
    st.header("💼 CRM BigQuery Monitor")
    st.markdown("---")
    st.markdown("**Status:** Active")
    st.markdown(f"**Model:** `{MODEL_ID}`")
    st.markdown(f"**GCP Project:** `{GCP_PROJECT}`")
    st.markdown(f"**BigQuery Table:** `{DATASET_ID}.{TABLE_ID}`")
    
    st.markdown("---")
    st.caption("Table Schema:")
    st.code(
        "CustomerID, FirstName, LastName, Email, Phone, Address, City, State, "
        "ZipCode, Country, SignupDate, LastPurchaseDate, TotalSpent, LeadSource, Notes",
        language="text"
    )

# Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": f"💼 **CRM Intelligence Agent Ready.** Connected to `{FULL_TABLE_PATH}` using model `{MODEL_ID}`. Ask me to run SQL aggregations, evaluate lead acquisition channels, or extract sentiment from customer notes!"
        }
    ]

# Render Message Stream
for message in st.session_state.messages:
    avatar = "💼" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat Input Box
if prompt := st.chat_input("Ask CRM Assistant to analyze spend, find churn risks, or rank lead sources..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💼"):
        with st.spinner("Processing request and running BigQuery SQL..."):
            try:
                new_message = types.Content(parts=[types.Part(text=prompt)])
                events = runner.run(
                    user_id="local_user",
                    session_id="local_session",
                    new_message=new_message
                )
                
                final_response = "".join(
                    part.text
                    for event in events
                    if event.content and event.content.parts
                    for part in event.content.parts
                    if part.text
                ) or "Query executed successfully without text output."
                
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                error_msg = f"⚠️ **Execution Error:** {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
