"""
Pydantic data models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Data Ingest Models
class FileUploadResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    shape: Optional[tuple] = None
    columns: Optional[List[str]] = None
    validation: Optional[Dict[str, Any]] = None
    schema: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# FTE Analysis Models
class FTEAnalysisRequest(BaseModel):
    task_column: Optional[str] = None
    time_column: Optional[str] = None
    volume_column: Optional[str] = None
    frequency_column: Optional[str] = None

class FTEAnalysisResponse(BaseModel):
    status: str
    analysis_parameters: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    assumptions: Optional[List[str]] = None
    error: Optional[str] = None

# Report Generation Models
class ReportGenerationRequest(BaseModel):
    format: str = Field(default="summary", description="Report format: summary or executive")
    include_charts: bool = Field(default=True, description="Whether to include charts")

class ReportGenerationResponse(BaseModel):
    status: str
    report_type: Optional[str] = None
    content: Optional[str] = None
    generated_at: Optional[datetime] = None
    error: Optional[str] = None

# Query Models
class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question about the data")

class QueryResponse(BaseModel):
    status: str
    query_type: Optional[str] = None
    response: Optional[str] = None
    query: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    columns: Optional[List[str]] = None
    data_types: Optional[Dict[str, str]] = None
    record_count: Optional[int] = None
    missing_counts: Optional[Dict[str, Any]] = None
    total_missing: Optional[int] = None
    available_columns: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    error: Optional[str] = None

# Orchestrator Models
class TaskRouteRequest(BaseModel):
    task_type: str = Field(..., description="Type of task: ingest_data, analyze_fte, generate_report, query_data")
    payload: Dict[str, Any] = Field(..., description="Task-specific payload")

class TaskRouteResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None

# Health Check Model
class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"