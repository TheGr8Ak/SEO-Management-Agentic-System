"""
=============================================================================
KEYWORD RESEARCH AGENT - Google ADK Implementation
=============================================================================
Specializes in keyword research and strategy for GSBG.IN.
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

def research_keywords_for_gsbg(topic: str, focus_area: Optional[str] = None) -> str:
    """
    Research keywords for GSBG.IN based on topic and focus area.
    
    Args:
        topic: Main topic for keyword research
        focus_area: Specific area to focus on (e.g., "Salesforce", "real estate")
    
    Returns:
        str: Formatted keyword research results
    """
    from tools.seo_tools import research_keywords
    
    try:
        # Perform keyword research with GSBG context
        context_topic = f"{topic} for GSBG.IN" if "gsbg" not in topic.lower() else topic
        if focus_area:
            context_topic = f"{context_topic} - {focus_area}"
        
        keyword_results = research_keywords(context_topic)
        
        # Store in Streamlit session state (optional)
        try:
            import streamlit as st
            if hasattr(st, 'session_state'):
                st.session_state['last_keyword_research'] = {
                    "topic": topic,
                    "focus_area": focus_area,
                    "results": keyword_results
                }
                st.session_state['keyword_research_complete'] = True
                logger.info("✅ Stored keyword research in Streamlit session")
        except ImportError:
            pass
        
        logger.info(f"✅ Keyword research completed for: {topic}")
        return keyword_results
        
    except Exception as e:
        logger.error(f"Keyword research error: {e}", exc_info=True)
        return f"❌ Research failed: {str(e)}"


def check_keyword_status() -> str:
    """Check keyword research status in session."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state'):
            has_research = st.session_state.get("keyword_research_complete", False)
            last_research = st.session_state.get("last_keyword_research")
            if has_research and last_research:
                topic = last_research.get("topic", "N/A")
                return f"✅ Keyword research completed for topic: {topic}"
            else:
                return "⚠️ No keyword research performed yet."
    except ImportError:
        return "⚠️ Session state not available"
    except Exception as e:
        return f"❌ Status check failed: {str(e)}"


# ----------------------
# Agent Creation
# ----------------------

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Keyword Research Specialist for GSBG.IN, a Salesforce consulting company serving the real estate sector.

Your job:
1. Call research_keywords_for_gsbg() with the topic immediately
2. Provide categorized keyword lists by search intent and difficulty
3. Suggest content creation roadmap with priorities
4. Focus on Salesforce, real estate tech, and B2B sales keywords

Provide your complete research analysis in ONE comprehensive response."""

# ✅ CORRECT: Properly closed with detailed description
keyword_agent = LlmAgent(
    name="keyword_agent",
    model="gemini-2.5-flash",
    description="Conducts keyword research and strategy for GSBG.IN. Handles requests about: keyword opportunities, search terms analysis, competitor keywords, keyword rankings, search volume data, keyword difficulty assessment, and SEO keyword strategy for Salesforce consulting services in the real estate sector.",
    instruction=system_instruction,
    tools=[
        research_keywords_for_gsbg,
        check_keyword_status
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.8,  # Higher temp for creative keyword ideas
        top_p=0.95,
        max_output_tokens=8192,
    )  # ✅ CLOSES GenerateContentConfig
)  # ✅ CLOSES LlmAgent

logger.info("✅ Keyword Research Agent created successfully")

__all__ = ['keyword_agent']
