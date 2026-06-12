# CLAUDE.md — FutureAI Global Hackathon 2026

## 🏆 Hackathon Context

| Field              | Details                                                  |
|--------------------|----------------------------------------------------------|
| Event              | FutureAI Global Hackathon 2026                           |
| Platform           | Devpost                                                  |
| Submission URL     | https://futureai-global-hackthon.devpost.com/            |
| Deadline           | **July 5, 2026 @ 5:00 PM IST**                          |
| Track Chosen       | 🤖 AI Agents & Automation + ⚡ Productivity AI           |
| Team               | Solo / TBD                                               |
| Status             | 🟡 In Progress                                           |

---

## 🎯 Project Concept

**Project Name:** WorkForce Intelligence Agent (WFIA)

**Tagline:** _An agentic AI system that automates workforce analytics, identifies FTE savings, and surfaces productivity insights — turning manual HR/ops data pipelines into autonomous intelligence._

**Core Problem Statement:**
> "How can AI improve human productivity?" — Organizations waste thousands of analyst-hours manually calculating FTE utilization, identifying process inefficiencies, and building workforce reports. This is repetitive, high-stakes, and completely automatable.

**Solution:**
A multi-agent AI system that:
1. Ingests workforce/process data (CSV, Excel, or connected HR tools)
2. Runs automated FTE savings analysis (time-per-task × volume × frequency)
3. Generates natural language insights and executive-ready reports
4. Provides a chat interface for ad-hoc queries on workforce data
5. Outputs actionable automation opportunity rankings

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│         (Web App — React + Tailwind)                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Orchestrator Agent                      │
│   (Claude claude-sonnet-4-6 via Anthropic API)              │
│   - Routes tasks to specialist sub-agents            │
│   - Maintains conversation + context state           │
└────┬──────────┬──────────┬──────────┬───────────────┘
     │          │          │          │
┌────▼──┐  ┌───▼───┐  ┌───▼───┐  ┌──▼────────┐
│ Data  │  │  FTE  │  │Report │  │  Query    │
│Ingest │  │Analyst│  │Writer │  │  Agent    │
│Agent  │  │Agent  │  │Agent  │  │           │
└───────┘  └───────┘  └───────┘  └───────────┘
     │          │          │          │
┌────▼──────────▼──────────▼──────────▼───────────────┐
│              Tool Layer                              │
│  - pandas/numpy (data processing)                    │
│  - File I/O (CSV, Excel, JSON)                       │
│  - Chart generation (matplotlib/seaborn)             │
│  - PDF/DOCX report export                            │
└─────────────────────────────────────────────────────┘
```

**Agent Roles:**
- **Orchestrator:** Interprets user intent, delegates, aggregates responses
- **Data Ingest Agent:** Parses uploaded files, detects schema, validates data quality
- **FTE Analyst Agent:** Calculates time savings, automation ROI, capacity freed
- **Report Writer Agent:** Converts analysis into narrative summaries + exec decks
- **Query Agent:** Handles free-form NL questions about the loaded dataset

---

## 🛠️ Tech Stack

| Layer         | Technology                              |
|---------------|-----------------------------------------|
| AI/LLM        | Claude claude-sonnet-4-6 (Anthropic API)       |
| Orchestration | Custom multi-agent loop (Python)        |
| Backend       | Python (FastAPI or Flask)               |
| Frontend      | React + Tailwind CSS                    |
| Data Layer    | pandas, numpy, openpyxl                 |
| Visualization | matplotlib, seaborn, plotly             |
| Export        | python-docx, reportlab (PDF)            |
| Deployment    | Vercel (frontend) + Railway/Render (API)|
| Version Ctrl  | GitHub                                  |

---

## 📁 Project Structure

```
futureai-hackathon-2026/
├── CLAUDE.md                    ← This file (project bible)
├── README.md                    ← Public-facing project description
├── backend/
│   ├── main.py                  ← FastAPI entry point
│   ├── agents/
│   │   ├── orchestrator.py      ← Master agent logic
│   │   ├── data_ingest.py       ← File parsing + schema detection
│   │   ├── fte_analyst.py       ← FTE savings calculations
│   │   ├── report_writer.py     ← Narrative generation
│   │   └── query_agent.py       ← NL query handler
│   ├── tools/
│   │   ├── file_tools.py        ← CSV/Excel I/O utilities
│   │   ├── chart_tools.py       ← Chart generation
│   │   └── export_tools.py      ← PDF/DOCX export
│   ├── models/
│   │   └── schemas.py           ← Pydantic data models
│   └── config.py                ← API keys, settings
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── InsightCard.jsx
│   │   │   ├── FTEDashboard.jsx
│   │   │   └── ReportViewer.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── sample_data/
│   ├── sample_workforce.csv     ← Demo dataset for judges
│   └── sample_process_log.xlsx
├── demo/
│   ├── demo_script.md           ← Walkthrough for video
│   └── screenshots/
└── submission/
    ├── project_description.md
    └── presentation.pdf
