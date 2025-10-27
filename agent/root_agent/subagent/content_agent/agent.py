"""
=============================================================================
CONTENT OPTIMIZATION AGENT - Google ADK Implementation
=============================================================================
Specializes in content analysis and on-page SEO for GSBG.IN.
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

def analyze_page_content(page_url: str) -> str:
    """
    Analyze content and on-page SEO for a GSBG.IN page.
    
    Args:
        page_url: Full URL of the page to analyze
    
    Returns:
        str: Formatted content analysis results
    """
    from tools.seo_tools import analyze_content
    
    # Validate GSBG.IN domain
    if "gsbg.in" not in page_url.lower():
        return f"❌ This agent only analyzes GSBG.IN pages. URL provided: {page_url}"
    
    try:
        # Perform content analysis
        analysis_result = analyze_content(page_url)
        
        # Store in Streamlit session state (optional)
        try:
            import streamlit as st
            if hasattr(st, 'session_state'):
                st.session_state['last_content_analysis'] = {
                    "url": page_url,
                    "results": analysis_result
                }
                st.session_state['content_analysis_complete'] = True
                logger.info("✅ Stored content analysis in Streamlit session")
        except ImportError:
            pass
        
        logger.info(f"✅ Content analysis completed for: {page_url}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Content analysis error: {e}", exc_info=True)
        return f"❌ Analysis failed: {str(e)}"


def check_content_status() -> str:
    """Check content analysis status."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state'):
            has_analysis = st.session_state.get("content_analysis_complete", False)
            last_analysis = st.session_state.get("last_content_analysis")
            if has_analysis and last_analysis:
                url = last_analysis.get("url", "N/A")
                return f"✅ Content analysis completed for: {url}"
            else:
                return "⚠️ No content analysis performed yet."
    except ImportError:
        return "⚠️ Session state not available"
    except Exception as e:
        return f"❌ Status check failed: {str(e)}"


# ----------------------
# Agent Creation
# ----------------------

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Content Optimization Specialist for GSBG.IN pages.

Your job:
1. Call analyze_page_content() with the URL immediately
2. Evaluate title tags, meta descriptions, H1-H6 heading structure
3. Assess content depth, readability scores, and E-E-A-T signals
4. Provide prioritized optimization recommendations with implementation steps

Provide your complete content analysis in ONE comprehensive response."""

# ✅ CORRECT: Properly closed with detailed description
content_agent = LlmAgent(
    name="content_agent",
    model="gemini-2.5-flash",
    description="Analyzes page content and provides on-page SEO optimization for GSBG.IN. Handles requests about: content quality analysis, meta tags optimization, title and description improvements, heading structure, readability assessment, keyword usage, internal linking, content depth evaluation, and E-E-A-T optimization.",
    instruction=system_instruction,
    tools=[
        analyze_page_content,
        check_content_status
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )  # ✅ CLOSES GenerateContentConfig
)  # ✅ CLOSES LlmAgent

logger.info("✅ Content Optimization Agent created successfully")

__all__ = ['content_agent']
