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

def monitor_gsbg_performance(metric_type: Optional[str] = "all") -> str:
    """
    Monitor performance metrics for GSBG.IN.
    
    Args:
        metric_type: Type of metrics to check ('all', 'rankings', 'traffic', 'speed')
    
    Returns:
        str: Formatted performance monitoring results
    """
    from tools.seo_tools import check_performance
    
    try:
        # Check performance with GSBG context
        performance_result = check_performance("gsbg.in", metric_type)
        
        # Store in Streamlit session state (optional)
        try:
            import streamlit as st
            if hasattr(st, 'session_state'):
                st.session_state['last_performance_check'] = {
                    "metric_type": metric_type,
                    "results": performance_result
                }
                st.session_state['performance_check_complete'] = True
                logger.info("✅ Stored performance check in Streamlit session")
        except ImportError:
            pass
        
        logger.info(f"✅ Performance check completed: {metric_type}")
        return performance_result
        
    except Exception as e:
        logger.error(f"Performance monitoring error: {e}", exc_info=True)
        return f"❌ Monitoring failed: {str(e)}"


def check_monitoring_status() -> str:
    """Check performance monitoring status."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state'):
            has_check = st.session_state.get("performance_check_complete", False)
            last_check = st.session_state.get("last_performance_check")
            if has_check and last_check:
                metric_type = last_check.get("metric_type", "N/A")
                return f"✅ Performance monitoring completed for: {metric_type}"
            else:
                return "⚠️ No performance monitoring performed yet."
    except ImportError:
        return "⚠️ Session state not available"
    except Exception as e:
        return f"❌ Status check failed: {str(e)}"


# ----------------------
# Agent Creation
# ----------------------

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Performance Analytics Specialist monitoring GSBG.IN exclusively.

Your job:
1. Call monitor_gsbg_performance() with metric type immediately
2. Provide insights on organic traffic trends, keyword rankings, CTR, and user engagement
3. Explain Google Search Console and Analytics 4 setup requirements
4. Recommend page speed improvements and track SEO ROI

Provide your complete performance analysis in ONE comprehensive response."""

# ✅ CORRECT: Properly closed with detailed description
performance_agent = LlmAgent(
    name="performance_agent",
    model="gemini-2.5-flash",
    description="Monitors website performance, rankings, and analytics for GSBG.IN. Handles requests about: search rankings tracking, organic traffic analysis, click-through rates, user engagement metrics, Google Search Console data, Google Analytics 4 insights, page speed performance, Core Web Vitals monitoring, and SEO ROI measurement.",
    instruction=system_instruction,
    tools=[
        monitor_gsbg_performance,
        check_monitoring_status
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )  # ✅ CLOSES GenerateContentConfig
)  # ✅ CLOSES LlmAgent

logger.info("✅ Performance Monitoring Agent created successfully")

__all__ = ['performance_agent']
