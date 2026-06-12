"""
Report Writer Agent - Converts analysis into narrative summaries and executive decks
"""
from typing import List, Dict, Any, Optional
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportWriterAgent:
    def __init__(self):
        pass

    async def generate_narrative_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate natural language insights from FTE analysis results
        """
        try:
            logger.info("Generating narrative summary")

            if analysis_results.get("status") != "success":
                return {"error": "Cannot generate summary from failed analysis"}

            results = analysis_results.get("results", {})
            assumptions = analysis_results.get("assumptions", [])

            # Extract key metrics
            daily_hours = results.get("daily_time_saved_hours", 0)
            annual_hours = results.get("annual_time_saved_hours", 0)
            fte_equivalent = results.get("fte_equivalent", 0)
            cost_savings = results.get("annual_cost_savings", 0)
            opportunities = results.get("automation_opportunities", [])

            # Generate narrative
            narrative_parts = []

            # Executive summary
            if fte_equivalent > 0:
                narrative_parts.append(
                    f"Analysis reveals potential to free up {fte_equivalent:.1f} full-time equivalent (FTE) "
                    f"through automation, representing {annual_hours:,.0f} hours annually "
                    f"or {daily_hours:.1f} hours per day."
                )
            else:
                narrative_parts.append(
                    f"Analysis shows potential time savings of {annual_hours:,.0f} hours annually "
                    f"({daily_hours:.1f} hours per day) through process optimization."
                )

            # Financial impact
            if cost_savings > 0:
                narrative_parts.append(
                    f"At an estimated fully loaded cost of $50/hour, this represents "
                    f"potential annual cost savings of ${cost_savings:,.0f}."
                )

            # Top opportunities
            if opportunities:
                top_opportunity = opportunities[0]
                task_name = top_opportunity.get('task_column', 'Unknown Task')
                savings = top_opportunity.get('annual_time_savings', 0)
                narrative_parts.append(
                    f"The highest-impact automation opportunity is '{task_name}' "
                    f"with {savings:,.0f} hours of potential annual savings."
                )

            # Call to action
            narrative_parts.append(
                "Recommended next steps include detailed process analysis for top automation "
                "candidates and development of pilot automation projects."
            )

            full_narrative = " ".join(narrative_parts)

            return {
                "status": "success",
                "report_type": "narrative_summary",
                "generated_at": datetime.now().isoformat(),
                "narrative": full_narrative,
                "key_metrics": {
                    "daily_time_saved_hours": daily_hours,
                    "annual_time_saved_hours": annual_hours,
                    "fte_equivalent": fte_equivalent,
                    "annual_cost_savings": cost_savings
                },
                "assumptions": assumptions
            }

        except Exception as e:
            logger.error(f"Error generating narrative summary: {str(e)}")
            return {"error": str(e)}

    async def generate_executive_report(self, analysis_results: Dict[str, Any],
                                      narrative_summary: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate executive-ready report structure
        """
        try:
            logger.info("Generating executive report")

            if narrative_summary is None:
                narrative_summary = await self.generate_narrative_summary(analysis_results)

            results = analysis_results.get("results", {}) if analysis_results.get("status") == "success" else {}

            executive_report = {
                "status": "success",
                "report_type": "executive_report",
                "generated_at": datetime.now().isoformat(),
                "title": "WorkForce Intelligence Analysis Report",
                "sections": [
                    {
                        "title": "Executive Summary",
                        "content": narrative_summary.get("narrative", "Analysis completed") if narrative_summary.get("status") == "success" else "Analysis pending"
                    },
                    {
                        "title": "Key Findings",
                        "content": self._format_key_findings(results)
                    },
                    {
                        "title": "Automation Opportunities",
                        "content": self._format_automation_opportunities(results.get("automation_opportunities", []))
                    },
                    {
                        "title": "Methodology & Assumptions",
                        "content": self._format_methodology(analysis_results.get("assumptions", []))
                    },
                    {
                        "title": "Recommendations",
                        "content": "1. Prioritize top 3 automation opportunities for pilot projects\n"
                                 "2. Conduct detailed time-and-motion studies for selected processes\n"
                                 "3. Develop ROI business cases for automation investments\n"
                                 "4. Implement change management plan for affected staff"
                    }
                ]
            }

            return executive_report

        except Exception as e:
            logger.error(f"Error generating executive report: {str(e)}")
            return {"error": str(e)}

    def _format_key_findings(self, results: Dict[str, Any]) -> str:
        """Format key findings section"""
        if not results:
            return "No analysis results available"

        findings = []
        findings.append(f"• Daily time savings: {results.get('daily_time_saved_hours', 0):.1f} hours")
        findings.append(f"• Annual time savings: {results.get('annual_time_saved_hours', 0):,.0f} hours")
        findings.append(f"• FTE equivalent: {results.get('fte_equivalent', 0):.1f} FTE")
        findings.append(f"• Estimated annual cost savings: ${results.get('annual_cost_savings', 0):,.0f}")

        return "\n".join(findings)

    def _format_automation_opportunities(self, opportunities: List[Dict[str, Any]]) -> str:
        """Format automation opportunities section"""
        if not opportunities:
            return "No automation opportunities identified"

        content = "Top automation opportunities ranked by potential time savings:\n\n"
        for i, opp in enumerate(opportunities[:5], 1):  # Top 5
            task = opp.get('task_column', 'Unknown Task')
            savings = opp.get('annual_time_savings', 0)
            content += f"{i}. {task}: {savings:,.0f} hours annually\n"

        return content

    def _format_methodology(self, assumptions: List[str]) -> str:
        """Format methodology and assumptions section"""
        if not assumptions:
            return "Standard FTE calculation methodology applied"

        content = "Calculation Methodology:\n"
        content += "• Time savings = (time_per_task_min × volume_per_day × frequency) / 60\n"
        content += "• FTE equivalent = Annual time savings / (FTE hours/day × Working days/year)\n\n"
        content += "Assumptions:\n"
        for assumption in assumptions:
            content += f"• {assumption}\n"

        return content

# Global report writer agent instance
report_writer_agent = ReportWriterAgent()