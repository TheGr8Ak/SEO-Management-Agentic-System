from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

def analyze_page_content(page_url: str) -> str:
    """Analyze content for a GSBG.IN page"""
    from tools.seo_tools import analyze_content
    
    if "gsbg.in" not in page_url.lower():
        return f"❌ Only analyzes GSBG.IN pages"
    
    try:
        return analyze_content(page_url)
    except Exception as e:
        logger.error(f"Content analysis error: {e}")
        return f"❌ Analysis failed: {str(e)}"

from google.adk.agents import LlmAgent
from google.genai import types

system_instruction = """You are a Content Optimization Specialist for GSBG.IN.

When you receive control:
1. Call analyze_page_content() immediately
2. Evaluate meta tags, headings, content quality
3. Provide optimization recommendations

Call the analysis function immediately."""

# ✅ CORRECT: NO invalid parameters
content_agent = LlmAgent(
    name="content_agent",
    model="gemini-2.5-flash",
    description="Analyzes page content for GSBG.IN: content quality, meta tags, title/description optimization, heading structure, readability, keyword usage, internal linking, E-E-A-T.",
    instruction=system_instruction,
    tools=[analyze_page_content],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Content Optimization Agent created")

__all__ = ['content_agent']
