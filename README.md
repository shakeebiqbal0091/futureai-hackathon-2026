# WorkForce Intelligence Agent (WFIA)

An agentic AI system that automates workforce analytics, identifies FTE savings, and surfaces productivity insights — turning manual HR/ops data pipelines into autonomous intelligence.

## 🏆 FutureAI Global Hackathon 2026

- **Event**: FutureAI Global Hackathon 2026
- **Platform**: Devpost
- **Track**: 🤖 AI Agents & Automation + ⚡ Productivity AI
- **Submission URL**: https://futureai-global-hackthon.devpost.com/
- **Deadline**: July 5, 2026 @ 5:00 PM IST

## 🎯 Project Concept

**Problem Statement**: Organizations waste thousands of analyst-hours manually calculating FTE utilization, identifying process inefficiencies, and building workforce reports. This is repetitive, high-stakes, and completely automatable.

**Solution**: A multi-agent AI system that:
1. Ingests workforce/process data (CSV, Excel, or connected HR tools)
2. Runs automated FTE savings analysis (time-per-task × volume × frequency)
3. Generates natural language insights and executive-ready reports
4. Provides a chat interface for ad-hoc queries on workforce data
5. Outputs actionable automation opportunity rankings

## 📐 Architecture

```
User Interface (React + Tailwind)
        ↓
Orchestrator Agent (Claude claude-sonnet-4-6)
        ↙     ↘     ↙     ↘
Data Ingest → FTE Analyst → Report Writer → Query Agent
        ↓     ↙     ↘     ↓
    Tool Layer (pandas, numpy, charting, export)
```

## 🛠️ Tech Stack

| Layer         | Technology                              |
|---------------|-----------------------------------------|
| AI/LLM        | Claude claude-sonnet-4-6 (Anthropic API)       |
| Orchestration | Custom multi-agent loop (Python)        |
| Backend       | Python (FastAPI)                        |
| Frontend      | React + Tailwind CSS                    |
| Data Layer    | pandas, numpy, openpyxl                 |
| Visualization | matplotlib, seaborn                     |
| Export        | TXT format (PDF/DOCX planned for future)|
| Deployment    | Local development (Vercel/Railway planned)|
| Version Ctrl  | GitHub                                  |

## 📁 Project Structure

```
futureai-hackathon-2026/
├── backend/                  # Python/FastAPI backend
│   ├── main.py               # API entry point
│   ├── agents/               # Specialized AI agents
│   │   ├── orchestrator.py   # Master agent logic
│   │   ├── data_ingest.py    # File parsing + schema detection
│   │   ├── fte_analyst.py    # FTE savings calculations
│   │   ├── report_writer.py  # Narrative generation
│   │   └── query_agent.py    # NL query handler
│   ├── tools/                # Utility functions
│   │   ├── file_tools.py     # CSV/Excel I/O utilities
│   │   ├── chart_tools.py    # Chart generation
│   │   └── export_tools.py   # Report export
│   ├── models/               # Pydantic data models
│   │   └── schemas.py        # API request/response models
│   └── config.py             # Configuration settings
├── frontend/                 # React/Tailwind frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── FileUpload.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── FTEDashboard.jsx
│   │   │   └── ReportViewer.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── sample_data/              # Demo datasets
│   ├── sample_workforce.csv
│   └── sample_process_log.xlsx
├── demo/                     # Demo materials
│   ├── demo_script.md
│   └── screenshots/
└── submission/               # Submission materials
    ├── project_description.md
    └── presentation.pdf
```

## ⚙️ Environment Setup

### Backend Setup
```bash
# Clone repository
git clone https://github.com/your-username/futureai-hackathon-2026.git
cd futureai-hackathon-2026

# Backend setup
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run backend
uvicorn main:app --reload
```

### Frontend Setup
```bash
# Frontend setup
cd ../frontend
npm install
npm run dev
```

## 📝 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /upload` - Upload workforce data file (CSV, Excel, JSON)
- `POST /analyze/fte` - Perform FTE savings analysis
- `POST /query` - Natural language queries about data
- `POST /report/generate` - Generate reports from analysis

## 🧪 Sample Data Format

The system expects workforce data with columns like:
- `task_name` or `process`: Name of the task/process
- `time_per_task_min`: Average time to complete task (in minutes)
- `volume_per_day`: Number of times task is performed daily
- `frequency`: How often task is performed (daily, weekly, etc.)

## 📊 Key Features

### Multi-Agent Architecture
- **Orchestrator**: Routes tasks and maintains context
- **Data Ingest Agent**: Handles file parsing and validation
- **FTE Analyst Agent**: Calculates time savings and automation ROI
- **Report Writer Agent**: Generates narrative insights and executive reports
- **Query Agent**: Handles natural language questions about data

### FTE Calculation
Transparent FTE savings calculation using the formula:
```
Time Savings (hours) = (time_per_task_min × volume_per_day × frequency) / 60
FTE Equivalent = Annual Time Savings / (FTE_hours_per_day × Working_days_per_year)
```

Default assumptions:
- FTE hours per day: 8 hours
- Working days per year: 250 days
- Hourly cost: $50/hour (fully loaded)

## 📱 Features Implemented

✅ File upload (CSV, Excel, JSON)
✅ Natural language chat interface
✅ FTE savings analysis with transparent assumptions
✅ Automation opportunity identification
✅ Basic report generation
✅ Responsive React/Tailwind frontend
✅ RESTful API backend

## 🚀 Next Steps for Hackathon Completion

1. [ ] Add sample datasets to `sample_data/` directory
2. [ ] Record demo video (3-5 minutes)
3. [ ] Capture screenshots (3-5 minimum)
4. [ ] Finalize project description
5. [ ] Create presentation deck
6. [ ] Submit to Devpost before July 5, 2026 @ 5:00 PM IST

## 👥 Team

Solo developer (to be determined)

## 🔗 Important Links

- Hackathon Page: https://futureai-global-hackthon.devpost.com/
- Official Site: https://futureai.lokeshloki.in/
- Anthropic API Docs: https://docs.anthropic.com/