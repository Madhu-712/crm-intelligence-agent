
# 💼 CRM Data & BigQuery Analytics Agent

An enterprise-grade, autonomous CRM intelligence assistant built for sales leaders, data analysts, and strategy teams. This application enables users to query customer records, run complex SQL aggregations on BigQuery, and execute sandbox analytical scripts using natural language—all powered by Google Cloud and the Gemini 3 model engine.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/04ce7abc-8c6f-47e3-b955-cefa6cbb44a3" />

## Project Overview

This application delivers a modern CRM dashboard that lets teams:

- monitor account health and revenue performance
- explore customer and lead records in near real time
- query BigQuery datasets using SQL
- use an AI assistant to ask business questions in natural language
- receive event-driven notifications when new CRM records are inserted

Built around a Google Cloud data stack and an AI-driven workflow, CRM AGENTS helps organizations move from raw CRM information to decisions that improve retention, pipeline conversion, and customer expansion.


## 🛑 Problem Statement

Modern enterprise CRMs gather immense volumes of customer data, lead touchpoints, and transactional histories. However, extracting operational insights often presents major bottlenecks:
- sales teams cannot quickly identify at-risk accounts
- customer success teams lack early churn signals
- revenue leaders work with stale reports instead of live intelligence
- data analysts spend too much time preparing dashboards instead of deriving insights

* **SQL & Technical Barriers:** Non-technical sales managers must rely on overworked data teams to write custom SQL queries for basic metrics like churn risk or segment performance.
* **Unstructured Data Silos:** Critical context stored in unstructured sales notes, feedback forms, and support transcripts remains unused in traditional relational dashboards.
* **Delayed Actionable Strategy:** Static analytics tools report *what* happened, but fail to deliver immediate, actionable next steps or automated script-based data manipulation.

CRM AGENTS addresses this gap by providing a unified operating layer for CRM insights, AI analysis, and BigQuery-backed reporting.



## ✨ Key Features

* 🗣️ **Natural Language to BigQuery SQL:** Translate plain English questions into optimized Google BigQuery queries to analyze spend, acquisition channels, and customer segments in real time.
* 🤖 **Gemini 3 Intelligence Engine:** Leverages `gemini-3.6-flash` (with automated resilient fallback ladders) to evaluate intent, analyze unstructured lead notes, and produce executive summaries.
* 🛠️ **Autonomous Tool Calling:** Powered by the Google Agent Development Kit (ADK), enabling the agent to dynamically route between native BigQuery execution and local sandbox Python environments.
* ⚡ **Streamlit Enterprise UI:** Custom-themed, responsive dashboard supporting interactive session history, seamless API credential management, and quick environment resets.
* 🛡️ **Resilient Model Failover & Auto-Retry:** Built-in exponential backoff for transient capacity spikes (`503 UNAVAILABLE`) and dynamic model failover to ensure maximum uptime.
*  **CRM lead explorer** with filters and CSV export
* **Pub/Sub**-driven alerting for new BigQuery insert notifications

---

## 🌐 Live Demo

