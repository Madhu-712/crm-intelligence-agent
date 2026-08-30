
# 💼 CRM Data & BigQuery Analytics Agent

An enterprise-grade, autonomous CRM intelligence assistant built for sales leaders, data analysts, and strategy teams. This application enables users to query customer records, run complex SQL aggregations on BigQuery, and execute sandbox analytical scripts using natural language—all powered by Google Cloud and the Gemini 3 model engine.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/04ce7abc-8c6f-47e3-b955-cefa6cbb44a3" />


## 🛑 Problem Statement

Modern enterprise CRMs gather immense volumes of customer data, lead touchpoints, and transactional histories. However, extracting operational insights often presents major bottlenecks:

* **SQL & Technical Barriers:** Non-technical sales managers must rely on overworked data teams to write custom SQL queries for basic metrics like churn risk or segment performance.
* **Unstructured Data Silos:** Critical context stored in unstructured sales notes, feedback forms, and support transcripts remains unused in traditional relational dashboards.
* **Delayed Actionable Strategy:** Static analytics tools report *what* happened, but fail to deliver immediate, actionable next steps or automated script-based data manipulation.



## ✨ Key Features

* 🗣️ **Natural Language to BigQuery SQL:** Translate plain English questions into optimized Google BigQuery queries to analyze spend, acquisition channels, and customer segments in real time.
* 🤖 **Gemini 3 Intelligence Engine:** Leverages `gemini-3.6-flash` (with automated resilient fallback ladders) to evaluate intent, analyze unstructured lead notes, and produce executive summaries.
* 🛠️ **Autonomous Tool Calling:** Powered by the Google Agent Development Kit (ADK), enabling the agent to dynamically route between native BigQuery execution and local sandbox Python environments.
* ⚡ **Streamlit Enterprise UI:** Custom-themed, responsive dashboard supporting interactive session history, seamless API credential management, and quick environment resets.
* 🛡️ **Resilient Model Failover & Auto-Retry:** Built-in exponential backoff for transient capacity spikes (`503 UNAVAILABLE`) and dynamic model failover to ensure maximum uptime.

---

## 🌐 Live Demo

* **Web Application:** [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)
* **Video Walkthrough / Pitch:** [https://youtube.com/your-demo-video](https://youtube.com/your-demo-video)

---

## 📸 Application Screenshot


```

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

```

---

## 👤 User Personas

| Persona | Role | Primary Goal | How They Use the Agent |
| :--- | :--- | :--- | :--- |
| **Sales Executives** | VP of Sales / Regional Manager | Identify immediate revenue opportunities & pipeline health | Asks high-level questions on channel revenue, lead conversion, and rep performance without writing code. |
| **Data Analysts** | Analytics Lead | Speed up exploratory analysis & ad-hoc data requests | Uses natural language to instantly query BigQuery tables and generate initial analytical data frames. |
| **Customer Success** | CS Lead / Account Manager | Reduce churn & spot expansion targets | Queries purchase histories and unstructured customer notes to flag accounts at risk of churning. |

---

## 🏗️ System Architecture


```

```
             +-----------------------------------+
             |        Streamlit Web UI           |
             +-----------------------------------+
                               |
                               v
             +-----------------------------------+
             |    ADK Agent (Gemini 3 Engine)    |
             +-----------------------------------+
               /                               \
              /                                 \
             v                                   v

```

+-----------------------------+     +-----------------------------+
|    Function Tool: BigQuery   |     |    Function Tool: Sandbox   |
|   `run_bigquery_sql()`      |     | `execute_sandbox_command()` |
+-----------------------------+     +-----------------------------+
|                                   |
v                                   v
+-----------------------------+     +-----------------------------+
|    Google Cloud BigQuery    |     |   Local / Isolated Python   |
|     (`crm_data.leads`)      |     |       Runtime Environment   |
+-----------------------------+     +-----------------------------+

```

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

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

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

```

---

## 🗺️ Feature Roadmap

* [x] **Phase 1: Foundation (Current)** — Streamlit UI, ADK multi-tool routing, BigQuery integration, resilient Gemini 3 failover ladder.
* [ ] **Phase 2: Visualizations** — Auto-generation of interactive Plotly/Altair charts directly from SQL query outputs.
* [ ] **Phase 3: Multi-Agent Collaboration** — Specialized sub-agents for dedicated Lead Scoring, Automated Email Drafting, and Predictive Churn Analytics.
* [ ] **Phase 4: Write-back Capabilities** — Controlled CRM update pipelines allowing authorized users to update lead statuses via natural language commands.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome!

1. Fork the Project repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
