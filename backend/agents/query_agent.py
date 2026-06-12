"""
Query Agent - Handles free-form NL questions about the loaded dataset
"""
from typing import Dict, Any, Optional, List
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class QueryAgent:
    def __init__(self):
        self.current_data = None
        self.data_summary = None

    def load_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Load data for querying"""
        try:
            if not data:
                return {"error": "No data provided"}

            self.current_data = pd.DataFrame(data)
            self.data_summary = self._create_data_summary()

            return {
                "status": "success",
                "message": f"Loaded {len(self.current_data)} records with {len(self.current_data.columns)} columns",
                "summary": self.data_summary
            }

        except Exception as e:
            logger.error(f"Error loading data for query agent: {str(e)}")
            return {"error": str(e)}

    def handle_query(self, query: str) -> Dict[str, Any]:
        """
        Handle natural language queries about the dataset
        """
        try:
            logger.info(f"Processing query: {query}")

            if self.current_data is None:
                return {"error": "No data loaded. Please load data first."}

            query_lower = query.lower().strip()

            # Handle different types of queries
            if any(word in query_lower for word in ['summary', 'overview', 'describe', 'stats']):
                return self._handle_summary_query()
            elif any(word in query_lower for word in ['columns', 'fields', 'variables']):
                return self._handle_columns_query()
            elif any(word in query_lower for word in ['rows', 'records', 'count', 'how many']):
                return self._handle_count_query()
            elif any(word in query_lower for word in ['missing', 'null', 'empty']):
                return self._handle_missing_data_query()
            elif any(word in query_lower for word in ['unique', 'distinct', 'different']):
                return self._handle_unique_values_query()
            else:
                return self._handle_general_query(query)

        except Exception as e:
            logger.error(f"Error handling query '{query}': {str(e)}")
            return {"error": str(e)}

    def _create_data_summary(self) -> Dict[str, Any]:
        """Create a summary of the loaded data"""
        try:
            df = self.current_data
            summary = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "data_types": df.dtypes.astype(str).to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
            }
            return summary
        except Exception as e:
            logger.error(f"Error creating data summary: {str(e)}")
            return {"error": str(e)}

    def _handle_summary_query(self) -> Dict[str, Any]:
        """Handle summary/overview queries"""
        if not self.data_summary:
            return {"error": "No data summary available"}

        return {
            "status": "success",
            "query_type": "summary",
            "response": f"The dataset contains {self.data_summary['row_count']} records "
                       f"with {self.data_summary['column_count']} columns. "
                       f"Key columns include: {', '.join(self.data_summary['columns'][:5])}{'...' if len(self.data_summary['columns']) > 5 else ''}",
            "summary": self.data_summary
        }

    def _handle_columns_query(self) -> Dict[str, Any]:
        """Handle columns/fields queries"""
        return {
            "status": "success",
            "query_type": "columns",
            "response": f"The dataset has {len(self.current_data.columns)} columns: "
                       f"{', '.join(self.current_data.columns.tolist())}",
            "columns": self.current_data.columns.tolist(),
            "data_types": self.current_data.dtypes.astype(str).to_dict()
        }

    def _handle_count_query(self) -> Dict[str, Any]:
        """Handle count/record queries"""
        return {
            "status": "success",
            "query_type": "count",
            "response": f"The dataset contains {len(self.current_data):,} records.",
            "record_count": len(self.current_data)
        }

    def _handle_missing_data_query(self) -> Dict[str, Any]:
        """Handle missing data queries"""
        missing_counts = self.current_data.isnull().sum()
        total_missing = missing_counts.sum()

        if total_missing == 0:
            response = "The dataset has no missing values."
        else:
            missing_cols = missing_counts[missing_counts > 0]
            response = f"The dataset has {total_missing:,} missing values across {len(missing_cols)} columns. "
            response += f"Columns with missing data: {', '.join(missing_cols.index.tolist())}"

        return {
            "status": "success",
            "query_type": "missing_data",
            "response": response,
            "missing_counts": missing_counts.to_dict(),
            "total_missing": int(total_missing)
        }

    def _handle_unique_values_query(self) -> Dict[str, Any]:
        """Handle unique/distinct values queries"""
        # Ask which column they want to know about unique values for
        return {
            "status": "success",
            "query_type": "unique_values",
            "response": "To check unique values, please specify which column you're interested in. "
                       f"Available columns: {', '.join(self.current_data.columns.tolist())}",
            "available_columns": self.current_data.columns.tolist()
        }

    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general queries that don't match specific patterns"""
        return {
            "status": "success",
            "query_type": "general",
            "response": f"I received your query: '{query}'. "
                       f"The dataset contains {len(self.current_data)} records about workforce/process data. "
                       f"Try asking about summary, columns, record count, or missing data for more specific insights.",
            "suggestions": [
                "What's a summary of the data?",
                "What columns are available?",
                "How many records are there?",
                "Are there any missing values?"
            ]
        }

# Global query agent instance
query_agent = QueryAgent()