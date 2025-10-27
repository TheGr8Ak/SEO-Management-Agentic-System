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

async def create_session_async(session_service, app_name, user_id):
    return await session_service.create_session(app_name=app_name, user_id=user_id)

def initialize_session_state():
    if 'session_service' not in st.session_state:
        st.session_state.session_service = InMemorySessionService()
        logger.info("✅ Session service created")
    if 'session_id' not in st.session_state:
        st.session_state.user_id = f"user_{str(uuid.uuid4())[:8]}"
        session = asyncio.run(create_session_async(st.session_state.session_service, "seo_agent_app", st.session_state.user_id))
        st.session_state.session_id = session.id
        logger.info(f"✅ Session created: {st.session_state.session_id}")
    if 'runner' not in st.session_state:
        try:
            st.session_state.runner = Runner(agent=root_agent, app_name="seo_agent_app", session_service=st.session_state.session_service)
            logger.info("✅ Runner initialized")
        except Exception as e:
            st.error(f"Failed to initialize: {e}")
            st.stop()
    if 'messages' not in st.session_state:
        st.session_state.messages = [{'role': 'assistant', 'content': """👋 **Welcome to GSBG.IN SEO Management Agent!**

I'm your AI-powered SEO consultant for **GSBG.IN exclusively**. Please select a service:

**1.** Audit gsbg.in                                   
**2.** Research keywords for Salesforce consulting                                       
**3.** Analyze content at https://www.gsbg.in/services                                     
**4.** Check GSBG.IN performance                                     
**5.** Generate comprehensive SEO report                                     
What would you like to work on today?
                                      
"""}]

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🔍 SEO Agent System")
        st.markdown("**For GSBG.IN Exclusively**")
        st.markdown("---")
        st.markdown("#### System Status")
        st.success("🟢 All agents ready")
        api_key_check = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        st.text(f"API Key: {'✅ Loaded' if api_key_check else '❌ Missing'}")
        st.markdown("#### Target Domain")
        st.info("🌐 www.gsbg.in")
        st.markdown("---")
        st.markdown("#### Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Audit", use_container_width=True):
                st.session_state.quick_action = "Audit gsbg.in"
                st.rerun()
        with col2:
            if st.button("📊 Report", use_container_width=True):
                st.session_state.quick_action = "Generate comprehensive report for gsbg.in"
                st.rerun()
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🔑 Keywords", use_container_width=True):
                st.session_state.quick_action = "Research keywords for Salesforce consulting"
                st.rerun()
        with col4:
            if st.button("📈 Monitor", use_container_width=True):
                st.session_state.quick_action = "Check GSBG.IN performance"
                st.rerun()
        st.markdown("---")
        st.markdown("#### Session Info")
        st.text(f"Messages: {len(st.session_state.get('messages', []))}")
        st.text(f"Session: {st.session_state.session_id[:8]}...")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            keys_to_delete = ['session_id', 'user_id', 'messages']
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            initialize_session_state()
            st.rerun()

def process_user_message(user_input: str):
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        with st.spinner("🤔 Analyzing..."):
            try:
                runner = st.session_state.runner
                response_text = ""
                user_message = types.Content(parts=[types.Part(text=user_input)])
                for event in runner.run(user_id=st.session_state.user_id, session_id=st.session_state.session_id, new_message=user_message):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_text += part.text
                                placeholder.markdown(response_text + "▌")
                if response_text:
                    placeholder.markdown(response_text)
                    st.session_state.messages.append({'role': 'assistant', 'content': response_text})
                else:
                    msg = "⚠️ No response received. Check logs for details."
                    placeholder.markdown(msg)
                    st.session_state.messages.append({'role': 'assistant', 'content': msg})
            except Exception as e:
                logger.error(f"❌ Error: {e}", exc_info=True)
                error_msg = f"""❌ **Error**\n\n``````\n\n**Try:** Click "Clear Chat" to reset"""
                st.error(error_msg)
                st.session_state.messages.append({'role': 'assistant', 'content': error_msg})

def main():
    initialize_session_state()
    st.title("🔍 SEO Management Agent for GSBG.IN")
    render_sidebar()
    for msg in st.session_state.messages:
        with st.chat_message(msg['role'], avatar="👤" if msg['role'] == 'user' else "🤖"):
            st.markdown(msg['content'])
    if 'quick_action' in st.session_state:
        action = st.session_state.quick_action
        del st.session_state.quick_action
        process_user_message(action)
    if prompt := st.chat_input("Ask me anything about GSBG.IN SEO..."):
        process_user_message(prompt)

if __name__ == "__main__":
    main()
