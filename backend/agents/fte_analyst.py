"""
FTE Analyst Agent - Calculates time savings, automation ROI, and capacity freed
"""
from typing import Dict, Any, List, Optional
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class FTEAnalystAgent:
    def __init__(self):
        # Default assumptions as per CLAUDE.md
        self.default_fte_hours_per_day = 8
        self.default_working_days_per_year = 250

    async def analyze_fte_savings(self, data: List[Dict[str, Any]],
                                task_column: str = None,
                                time_column: str = None,
                                volume_column: str = None,
                                frequency_column: str = None) -> Dict[str, Any]:
        """
        Calculate FTE savings based on time-per-task × volume × frequency
        """
        try:
            logger.info("Starting FTE savings analysis")

            if not data:
                return {"error": "No data provided for analysis"}

            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(data)

            # Auto-detect columns if not provided
            if not task_column:
                task_column = self._detect_task_column(df)
            if not time_column:
                time_column = self._detect_time_column(df)
            if not volume_column:
                volume_column = self._detect_volume_column(df)
            if not frequency_column:
                frequency_column = self._detect_frequency_column(df)

            logger.info(f"Using columns - Task: {task_column}, Time: {time_column}, Volume: {volume_column}, Frequency: {frequency_column}")

            # Validate that required columns exist
            required_cols = [task_column, time_column, volume_column, frequency_column]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return {"error": f"Missing required columns: {missing_cols}"}

            # Calculate time savings for each task
            df = df.copy()  # Avoid modifying original data
            df['time_savings_per_instance_hours'] = (
                pd.to_numeric(df[time_column], errors='coerce') / 60
            ).fillna(0)

            df['daily_time_savings_hours'] = (
                df['time_savings_per_instance_hours'] *
                pd.to_numeric(df[volume_column], errors='coerce').fillna(0) *
                pd.to_numeric(df[frequency_column], errors='coerce').fillna(0)
            )

            # Total calculations
            total_daily_time_savings = df['daily_time_savings_hours'].sum()
            total_annual_time_savings = total_daily_time_savings * self.default_working_days_per_year
            total_fte_equivalent = total_annual_time_savings / (self.default_fte_hours_per_day * self.default_working_days_per_year)

            # Identify automation opportunities (tasks with highest savings)
            df['annual_time_savings'] = df['daily_time_savings_hours'] * self.default_working_days_per_year
            automation_opportunities = df.nlargest(10, 'annual_time_savings')[[
                task_column, 'annual_time_savings', 'daily_time_savings_hours'
            ]].to_dict('records')

            # Calculate potential cost savings (assuming $50/hour fully loaded cost)
            hourly_cost = 50  # This should be configurable
            annual_cost_savings = total_annual_time_savings * hourly_cost

            return {
                "status": "success",
                "analysis_parameters": {
                    "task_column": task_column,
                    "time_column": time_column,
                    "volume_column": volume_column,
                    "frequency_column": frequency_column,
                    "fte_hours_per_day": self.default_fte_hours_per_day,
                    "working_days_per_year": self.default_working_days_per_year
                },
                "results": {
                    "daily_time_saved_hours": round(total_daily_time_savings, 2),
                    "annual_time_saved_hours": round(total_annual_time_savings, 2),
                    "fte_equivalent": round(total_fte_equivalent, 2),
                    "annual_cost_savings": round(annual_cost_savings, 2),
                    "automation_opportunities": automation_opportunities
                },
                "assumptions": [
                    f"FTE hours per day: {self.default_fte_hours_per_day}",
                    f"Working days per year: {self.default_working_days_per_year}",
                    f"Hourly cost for savings calculation: ${hourly_cost}",
                    "Time savings calculated as: (time_per_task_min × volume_per_day × frequency) / 60",
                    "FTE equivalent = Annual time savings / (FTE hours/day × Working days/year)"
                ]
            }

        except Exception as e:
            logger.error(f"Error in FTE analysis: {str(e)}")
            return {"error": str(e)}

    def _detect_task_column(self, df: pd.DataFrame) -> Optional[str]:
        """Auto-detect task/process column"""
        task_indicators = ['task', 'process', 'activity', 'operation', 'job', 'work']
        for col in df.columns:
            if any(indicator in col.lower() for indicator in task_indicators):
                return col
        return df.columns[0] if len(df.columns) > 0 else None

    def _detect_time_column(self, df: pd.DataFrame) -> Optional[str]:
        """Auto-detect time/duration column"""
        time_indicators = ['time', 'duration', 'minutes', 'hours', 'mins', 'hrs']
        for col in df.columns:
            if any(indicator in col.lower() for indicator in time_indicators):
                return col
        return None

    def _detect_volume_column(self, df: pd.DataFrame) -> Optional[str]:
        """Auto-detect volume/quantity column"""
        volume_indicators = ['volume', 'quantity', 'count', 'number', 'qty', 'amount']
        for col in df.columns:
            if any(indicator in col.lower() for indicator in volume_indicators):
                return col
        return None

    def _detect_frequency_column(self, df: pd.DataColumn) -> Optional[str]:
        """Auto-detect frequency column"""
        freq_indicators = ['frequency', 'freq', 'times', 'per_day', 'per_week', 'daily', 'weekly']
        for col in df.columns:
            if any(indicator in col.lower() for indicator in freq_indicators):
                return col
        return None

# Global FTE analyst agent instance
fte_analyst_agent = FTEAnalystAgent()