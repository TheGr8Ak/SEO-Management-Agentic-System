from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

def research_keywords_for_gsbg(topic: str, focus_area: Optional[str] = None) -> str:
    """Research keywords for GSBG.IN"""
    from tools.seo_tools import research_keywords
    
    try:
        context_topic = f"{topic} for GSBG.IN" if "gsbg" not in topic.lower() else topic
        if focus_area:
            context_topic = f"{context_topic} - {focus_area}"
        
        return research_keywords(context_topic)
        
    except Exception as e:
        logger.error(f"Keyword research error: {e}")
        return f"❌ Research failed: {str(e)}"

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Keyword Research Specialist for GSBG.IN.

When you receive control:
1. Call research_keywords_for_gsbg() immediately
2. Provide categorized keyword lists
3. Focus on Salesforce consulting keywords

Call the research function immediately."""

# ✅ CORRECT: NO invalid parameters
keyword_agent = LlmAgent(
    name="keyword_agent",
    model="gemini-2.5-flash",
    description="Conducts keyword research for GSBG.IN: keyword opportunities, search terms, competitor keywords, rankings, search volume, keyword difficulty, SEO strategy for Salesforce consulting.",
    instruction=system_instruction,
    tools=[research_keywords_for_gsbg],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.8,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Keyword Research Agent created")

__all__ = ['keyword_agent']
