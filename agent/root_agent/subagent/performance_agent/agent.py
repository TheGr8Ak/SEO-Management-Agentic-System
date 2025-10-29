"""
=============================================================================
PERFORMANCE MONITORING AGENT - Google ADK Implementation
=============================================================================
Specializes in tracking rankings, traffic, and metrics for GSBG.IN.
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

def monitor_gsbg_performance(metric_type: str = "all") -> str:
    """
    Monitor performance metrics for GSBG.IN.
    
    Args:
        metric_type: Type of metrics to check ('all', 'rankings', 'traffic', 'speed')
    
    Returns:
        str: Formatted performance monitoring results
    """
    from tools.seo_tools import check_performance
    
    try:
        # ✅ FIXED: Pass metric_type as second argument
        performance_result = check_performance("gsbg.in", metric_type)
        logger.info(f"✅ Performance check completed: {metric_type}")
        return performance_result
        
    except Exception as e:
        logger.error(f"Performance monitoring error: {e}", exc_info=True)
        return f"❌ Monitoring failed: {str(e)}"

# ----------------------
# Agent Creation
# ----------------------

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Performance Analytics Specialist monitoring GSBG.IN exclusively.

Your job:
1. Call monitor_gsbg_performance() immediately (use "all" for comprehensive check)
2. Provide insights on organic traffic trends, keyword rankings, CTR, and user engagement
3. Recommend improvements based on the data

Call the monitoring function immediately."""

# ✅ CORRECT: No invalid parameters
performance_agent = LlmAgent(
    name="performance_agent",
    model="gemini-2.5-flash",
    description="Monitors website performance, rankings, and analytics for GSBG.IN. Handles: search rankings, organic traffic, click-through rates, engagement metrics, Google Search Console, Analytics 4, page speed, Core Web Vitals, SEO ROI.",
    instruction=system_instruction,
    tools=[monitor_gsbg_performance],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Performance Monitoring Agent created successfully")

__all__ = ['performance_agent']










system_instruction = """You are a Performance Analytics Specialist monitoring GSBG.IN exclusively.

Your job:
1. Call monitor_gsbg_performance() immediately (use "all" for comprehensive check)
2. Provide insights on organic traffic trends, keyword rankings, CTR, and user engagement
3. Recommend improvements based on the data

Call the monitoring function immediately."""