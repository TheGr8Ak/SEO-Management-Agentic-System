"""
=============================================================================
REPORTING AGENT - Google ADK Implementation
=============================================================================
Specializes in generating comprehensive SEO reports for GSBG.IN.
"""
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load .env
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

# ----------------------
# Tool Functions
# ----------------------

def generate_gsbg_report(report_type: str = "comprehensive") -> str:
    """
    Generate SEO report for GSBG.IN.
    
    Args:
        report_type: Type of report ('comprehensive', 'executive', 'technical', 'progress')
    
    Returns:
        str: Formatted report with recommendations
    """
    from tools.seo_tools import generate_seo_report
    
    try:
        # Gather data from Streamlit session state
        technical_audit = None
        keyword_research = None
        content_analysis = None
        performance_check = None
        
        try:
            import streamlit as st
            if hasattr(st, 'session_state'):
                technical_audit = st.session_state.get("last_technical_audit")
                keyword_research = st.session_state.get("last_keyword_research")
                content_analysis = st.session_state.get("last_content_analysis")
                performance_check = st.session_state.get("last_performance_check")
        except ImportError:
            pass
        
        # Generate report
        report_result = generate_seo_report(
            domain="gsbg.in",
            report_type=report_type,
            technical_data=technical_audit,
            keyword_data=keyword_research,
            content_data=content_analysis,
            performance_data=performance_check
        )
        
        # Store report in session state
        try:
            import streamlit as st
            if hasattr(st, 'session_state'):
                st.session_state['last_report'] = {
                    "type": report_type,
                    "content": report_result
                }
                st.session_state['report_generated'] = True
                logger.info("✅ Stored report in Streamlit session")
        except ImportError:
            pass
        
        logger.info(f"✅ {report_type.capitalize()} report generated for GSBG.IN")
        return report_result
        
    except Exception as e:
        logger.error(f"Report generation error: {e}", exc_info=True)
        return f"❌ Report generation failed: {str(e)}"


def check_report_status() -> str:
    """Check report generation status."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state'):
            has_report = st.session_state.get("report_generated", False)
            last_report = st.session_state.get("last_report")
            if has_report and last_report:
                report_type = last_report.get("type", "N/A")
                return f"✅ Report generated: {report_type}"
            else:
                return "⚠️ No report generated yet."
    except ImportError:
        return "⚠️ Session state not available"
    except Exception as e:
        return f"❌ Status check failed: {str(e)}"


# ----------------------
# Agent Creation
# ----------------------

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are an SEO Reporting Specialist creating reports exclusively for GSBG.IN.

Your job:
1. Call generate_gsbg_report() with report type immediately
2. Provide executive summary highlighting key findings and trends
3. Create prioritized action plan with realistic timelines
4. Focus on Salesforce consulting industry and real estate sector context

Provide your complete comprehensive report in ONE response."""

# ✅ CORRECT: Properly closed with detailed description
reporting_agent = LlmAgent(
    name="reporting_agent",
    model="gemini-2.5-flash",
    description="Generates comprehensive SEO reports and action plans for GSBG.IN. Handles requests about: comprehensive SEO reports, executive summaries, progress tracking, SEO audit summaries, performance reports, actionable recommendations, prioritized improvement plans, and complete SEO status overviews.",
    instruction=system_instruction,
    tools=[
        generate_gsbg_report,
        check_report_status
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )  # ✅ CLOSES GenerateContentConfig
)  # ✅ CLOSES LlmAgent

logger.info("✅ Reporting Agent created successfully")

__all__ = ['reporting_agent']
