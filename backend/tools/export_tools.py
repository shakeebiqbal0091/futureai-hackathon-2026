"""
PDF/DOCX export utilities for reports
"""
from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime
import io

logger = logging.getLogger(__name__)

class ExportTools:
    @staticmethod
    def export_to_txt(content: str, title: str = "Report") -> Dict[str, Any]:
        """Export content to text format"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{title.replace(' ', '_')}_{timestamp}.txt"

            # For now, return the content as we're focusing on the MVP
            # In a full implementation, this would save to a file or return binary data
            return {
                "status": "success",
                "format": "txt",
                "filename": filename,
                "content": content,
                "message": f"Report exported as {filename}"
            }
        except Exception as e:
            logger.error(f"Error exporting to TXT: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def export_narrative_summary(narrative_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Export narrative summary to text format"""
        try:
            if narrative_summary.get("status") != "success":
                return {"error": "Cannot export failed narrative summary"}

            content = []
            content.append("=" * 50)
            content.append("WORKFORCE INTELLIGENCE AGENT - NARRATIVE SUMMARY")
            content.append("=" * 50)
            content.append(f"Generated: {narrative_summary.get('generated_at', 'Unknown')}")
            content.append("")
            content.append(narrative_summary.get("narrative", "No narrative available"))
            content.append("")
            content.append("Key Metrics:")
            metrics = narrative_summary.get("key_metrics", {})
            for key, value in metrics.items():
                content.append(f"  {key.replace('_', ' ').title()}: {value}")
            content.append("")
            content.append("Assumptions:")
            for assumption in narrative_summary.get("assumptions", []):
                content.append(f"  • {assumption}")

            full_content = "\n".join(content)

            return ExportTools.export_to_txt(full_content, "Narrative_Summary")

        except Exception as e:
            logger.error(f"Error exporting narrative summary: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def export_executive_report(executive_report: Dict[str, Any]) -> Dict[str, Any]:
        """Export executive report to text format"""
        try:
            if executive_report.get("status") != "success":
                return {"error": "Cannot export failed executive report"}

            content = []
            content.append("=" * 60)
            content.append(f"{executive_report.get('title', 'WORKFORCE INTELLIGENCE REPORT')}")
            content.append("=" * 60)
            content.append(f"Generated: {executive_report.get('generated_at', 'Unknown')}")
            content.append("")

            for section in executive_report.get("sections", []):
                content.append(f"{section.get('title', 'SECTION')}")
                content.append("-" * len(section.get('title', 'SECTION')))
                content.append(section.get("content", "No content available"))
                content.append("")

            full_content = "\n".join(content)

            return ExportTools.export_to_txt(full_content, "Executive_Report")

        except Exception as e:
            logger.error(f"Error exporting executive report: {str(e)}")
            return {"error": str(e)}

# Global export tools instance
export_tools = ExportTools()