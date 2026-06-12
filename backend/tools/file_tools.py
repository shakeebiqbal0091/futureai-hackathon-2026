"""
File I/O utilities for CSV, Excel, and JSON processing
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileTools:
    @staticmethod
    def read_csv(file_path: Union[str, Path], **kwargs) -> Dict[str, Any]:
        """Read CSV file"""
        try:
            df = pd.read_csv(file_path, **kwargs)
            return {
                "status": "success",
                "data": df.to_dict('records'),
                "shape": df.shape,
                "columns": list(df.columns)
            }
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def read_excel(file_path: Union[str, Path], **kwargs) -> Dict[str, Any]:
        """Read Excel file"""
        try:
            df = pd.read_excel(file_path, **kwargs)
            return {
                "status": "success",
                "data": df.to_dict('records'),
                "shape": df.shape,
                "columns": list(df.columns)
            }
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def read_json(file_path: Union[str, Path], **kwargs) -> Dict[str, Any]:
        """Read JSON file"""
        try:
            df = pd.read_json(file_path, **kwargs)
            return {
                "status": "success",
                "data": df.to_dict('records'),
                "shape": df.shape,
                "columns": list(df.columns)
            }
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def save_csv(data: Union[pd.DataFrame, List[Dict]], file_path: Union[str, Path]) -> Dict[str, Any]:
        """Save data to CSV file"""
        try:
            if isinstance(data, list):
                df = pd.DataFromDict(data)
            else:
                df = data

            df.to_csv(file_path, index=False)
            return {
                "status": "success",
                "message": f"Data saved to {file_path}",
                "shape": df.shape
            }
        except Exception as e:
            logger.error(f"Error saving CSV file {file_path}: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get basic file information"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}

            stat = path.stat()
            return {
                "status": "success",
                "file_path": str(path),
                "file_size": stat.st_size,
                "file_extension": path.suffix.lower(),
                "modified_time": stat.st_mtime
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return {"error": str(e)}

# Global file tools instance
file_tools = FileTools()