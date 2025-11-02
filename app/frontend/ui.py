import streamlit as st
import requests 

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multiagent AI Chat", layout="wide")
st.title("Multiagent AI Chat Interface")

system_prompt = st.text_area("Define your AI agent's behavior:", height=70, value="Example: You are a helpful AI assistant.")
selected_model = st.selectbox("Choose AI Model:", settings.AUTHORIZED_MODELS)

allow_search = st.checkbox("Enable Web Search", value=False)

user_input = st.text_area("Enter your message:", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask the Agent") and user_input.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_input],
        "allow_search": allow_search
    }

    try:
        logger.info("Sending request to backend")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error("Backend error")
            st.error(str(CustomException("Failed to reach backend", Exception(f"Status code: {response.status_code}"))))

    except Exception as e:
        logger.error("An exception occurred while communicating with backend")
        st.error(str(CustomException("An error occurred while communicating with the backend", e)))

        
