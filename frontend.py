import streamlit as st
import requests


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="✨",
    layout="centered", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

API_URL = "https://your-render-app.onrender.com/chat"


with st.sidebar:
    st.title("✨ Research Assistant")
    st.markdown("Your personal AI for deep research and insights.")
    st.divider()
    
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.caption("Powered by Local API")


st.title("How can I help with your research today?")

if "messages" not in st.session_state:
    st.session_state.messages = []


if len(st.session_state.messages) == 0:
    st.info("👋 Hello! Ask me anything to get started.")


for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your research assistant anything...")

if prompt:

    
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    
    with st.chat_message("assistant", avatar="✨"):
        
        with st.spinner("Researching..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "session_id": "user1",
                        "query": prompt
                    }
                )
                answer = response.json()["answer"]
            except Exception as e:
                
                answer = f"⚠️ Connection error: Make sure your backend at {API_URL} is running."
                
        
        st.markdown(answer)

  
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
