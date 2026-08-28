# 💼 CRM Intelligence Agent

An AI-driven CRM analytics assistant built for hackathons that enables sales teams and managers to query customer records, analyze acquisition channels, and extract sentiment from interaction notes using natural language—all running on a **100% credit-card-free Google Cloud and Gemini stack**.

---

## ✨ Key Features

* 🗣️ **Natural Language to SQL:** Ask plain-English questions about spend, lead channels, and churn risks, and automatically execute queries on BigQuery.
* 📊 **BigQuery Sandbox Integration:** Zero-cost analytical data warehousing without active GCP billing accounts.
* 🤖 **Gemini 2.5 Flash Intelligence:** Extracts lead intent, sentiment, and action items from unstructured text notes.
* ⚡ **Streamlit Web UI:** Intuitive interface for interacting with customer intelligence and running real-time analytical reports.
* ☁️ **Cloud Native & Deployable:** Fully deployable on Streamlit Community Cloud using Service Account secrets.

---

## 🏗️ Architecture
[ User Prompt ]
│
▼
[ Streamlit Web UI ] ──(Gemini 2.5 Flash / AI Studio)──► [ Intent & SQL Generation ]
│                                                           │
├──────────────────(Google Cloud BigQuery)──────────────────┘
│
▼
[ Insights & Executable Action Items ]


---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Orchestration & LLM:** Google Agent Development Kit (ADK) & `google-genai` (Gemini 2.5 Flash via Google AI Studio)
* **Data Warehouse:** [Google Cloud BigQuery Sandbox](https://cloud.google.com/bigquery/docs/sandbox)
* **Language:** Python 3.10+

---

## 🚀 Quickstart (Local Setup)

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/crm-intelligence-agent.git](https://github.com/your-username/crm-intelligence-agent.git)
cd crm-intelligence-agent

2. Set Up Virtual Environment & Install Dependencies
Bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the project root:

Code snippet
GEMINI_API_KEY=your_google_ai_studio_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GCP_PROJECT=your-gcp-project-id
BQ_DATASET=crm_data
BQ_TABLE=leads
4. Run the Streamlit Application
Bash
streamlit run app.py

📜 License
This project is licensed under the MIT License.


<ElicitationsGroup message="Next steps for finalizing your repository:">
  <Elicitation label="Generate a LICENSE file for MIT License" query="Generate the standard text for an MIT License file to include in my GitHub repository."/>
  <Elicitation label="Create a .gitignore file tailored for Python and Streamlit" query="Provide a complete .gitignore file for a Python, Streamlit, and Google Cloud project."/>
</ElicitationsGroup>
