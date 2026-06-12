"""
Configuration settings for the WorkForce Intelligence Agent
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    API_TITLE: str = "WorkForce Intelligence Agent"
    API_DESCRIPTION: str = "An agentic AI system that automates workforce analytics, identifies FTE savings, and surfaces productivity insights"
    API_VERSION: str = "1.0.0"

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

    # Anthropic API Configuration
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # FTE Analysis Defaults
    DEFAULT_FTE_HOURS_PER_DAY: int = int(os.getenv("DEFAULT_FTE_HOURS_PER_DAY", 8))
    DEFAULT_WORKING_DAYS_PER_YEAR: int = int(os.getenv("DEFAULT_WORKING_DAYS_PER_YEAR", 250))
    DEFAULT_HOURLY_COST: float = float(os.getenv("DEFAULT_HOURLY_COST", 50.0))

    # File Upload Configuration
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS: set = {".csv", ".xlsx", ".xls", ".json"}

    # Chart Configuration
    CHART_DPI: int = int(os.getenv("CHART_DPI", 300))
    CHART_FORMAT: str = os.getenv("CHART_FORMAT", "png")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Global config instance
config = Config()