```

---

## ⚖️ Judging Criteria Alignment

| Criteria              | Weight | Our Strategy                                                  |
|-----------------------|--------|---------------------------------------------------------------|
| Innovation            | 30%    | Multi-agent FTE automation — not a chatbot, a system         |
| Technical Complexity  | 25%    | Real agentic loop, tool use, structured outputs, multi-step  |
| Real-world Impact     | 20%    | Direct ROI story: hours saved → cost saved → headcount freed |
| UI/UX                 | 15%    | Clean dashboard with clear data → insight → action flow      |
| Presentation          | 10%    | Polished demo video with narrated walkthrough                 |

---

## 📦 Submission Checklist

- [ ] Project Title finalized
- [ ] Project Description written
- [ ] GitHub Repository created (public)
- [ ] Backend MVP working (agents functional)
- [ ] Frontend MVP working (UI connected to API)
- [ ] Sample data uploaded and tested
- [ ] Demo Video recorded (3–5 min)
- [ ] Screenshots captured (min. 3–5)
- [ ] Technologies Used list finalized
- [ ] Team Information filled on Devpost
- [ ] Optional: Presentation deck (Gamma)
- [ ] Optional: Live demo link (deployed)
- [ ] **Submitted on Devpost before July 5, 2026 @ 5:00 PM IST**

---

## 🗓️ Build Timeline

| Phase | Dates         | Deliverables                                            |
|-------|---------------|---------------------------------------------------------|
| 1     | Day 1–2       | Repo setup, architecture finalized, agent scaffolding   |
| 2     | Day 3–5       | Core agent logic (FTE analyst + data ingest working)    |
| 3     | Day 6–8       | Frontend built, API connected, end-to-end flow working  |
| 4     | Day 9–10      | Polish UI, write README, record demo video              |
| 5     | Day 11        | Final testing, Devpost submission                       |

---

## 🔑 Key Design Decisions

### Why Multi-Agent over Single LLM?
- Separation of concerns = more reliable outputs per task
- Easier to debug, extend, and explain to judges
- Demonstrates real agentic architecture understanding

### Why FTE/Workforce Analytics?
- Directly tied to measurable business value (quantifiable ROI)
- Aligns with "AI Agents & Automation" + "Productivity AI" tracks
- Real problem with existing manual workflows — not a toy use case

### FTE Calculation Assumptions (must be explicit in outputs)
- Time savings = (manual_time_min × volume_per_day × working_days) / 60 / FTE_hours_per_day
- FTE hours/day default = 8 hours
- Working days/year default = 250
- Automation coverage assumption = stated per task, not assumed globally

---

## ⚙️ Environment Setup

```bash
# Clone repo
git clone https://github.com/[your-username]/futureai-hackathon-2026.git
cd futureai-hackathon-2026

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env

# Run backend
uvicorn main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

---

## 📝 Notes for Claude (AI Assistant)

- **This is a hackathon project** — prioritize working demos over perfect code
- **Model to use:** `claude-sonnet-4-6` in all API calls
- **FTE calculations must be transparent** — always show the formula + assumptions in outputs
- **Agent tool calls** should be logged visibly in the UI so judges can see the system working
- **Tone:** Technical but accessible — judges include both AI engineers and business professionals
- **Do not over-engineer** — a clean working MVP beats a complex broken system
- **Demo-first mindset** — every feature built should be demonstrable in a 5-minute video

---

## 🔗 Important Links

- Hackathon Page: https://futureai-global-hackthon.devpost.com/
- Official Site: https://futureai.lokeshloki.in/
- Anthropic API Docs: https://docs.anthropic.com/
- Submission Deadline: **July 5, 2026 @ 5:00 PM IST**
