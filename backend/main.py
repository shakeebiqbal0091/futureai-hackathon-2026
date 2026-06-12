"""
FastAPI entry point for WorkForce Intelligence Agent
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import pandas as pd
from pathlib import Path

# Import our agents and tools
from agents.orchestrator import orchestrator
from agents.data_ingest import data_ingest_agent
from agents.fte_analyst import fte_analyst_agent
from agents.report_writer import report_writer_agent
from agents.query_agent import query_agent
from tools.file_tools import file_tools
from config import config

# Set up logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS if config.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class FileUploadResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data_shape: Optional[tuple] = None
    columns: Optional[list] = None
    error: Optional[str] = None

class FTEAnalysisRequest(BaseModel):
    task_column: Optional[str] = None
    time_column: Optional[str] = None
    volume_column: Optional[str] = None
    frequency_column: Optional[str] = None

class FTEAnalysisResponse(BaseModel):
    status: str
    analysis_parameters: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    assumptions: Optional[list] = None
    error: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    status: str
    response: str
    query_type: Optional[str] = None
    error: Optional[str] = None

class ReportRequest(BaseModel):
    format: str = "summary"

class ReportResponse(BaseModel):
    status: str
    report_type: str
    content: str
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "WorkForce Intelligence Agent API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": config.API_VERSION}

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process workforce data file"""
    try:
        logger.info(f"Received file upload: {file.filename}")

        # Save uploaded file temporarily
        temp_file_path = f"/tmp/{file.filename}"
        content = await file.read()

        # Check file size
        if len(content) > config.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")

        # Save file
        with open(temp_file_path, "wb") as f:
            f.write(content)

        # Process file based on extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension == ".csv":
            result = file_tools.read_csv(temp_file_path)
        elif file_extension in [".xlsx", ".xls"]:
            result = file_tools.read_excel(temp_file_path)
        elif file_extension == ".json":
            result = file_tools.read_json(temp_file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")

        if result.get("status") == "success":
            # Load data into agents for querying
            if "data" in result:
                data_ingest_result = data_ingest_agent.ingest_file(temp_file_path)
                if data_ingest_result.get("status") == "success":
                    # Load data into query agent
                    query_agent.load_data(data_ingest_result["data"])
                    orchestrator.current_data = data_ingest_result["data"]

            return FileUploadResponse(
                status="success",
                message="File uploaded and processed successfully",
                data_shape=result.get("shape"),
                columns=result.get("columns")
            )
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))

    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/fte", response_model=FTEAnalysisResponse)
async def analyze_fte(request: FTEAnalysisRequest):
    """Perform FTE savings analysis"""
    try:
        if orchestrator.current_data is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a file first.")

        result = await fte_analyst_agent.analyze_fte_savings(
            data=orchestrator.current_data,
            task_column=request.task_column,
            time_column=request.time_column,
            volume_column=request.volume_column,
            frequency_column=request.frequency_column
        )

        if result.get("status") == "success":
            return FTEAnalysisResponse(
                status="success",
                analysis_parameters=result.get("analysis_parameters"),
                results=result.get("results"),
                assumptions=result.get("assumptions")
            )
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Analysis failed"))

    except Exception as e:
        logger.error(f"Error in FTE analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_data(request: QueryRequest):
    """Handle natural language queries about the data"""
    try:
        if orchestrator.current_data is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a file first.")

        result = query_agent.handle_query(request.query)

        if result.get("status") == "success":
            return QueryResponse(
                status="success",
                response=result.get("response", ""),
                query_type=result.get("query_type"),
                error=None
            )
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Query failed"))

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """Generate reports from analysis results"""
    try:
        if orchestrator.current_data is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a file first.")

        # For now, generate a basic report - in future versions this would use stored analysis results
        narrative_result = await report_writer_agent.generate_narrative_summary({
            "status": "success",
            "results": {
                "daily_time_saved_hours": 0,
                "annual_time_saved_hours": 0,
                "fte_equivalent": 0,
                "annual_cost_savings": 0,
                "automation_opportunities": []
            }
        })

        if narrative_result.get("status") == "success":
            return ReportResponse(
                status="success",
                report_type="narrative_summary",
                content=narrative_result.get("narrative", "Report generated")
            )
        else:
            raise HTTPException(status_code=400, detail=narrative_result.get("error", "Report generation failed"))

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT, reload=config.DEBUG)