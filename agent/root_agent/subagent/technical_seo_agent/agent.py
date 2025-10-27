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
    """Performs comprehensive technical SEO audit for gsbg.in"""
    from tools.seo_tools import audit_technical_seo
    
    domain_clean = domain.lower().replace('https://', '').replace('http://', '').replace('www.', '').strip('/')
    
    if domain_clean != "gsbg.in":
        return f"❌ This tool only works with gsbg.in domain"
    
    try:
        return audit_technical_seo("https://www.gsbg.in")
    except Exception as e:
        logger.error(f"Audit failed: {str(e)}")
        return f"❌ Technical audit failed: {str(e)}"

system_instruction = """You are the Technical SEO Specialist for GSBG.IN exclusively.

**Your Mission:**
1. Immediately call perform_technical_audit() to scan gsbg.in
2. Analyze the complete audit results thoroughly
3. Provide actionable, prioritized recommendations
4. Use ✅ ❌ ⚠️ for visual clarity

**Key Rules:**
- ONLY work with gsbg.in domain
- Call the audit function immediately - don't ask for permission
- Provide complete analysis in ONE comprehensive response
- Focus on actionable fixes, not theory

When you receive control, immediately begin by calling perform_technical_audit()."""

# ✅ CORRECT: Detailed description for LLM-driven routing
technical_seo_agent = LlmAgent(
    name="technical_seo_agent",
    model="gemini-2.0-flash-exp",
    description="Handles comprehensive technical SEO audits for gsbg.in including site speed, crawlability, indexing issues, Core Web Vitals, mobile-friendliness, structured data, sitemap, robots.txt, and HTTPS security checks.",  # ✅ CRITICAL for routing
    instruction=system_instruction,
    tools=[perform_technical_audit],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )
)

logger.info("✅ Technical SEO Agent initialized")
