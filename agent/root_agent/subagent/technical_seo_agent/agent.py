from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging
from google.adk.agents import LlmAgent
from google.genai import types

env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)

def perform_technical_audit(domain: str = "gsbg.in") -> str:
    """Performs technical SEO audit for gsbg.in"""
    from tools.seo_tools import audit_technical_seo
    
    domain_clean = domain.lower().replace('https://', '').replace('http://', '').replace('www.', '').strip('/')
    
    if domain_clean != "gsbg.in":
        return f"❌ Only works with gsbg.in"
    
    try:
        return audit_technical_seo("https://www.gsbg.in")
    except Exception as e:
        logger.error(f"Audit failed: {str(e)}")
        return f"❌ Audit failed: {str(e)}"

system_instruction = """You are the Technical SEO Audit Specialist for GSBG.IN.

When you receive control:
1. Immediately call perform_technical_audit()
2. Analyze results and provide recommendations
3. Use ✅ ❌ ⚠️ indicators

Call the audit function immediately - no questions."""

# ✅ CORRECT: NO invalid parameters
technical_seo_agent = LlmAgent(
    name="technical_seo_agent",
    model="gemini-2.5-flash",
    description="Performs technical SEO AUDITS for gsbg.in: site audits, technical scans, crawlability, indexing, site speed, Core Web Vitals, mobile testing. This agent performs AUDITS, not reports.",
    instruction=system_instruction,
    tools=[perform_technical_audit],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Technical SEO Agent created")

__all__ = ['technical_seo_agent']
