import streamlit as st
import requests
import uuid

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
    
    /* FIX: Make the header transparent instead of hidden so the reopen button stays visible */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

API_BASE = "https://ai-research-assistant-xku3.onrender.com"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Using a distinct UUID ensures multi-user safety on Render without ID collisions
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.title("✨ Research Assistant")
    st.markdown("Your personal AI for deep research & PDFs 📄")
    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        # Create a fresh session ID for a new separate environment
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Drag & drop or browse PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        st.success(f"Selected: {uploaded_file.name}")

        if st.button("🚀 Process PDF", use_container_width=True):
            with st.spinner("Uploading & processing PDF..."):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }

                    # FIX: Append the session_id cleanly into the URL parameters
                    target_url = f"{API_BASE}/upload_pdf?session_id={st.session_state.session_id}"
                    
                    res = requests.post(target_url, files=files)

                    if res.status_code == 200:
                        data = res.json()
                        if "error" in data:
                            st.error(f"Backend Error: {data['error']}")
                        else:
                            st.success("PDF uploaded & indexed successfully 🚀")
                    else:
                        st.error(f"Upload failed: {res.text}")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.divider()
    st.caption("Powered by FastAPI + LangChain + Gemini")

st.title("💬 AI Research Assistant")

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything about your PDF or general research...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Thinking... 🤔"):
            try:
                response = requests.post(
                    f"{API_BASE}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "query": prompt
                    }
                )

                data = response.json()
                answer = data.get("answer", "No response")
                route = data.get("route", "unknown")

            except Exception as e:
                answer = f"⚠️ Backend error: {str(e)}"
                route = "error"

        if route == "rag":
            st.success("📄 Answer from your PDF (RAG)")
        elif route == "coding":
            st.info("💻 Coding Mode")
        elif route == "summary":
            st.info("🧾 Summary Mode")
        elif route != "error":
            st.info(f"🧠 Mode: {route}")

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })