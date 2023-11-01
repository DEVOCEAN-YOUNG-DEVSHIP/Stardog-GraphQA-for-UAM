import os
import tempfile
import streamlit as st
import openai

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from libs.langchain.graphs.stardog_graph import StardogGraph
from libs.langchain.chains.graph_qa.stardog import StardogQAChain

st.set_page_config(page_title="EXPLAINABLE CHATBOT BY KNOWLEDGE GRAPH FOR UAM")
st.title("EXPLAINABLE CHATBOT BY KNOWLEDGE GRAPH FOR UAM")

openai.api_key = st.secrets["OPENAI_API_KEY"]

conn_details = {
    'endpoint': st.secrets["STARDOG_ENDPOINT"],
    'username': st.secrets["STARDOG_USERNAME"],
    'password': st.secrets["STARDOG_PASSWORD"],
    'database': st.secrets["STARDOG_DATABASE"]
}

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

# Setup LLM and QA chain
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, streaming=True
)

graph = stardog_graph = StardogGraph(**conn_details)

# graph.load_schema()
# graph.get_schema

qa_chain = StardogQAChain.from_llm(
    ChatOpenAI(temperature=0.5), 
    graph=graph, 
    verbose=True, 
    memory=memory
)

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response = qa_chain.run(user_query)
        st.write(response)