* **Web Application:** [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)
* **Video Walkthrough / Pitch:** [https://youtube.com/your-demo-video](https://youtube.com/your-demo-video)

---

## 📸 Application Screenshot

+-----------------------------------------------------------------------------------+
| 🔑 API Authentication   |  💼 CRM Intelligence Agent Ready.                      |
| [ ************* ]      |                                                           |
|                        |  👤 User: Show top 5 lead sources by total revenue.       |
| 💼 CRM BigQuery        |                                                           |
| Project: notebooklm... |  💼 Assistant: Running BigQuery SQL...                     |
| Table: crm_data.leads  |  +----------------+-----------------+                     |
|                        |  | Lead Source    | Total Revenue   |                     |
| [🗑️ Clear Chat History]|  +----------------+-----------------+                     |
|                        |  | Organic Search | $145,200        |                     |
|                        |  | Referral       | $98,400         |                     |
|                        |  +----------------+-----------------+                     |
+-----------------------------------------------------------------------------------+


- Executive Dashboard: overview of KPI cards, revenue metrics, and customer risk indicators

   <img width="1470" height="1140" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/7f070128-9555-4a82-84e9-a1611ddb9f31" />


- AI Assistant: natural-language CRM query and recommendation panel

  <img width="1470" height="1140" alt="AI assistant" src="https://github.com/user-attachments/assets/143d873a-d635-4aa6-a22d-d1663ce65fd9" />
  

- BigQuery SQL Terminal: SQL editor for CRM data exploration

  <img width="1470" height="1140" alt="BQ sql terminal" src="https://github.com/user-attachments/assets/093cdbea-5f08-494e-a431-574319be1409" />
  

- CRM Lead Explorer: filtered customer list with export-ready CSV output

  
<img width="1470" height="1140" alt="CRM data explorer" src="https://github.com/user-attachments/assets/03574d85-7b99-4832-921a-89c43d445132" />
  


## 👤 User Personas

| Persona | Role | Primary Goal | How They Use the Agent |
| :--- | :--- | :--- | :--- |
| **Sales Executives** | VP of Sales / Regional Manager | Identify immediate revenue opportunities & pipeline health | Asks high-level questions on channel revenue, lead conversion, and rep performance without writing code. |
| **Data Analysts** | Analytics Lead | Speed up exploratory analysis & ad-hoc data requests | Uses natural language to instantly query BigQuery tables and generate initial analytical data frames. |
| **Customer Success** | CS Lead / Account Manager | Reduce churn & spot expansion targets | Queries purchase histories and unstructured customer notes to flag accounts at risk of churning. |

---

## 🏗️ System Architecture


```

+---------------------------+
| User Interface            |
| Streamlit Web App         |
+------------+--------------+
             |
             v
+---------------------------+
| CRM Analytics Layer       |
| Python + Pandas + Logic   |
+------------+--------------+
             |
             v
+---------------------------+
| AI Layer                  |
| Gemini / Google GenAI     |
| ADK Agent Tools           |
+------------+--------------+
             |
             v
+---------------------------+
| Data Layer                |
| BigQuery Table / Dataset  |
| Pub/Sub Notifications     |
+---------------------------+
```

The architecture combines:

- a front-end dashboard for business users
- a Python analytics engine for aggregations and transformations
- a Google Cloud data layer for scalable CRM data storage and querying
- AI-driven reasoning to answer natural language questions and recommend next steps



---

## 🛠️ Tech Stack

* **Frontend:** Streamlit 1.x
* **AI Orchestration & LLM Framework:** Google Agent Development Kit (ADK), `google-genai` (Gemini 3.6 Flash / Gemini 3 Flash)
* **Data Warehouse:** Google Cloud BigQuery
* **Authentication & Credentials:** Google OAuth2 (`google-oauth2`), Streamlit Secrets Management
* **Language & Runtime:** Python 3.10+

---

## 📂 Project Structure


```

crm-intelligence-agent/
│
├── .streamlit/
│   └── secrets.toml            # Optional local secrets (GCP SA & API Keys)
│
├── app.py                      # Main Streamlit application & ADK agent definition
├── requirements.txt            # Project dependencies
├── .gitignore                  # Ignored files and secret exclusions
├── README.md                   # Project documentation
└── LICENSE                     # MIT License

```

---

## 🚀 Execution Structure (Local Setup)

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/crm-intelligence-agent.git](https://github.com/your-username/crm-intelligence-agent.git)
cd crm-intelligence-agent

```

### 2. Set Up Virtual Environment & Install Dependencies

#### 1. Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

#### 2. Configure Cloud Secrets

Set the following environment variables or store them in Streamlit secrets:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GEMINI_API_KEY="your-gemini-key"
export BIGQUERY_PROJECT_ID="your-project-id"
export BIGQUERY_DATASET_ID="crm_dataset"
export BIGQUERY_TABLE_ID="crm_leads"
export PUBSUB_SUBSCRIPTION="projects/your-project/subscriptions/your-subscription"


```

### 3. Authenticate Google Cloud & Credentials

For local execution, authenticate standard Application Default Credentials (ADC):

```bash
gcloud auth application-default login

```

Alternatively, configure `.streamlit/secrets.toml` or set environment variables:

```env
GEMINI_API_KEY=your_gemini_api_key
GCP_PROJECT=notebooklm-491108
BQ_DATASET=crm_data
BQ_TABLE=leads

```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
OR
streamlit run app.py --server.port 8503 --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

```
Once running, the app provides five areas:

1. Executive Dashboard
2. AI Assistant
3. CRM Leads Explorer
4. BigQuery SQL Terminal
5. Pub/Sub Notifications

## 🗺️ Feature Roadmap

* [x] **Phase 1: Foundation (Current)** — Streamlit UI, ADK multi-tool routing, BigQuery integration, resilient Gemini 3 failover ladder.
* [ ] **Phase 2: Visualizations** — Auto-generation of interactive Plotly/Altair charts directly from SQL query outputs.
* [ ] **Phase 3: Multi-Agent Collaboration** — Specialized sub-agents for dedicated Lead Scoring, Automated Email Drafting, and Predictive Churn Analytics.
* [ ] **Phase 4: Write-back Capabilities** — Controlled CRM update pipelines allowing authorized users to update lead statuses via natural language commands.
* [ ] **Phase 5:  CRM integrations** with Salesforce, HubSpot, and Zoho
* [ ] **Phase 6: Summary** automated weekly executive summaries
* [ ] **Phase 7: role-based access control** for sales and leadership teams
* [ ] **Phase 8: expansion**into multi-region analytics and enterprise data governance
* [ ] **Phase 9: smarter autonomous agents** for lead qualification and opportunity scoring



---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome!

1. Fork the Project repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## Why CRM AGENTS

CRM AGENTS exists to make customer intelligence more actionable, accessible, and scalable. Instead of waiting for monthly reports or manual spreadsheet reviews, teams can use an AI-enhanced CRM experience to:

- react faster to risk
- prioritize high-value opportunities
- unify business metrics with technical data access
- improve visibility across the full customer lifecycle

It is designed for organizations that need both operational clarity and strategic foresight.


## LICENSE

MIT License

Copyright (c) 2026 CRM AGENTS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

CRM AGENTS is built for smarter customer operations, stronger retention, and faster revenue decision-making.


```


