import streamlit as st
import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import uuid

st.set_page_config(page_title="SEO Management Agent", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ API KEY not found in .env file!")
    st.info("Add to .env: GOOGLE_API_KEY=your_key or GEMINI_API_KEY=your_key")
    st.stop()
else:
    os.environ["GOOGLE_API_KEY"] = api_key

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.root_agent.agent import root_agent

# ✅ CORRECT: Async helper to create session
async def create_session_async(session_service, app_name, user_id):
    """Create a new session with proper await"""
    return await session_service.create_session(app_name=app_name, user_id=user_id)

# ✅ CORRECT: Async function to run agent
async def run_agent_async(runner, user_id, session_id, prompt):
    """Run agent and collect all response events"""
    try:
        result_generator = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text=prompt)]
            )
        )
        
        # Collect all events
        response_parts = []
        async for event in result_generator:
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_parts.append(part.text)
        
        return "\n".join(response_parts) if response_parts else "No response generated"
        
    except Exception as e:
        logger.error(f"Agent execution error: {e}", exc_info=True)
        raise

def initialize_session_state():
    """Initialize all session state variables"""
    if "app_name" not in st.session_state:
        st.session_state.app_name = "seo_agent_app"
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
    
    if "session_service" not in st.session_state:
        st.session_state.session_service = InMemorySessionService()
        logger.info("✅ Session service initialized")
    
    if "session" not in st.session_state:
        # ✅ CRITICAL: Properly await the async create_session
        session = asyncio.run(
            create_session_async(
                st.session_state.session_service,
                st.session_state.app_name,
                st.session_state.user_id
            )
        )
        st.session_state.session = session
        logger.info(f"✅ Session created: {session.id}")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("✅ Message history initialized")
    
    if "runner" not in st.session_state:
        st.session_state.runner = Runner(
            agent=root_agent,
            app_name=st.session_state.app_name,
            session_service=st.session_state.session_service
        )
        logger.info("✅ Runner initialized with root agent")

def main():
    initialize_session_state()
    
    st.title("🔍 SEO Management Agent")
    st.markdown("**Powered by Google ADK & Gemini 2.5 Flash**")
    st.divider()
    
    # Welcome message
    with st.chat_message("assistant"):
        st.markdown("""
👋 **Welcome to GSBG.IN SEO Management Agent!**

I'm your AI-powered SEO consultant for GSBG.IN exclusively. Please select a service:

1. **Audit gsbg.in**
2. **Research keywords** for Salesforce consulting
3. **Analyze content** at https://www.gsbg.in/services
4. **Check GSBG.IN performance**
5. **Generate comprehensive SEO report**

What would you like to work on today?
        """)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your SEO request..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with agent
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                try:
                    # ✅ CORRECT: Run agent with existing session
                    response_text = asyncio.run(
                        run_agent_async(
                            st.session_state.runner,
                            st.session_state.user_id,
                            st.session_state.session.id,
                            prompt
                        )
                    )
                    
                    # Display response
                    st.markdown(response_text)
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
                    
                    logger.info("✅ Request completed")
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Request failed: {e}", exc_info=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Session Info")
        st.markdown(f"**Session ID:** `{st.session_state.session.id[:12]}...`")
        st.markdown(f"**User ID:** `{st.session_state.user_id}`")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        
        st.divider()
        
        if st.button("🔄 Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔴 Reset Session", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
