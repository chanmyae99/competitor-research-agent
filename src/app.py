import streamlit as st
from dotenv import load_dotenv
from agent import CompetitorResearchAgent

load_dotenv()

st.set_page_config(
    page_title="Competitor Research Agent",
    page_icon="🔎"
)

st.title("🔎 Competitor Research Agent")
st.write("Ask me to research a company's competitors.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = CompetitorResearchAgent()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Example: Find competitors of OpenAI")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching and analyzing..."):
            result = st.session_state.agent.run(user_input)

        st.markdown(result)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })