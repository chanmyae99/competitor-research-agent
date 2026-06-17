import time
import uuid
import streamlit as st
from dotenv import load_dotenv
from agent import CompetitorResearchAgent

load_dotenv()

st.set_page_config(
    page_title="Competitor Research Agent",
    page_icon="🔎",
    layout="wide"
)

st.markdown(
    """
    <style>
    .sticky-header {
        position: fixed;
        top: 3.5rem;
        left: 26rem;
        right: 0;
        background-color: #0E1117;
        z-index: 999;
        padding: 1rem 3rem;
        border-bottom: 1px solid #262730;
    }

    .sticky-header h1 {
        margin: 0;
        color: white;
        font-size: 2rem;
    }

    .sticky-header p {
        margin: 0.3rem 0 0 0;
        color: #A0A0A0;
        font-size: 1rem;
    }

    .main .block-container {
        padding-top: 10rem;
    }
    </style>

    <div class="sticky-header">
        <h1>🔎 Competitor Research Agent</h1>
        <p>Google Search + OpenAI competitor analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize agent
if "agent" not in st.session_state:
    st.session_state.agent = CompetitorResearchAgent()

# Initialize chats
if "chats" not in st.session_state:
    first_chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_chat_id: [
            {
                "role": "assistant",
                "content": "Hi! Ask me to research or compare competitors."
            }
        ]
    }
    st.session_state.current_chat_id = first_chat_id

# Safety check
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]


def get_current_messages():
    return st.session_state.chats[st.session_state.current_chat_id]


def stream_text(text):
    placeholder = st.empty()
    full_text = ""

    for word in text.split():
        full_text += word + " "
        placeholder.markdown(full_text)
        time.sleep(0.02)


with st.sidebar:
    st.header("Chats")

    if st.button("➕ New Chat"):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = [
            {
                "role": "assistant",
                "content": "New chat started. What company do you want to research?"
            }
        ]
        st.session_state.current_chat_id = new_chat_id
        st.rerun()

    for index, chat_id in enumerate(list(st.session_state.chats.keys()), start=1):
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(f"Chat {index}", key=f"select_{chat_id}"):
                st.session_state.current_chat_id = chat_id
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{chat_id}"):
                del st.session_state.chats[chat_id]

                if not st.session_state.chats:
                    new_chat_id = str(uuid.uuid4())
                    st.session_state.chats[new_chat_id] = [
                        {
                            "role": "assistant",
                            "content": "New chat started. What company do you want to research?"
                        }
                    ]
                    st.session_state.current_chat_id = new_chat_id
                else:
                    st.session_state.current_chat_id = next(iter(st.session_state.chats))

                st.rerun()

    st.divider()
    st.header("Example Questions")
    st.code("Find competitors of Nanyang Polytechnic")
    st.code("Compare Singapore Polytechnic with it")
    st.code("Analyze OpenAI competitors")


messages = get_current_messages()

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Ask about a company or competitor comparison...")

if user_input:
    messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching Google and analyzing..."):
            try:
                result = st.session_state.agent.run(
                    user_input=user_input,
                    chat_history=messages
                )
            except Exception as e:
                result = f"Something went wrong: `{e}`"

        st.markdown(result)

    messages.append({
        "role": "assistant",
        "content": result
    })