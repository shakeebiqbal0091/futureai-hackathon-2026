"""
Chart generation utilities using matplotlib and seaborn
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union
import logging
import io
import base64

logger = logging.getLogger(__name__)

# Set style for better looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ChartTools:
    @staticmethod
    def create_fte_savings_chart(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a chart showing FTE savings analysis"""
        try:
            if analysis_results.get("status") != "success":
                return {"error": "Cannot create chart from failed analysis"}

            results = analysis_results.get("results", {})
            opportunities = results.get("automation_opportunities", [])

            if not opportunities:
                return {"error": "No automation opportunities data available for charting"}

            # Prepare data for chart
            tasks = [opp.get('task_column', f'Task {i}') for i, opp in enumerate(opportunities[:10])]
            savings = [opp.get('annual_time_savings', 0) for opp in opportunities[:10]]

            # Create the chart
            fig, ax = plt.subplots(figsize=(12, 8))
            bars = ax.barh(range(len(tasks)), savings, color='skyblue', edgecolor='navy', alpha=0.7)
            ax.set_yticks(range(len(tasks)))
            ax.set_yticklabels(tasks)
            ax.set_xlabel('Annual Time Savings (hours)')
            ax.set_title('Top 10 Automation Opportunities by Time Savings')
            ax.grid(axis='x', alpha=0.3)

            # Add value labels on bars
            for i, (bar, savings_val) in enumerate(zip(bars, savings)):
                ax.text(bar.get_width() + max(savings) * 0.01, bar.get_y() + bar.get_height()/2,
                       f'{savings_val:,.0f}', va='center', fontweight='bold')

            plt.tight_layout()

            # Convert to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close(fig)

            return {
                "status": "success",
                "chart_type": "fte_savings_bar_chart",
                "title": "Top Automation Opportunities",
                "image_base64": img_base64,
                "image_format": "png"
            }

        except Exception as e:
            logger.error(f"Error creating FTE savings chart: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def create_time_distribution_chart(data: List[Dict[str, Any]], time_column: str) -> Dict[str, Any]:
        """Create a chart showing time distribution"""
        try:
            df = pd.DataFrame(data)
            if time_column not in df.columns:
                return {"error": f"Column '{time_column}' not found in data"}

            # Clean the data
            time_data = pd.to_numeric(df[time_column], errors='coerce').dropna()

            if len(time_data) == 0:
                return {"error": f"No valid numeric data in column '{time_column}'"}

            # Create the chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(time_data, bins=20, alpha=0.7, color='lightcoral', edgecolor='darkred')
            ax.set_xlabel('Time (minutes)')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution of {time_column}')
            ax.grid(axis='y', alpha=0.3)

            # Add statistics
            mean_val = time_data.mean()
            median_val = time_data.median()
            ax.axvline(mean_val, color='blue', linestyle='--', label=f'Mean: {mean_val:.1f}')
            ax.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.1f}')
            ax.legend()

            plt.tight_layout()

            # Convert to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close(fig)

            return {
                "status": "success",
                "chart_type": "time_distribution_histogram",
                "title": f"Distribution of {time_column}",
                "image_base64": img_base64,
                "image_format": "png",
                "statistics": {
                    "mean": round(float(mean_val), 2),
                    "median": round(float(median_val), 2),
                    "std": round(float(time_data.std()), 2),
                    "min": round(float(time_data.min()), 2),
                    "max": round(float(time_data.max()), 2)
                }
            }

        except Exception as e:
            logger.error(f"Error creating time distribution chart: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def create_volume_frequency_scatter(data: List[Dict[str, Any]],
                                      volume_column: str,
                                      frequency_column: str) -> Dict[str, Any]:
        """Create a scatter plot of volume vs frequency"""
        try:
            df = pd.DataFrame(data)
            missing_cols = []
            if volume_column not in df.columns:
                missing_cols.append(volume_column)
            if frequency_column not in df.columns:
                missing_cols.append(frequency_column)

            if missing_cols:
                return {"error": f"Columns not found: {', '.join(missing_cols)}"}

            # Clean the data
            volume_data = pd.to_numeric(df[volume_column], errors='coerce')
            frequency_data = pd.to_numeric(df[frequency_column], errors='coerce')

            # Remove NaN values
            valid_mask = ~(volume_data.isna() | frequency_data.isna())
            volume_clean = volume_data[valid_mask]
            frequency_clean = frequency_data[valid_mask]

            if len(volume_clean) == 0:
                return {"error": "No valid data points for scatter plot"}

            # Create the chart
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(volume_clean, frequency_clean, alpha=0.6, c='purple', s=50)
            ax.set_xlabel(volume_column.replace('_', ' ').title())
            ax.set_ylabel(frequency_column.replace('_', ' ').title())
            ax.set_title(f'{volume_column.replace("_", " ").title()} vs {frequency_column.replace("_", " ").title()}')
            ax.grid(True, alpha=0.3)

            plt.tight_layout()

            # Convert to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close(fig)

            return {
                "status": "success",
                "chart_type": "volume_frequency_scatter",
                "title": f"{volume_column} vs {frequency_column}",
                "image_base64": img_base64,
                "image_format": "png",
                "data_points": len(volume_clean)
            }

        except Exception as e:
            logger.error(f"Error creating volume/frequency scatter chart: {str(e)}")
            return {"error": str(e)}

# Global chart tools instance
chart_tools = ChartTools()