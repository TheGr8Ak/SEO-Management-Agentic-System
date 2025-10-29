from google.genai import types
from google.adk.agents import LlmAgent
import logging

# Import from subagent package
from .subagent import (
    technical_seo_agent,
    keyword_agent,
    content_agent,
    performance_agent,
    reporting_agent
)

logger = logging.getLogger(__name__)

# ✅ CRITICAL: Explicit audit → technical_seo_agent mapping
system_instruction = """You coordinate SEO tasks for GSBG.IN by routing to specialist agents.

ROUTING RULES (Match FIRST rule that applies):

1. "audit" OR "technical audit" OR "technical SEO" → transfer_to_agent(agent_name="technical_seo_agent")
2. "keyword" OR "keyword research" OR "research" → transfer_to_agent(agent_name="keyword_agent")
3. "content" OR "analyze page" OR "page analysis" → transfer_to_agent(agent_name="content_agent")
4. "performance" OR "check" OR "monitor" OR "traffic" → transfer_to_agent(agent_name="performance_agent")
5. "report" OR "comprehensive" OR "summary" → transfer_to_agent(agent_name="reporting_agent")

CRITICAL:
- "audit" ALWAYS = technical_seo_agent (NOT reporting_agent)
- Do NOT explain, do NOT acknowledge
- ONLY call transfer_to_agent() immediately"""

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash-exp",  # Keep your working model
    description="SEO Coordinator for GSBG.IN that routes requests to specialist agents",
    instruction=system_instruction,
    sub_agents=[
        technical_seo_agent,
        keyword_agent,
        content_agent,
        performance_agent,
        reporting_agent
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,  # ✅ Zero for deterministic routing
        top_p=0.9,
        max_output_tokens=256,
    )
)

logger.info("✅ Root SEO Agent initialized with 5 specialist sub-agents")
