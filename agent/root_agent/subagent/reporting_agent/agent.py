from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

# ✅ CRITICAL: Function signature must match what's in tools/seo_tools.py
def generate_gsbg_report() -> str:
    """Generate comprehensive SEO report for GSBG.IN"""
    from tools.seo_tools import generate_seo_report
    
    try:
        # Call the actual tool function - check its signature!
        return generate_seo_report("gsbg.in")
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        return f"❌ Report generation failed: {str(e)}"

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are an SEO Reporting Specialist for GSBG.IN.

When you receive control:
1. Call generate_gsbg_report() immediately
2. Provide executive summary
3. Create prioritized action plan

Call the report function immediately."""

# ✅ CORRECT: NO invalid parameters
reporting_agent = LlmAgent(
    name="reporting_agent",
    model="gemini-2.5-flash",
    description="Generates comprehensive SEO REPORTS for GSBG.IN: full reports, executive summaries, progress tracking, actionable recommendations, prioritized plans. This agent generates REPORTS, not audits.",
    instruction=system_instruction,
    tools=[generate_gsbg_report],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Reporting Agent created")

__all__ = ['reporting_agent']
