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

# ✅ CORRECT: Explicit delegation instruction based on official docs
system_instruction = """You coordinate SEO tasks for GSBG.IN by immediately routing to specialist agents.

Match keywords to actions:
- "audit", "technical" → transfer_to_agent(agent_name="technical_seo_agent")
- "keyword", "research" → transfer_to_agent(agent_name="keyword_agent")
- "content", "analyze page" → transfer_to_agent(agent_name="content_agent")
- "performance", "check", "monitor" → transfer_to_agent(agent_name="performance_agent")
- "report", "comprehensive" → transfer_to_agent(agent_name="reporting_agent")

Do NOT explain. Do NOT acknowledge. ONLY call transfer_to_agent() immediately."""

# ✅ CORRECT: Root agent configuration per official docs
root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash-exp",
    description="SEO Management Coordinator for GSBG.IN that routes requests to specialist agents",
    instruction=system_instruction,
    sub_agents=[
        technical_seo_agent,
        keyword_agent,
        content_agent,
        performance_agent,
        reporting_agent
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # ✅ Very low for deterministic routing
        top_p=0.9,
        max_output_tokens=512,  # ✅ Root only routes, doesn't need long responses
    )
)

logger.info("✅ Root SEO Agent initialized with 5 specialist sub-agents")
