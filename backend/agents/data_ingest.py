"""
Data Ingest Agent - Handles file parsing, schema detection, and data validation
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataIngestAgent:
    def __init__(self):
        self.supported_formats = {'.csv', '.xlsx', '.xls', '.json'}

    async def ingest_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Ingest and parse workforce/process data files
        """
        try:
            file_path = Path(file_path)
            logger.info(f"Ingesting file: {file_path}")

            if not file_path.exists():
                return {"error": f"File not found: {file_path}"}

            file_extension = file_path.suffix.lower()

            if file_extension not in self.supported_formats:
                return {"error": f"Unsupported file format: {file_extension}"}

            # Load data based on file type
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_extension == '.json':
                df = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file format: {file_extension}"}

            # Basic data validation
            validation_result = self._validate_data(df)

            # Schema detection
            schema_info = self._detect_schema(df)

            return {
                "status": "success",
                "data": df.to_dict('records'),  # Convert to serializable format
                "shape": df.shape,
                "columns": list(df.columns),
                "validation": validation_result,
                "schema": schema_info
            }

        except Exception as e:
            logger.error(f"Error ingesting file {file_path}: {str(e)}")
            return {"error": str(e)}

    def _validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform basic data validation"""
        try:
            validation = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "has_data": len(df) > 0 and len(df.columns) > 0
            }

            # Check for common workforce data columns
            workforce_indicators = ['employee', 'task', 'time', 'duration', 'volume', 'frequency', 'process']
            found_indicators = [col for col in df.columns
                              if any(indicator in col.lower() for indicator in workforce_indicators)]
            validation["workforce_indicators"] = found_indicators

            return validation

        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            return {"error": str(e)}

    def _detect_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect and describe the data schema"""
        try:
            schema = {
                "columns": [],
                "numeric_columns": [],
                "categorical_columns": [],
                "date_columns": []
            }

            for col in df.columns:
                col_info = {
                    "name": col,
                    "type": str(df[col].dtype),
                    "null_count": int(df[col].isnull().sum()),
                    "unique_values": int(df[col].nunique())
                }

                # Categorize column types
                if pd.api.types.is_numeric_dtype(df[col]):
                    schema["numeric_columns"].append(col)
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    schema["date_columns"].append(col)
                else:
                    schema["categorical_columns"].append(col)

                col_info["sample_values"] = df[col].dropna().head(5).tolist()
                schema["columns"].append(col_info)

            return schema

        except Exception as e:
            logger.error(f"Error detecting schema: {str(e)}")
            return {"error": str(e)}

# Global data ingest agent instance
data_ingest_agent = DataIngestAgent()