import os
import subprocess
from pathlib import Path
from typing import List
import streamlit as st
from google.cloud import bigquery

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

# Enterprise Navy & Slate Theme
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
# CONFIGURATION & BIGQUERY TOOLS
# ==========================================
SANDBOX_CLI = '/usr/local/gcp/bin/sandbox'
IS_LOCAL_MODE = not Path(SANDBOX_CLI).exists()

# Set BigQuery Dataset Details (Set these to match your GCP project)
GCP_PROJECT = os.environ.get("GCP_PROJECT", "your-gcp-project-id")
DATASET_ID = os.environ.get("BQ_DATASET", "crm_data")
TABLE_ID = os.environ.get("BQ_TABLE", "leads")

FULL_TABLE_PATH = f"`{GCP_PROJECT}.{DATASET_ID}.{TABLE_ID}`"

def run_bigquery_sql(query: str) -> str:
    """Executes a SQL query against the BigQuery CRM table and returns the results formatted as text."""
    try:
        # Initialize BigQuery client using implicit default credentials
        client = bigquery.Client(project=GCP_PROJECT)
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert rows to standard text format
        rows = [dict(row) for row in results]
        if not rows:
            return "Query returned no results."
        return str(rows)
    except Exception as e:
        return f"BigQuery Execution Error: {str(e)}"

def run_sandbox_process(args: list[str]):
    cmd = args[2:] if IS_LOCAL_MODE and args[:2] == ['do', '--'] else ([SANDBOX_CLI] + args if not IS_LOCAL_MODE else args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10)

def execute_sandbox_command(command: str) -> str:
    """Executes arbitrary POSIX shell/bash scripts inside a local or Cloud Run sandbox."""
    mode = "LOCAL" if IS_LOCAL_MODE else "CLOUD RUN SANDBOX"
    print(f"[ADK Sandbox Tool] Starting {mode} shell run...")
    try:
        res = run_sandbox_process(['do', '--', '/bin/sh', '-c', command])
        if res.returncode != 0:
            return f"Execution Failed!\nExit Code: {res.returncode}\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"
        return res.stdout
    except Exception as err:
        return f"Internal Sandbox Tool Error: {str(err)}"

# ==========================================
# ADK AGENT & RUNNER INITIALIZATION
# ==========================================
@st.cache_resource
def initialize_runner():
    root_agent = Agent(
        name='crm_bigquery_assistant',
        description='ADK agent capable of querying BigQuery datasets and running python scripts to analyze CRM records.',
        model=os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash'),
        instruction=(
            f'You are an expert AI CRM Strategy Analyst.\n'
            f'You have access to a BigQuery table containing CRM leads at path: {FULL_TABLE_PATH}.\n\n'
            '1. Table Schema Awareness:\n'
            '   The CRM table contains columns: CustomerID (INT), FirstName (STRING), LastName (STRING), '
            'Email (STRING), Phone (STRING), Address (STRING), City (STRING), State (STRING), ZipCode (STRING), '
            'Country (STRING), SignupDate (STRING/DATE), LastPurchaseDate (STRING/DATE), TotalSpent (NUMERIC), LeadSource (STRING), Notes (STRING).\n\n'
            '2. Query & Analytics Policy:\n'
            '   - Use `run_bigquery_sql` to execute analytical SQL queries directly on BigQuery.\n'
            '   - Write custom SQL queries to aggregate revenue, compute Customer Lifetime Value (CLV), find top lead acquisition channels, or flag churn risks.\n'
            '   - When necessary, write Python code using `execute_sandbox_command` for complex data manipulation.\n\n'
            '3. Output & Human-in-the-Loop Policy:\n'
            '   - Summarize insights concisely in clear markdown bullet points or tables.\n'
            '   - Provide concrete follow-up task recommendations for sales managers based on your analytical findings.'
        ),
        tools=[
            FunctionTool(func=run_bigquery_sql),
            FunctionTool(func=execute_sandbox_command)
        ]
    )

    adk_app = App(name="crm_bq_sandbox_app", root_agent=root_agent)
    return Runner(app=adk_app, session_service=InMemorySessionService(), auto_create_session=True)

runner = initialize_runner()

# ==========================================
# STREAMLIT UI & CHAT INTERFACE
# ==========================================

# Sidebar
with st.sidebar:
    st.header("💼 CRM BigQuery Monitor")
    st.markdown("---")
    st.markdown("**Status:** Active")
    st.markdown(f"**GCP Project:** `{GCP_PROJECT}`")
    st.markdown(f"**BigQuery Table:** `{DATASET_ID}.{TABLE_ID}`")
    st.markdown(f"**Execution Environment:** `{'Local' if IS_LOCAL_MODE else 'Cloud Run'}`")
    
    st.markdown("---")
    st.caption("Target Table Schema:")
    st.code(
        "CustomerID, FirstName, LastName, Email, Phone, Address, City, State, "
        "ZipCode, Country, SignupDate, LastPurchaseDate, TotalSpent, LeadSource, Notes",
        language="text"
    )

# Chat Session History Setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": f"💼 **CRM BigQuery Assistant Ready.** I am linked to `{FULL_TABLE_PATH}`. Ask me to run SQL metrics, analyze lead performance, or segment top customers!"
        }
    ]

# Render Message Stream
for message in st.session_state.messages:
    avatar = "💼" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User Prompt Box
if prompt := st.chat_input("Ask CRM Assistant to run BigQuery SQL, compute spend averages, or rank leads..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💼"):
        with st.spinner("Executing SQL query on BigQuery Sandbox..."):
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