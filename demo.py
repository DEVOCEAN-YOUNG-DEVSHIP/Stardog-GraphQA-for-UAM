import os
import tempfile
import streamlit as st
import openai

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from libs.langchain.graphs.stardog_graph import StardogGraph
from libs.langchain.chains.graph_qa.stardog import StardogQAChain

st.set_page_config(page_title="LangChain: Chat with Knowledge Graph", page_icon="🦜")
st.title("🦜 LangChain: Chat with Knowledge Graph at UAM domain")

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
# qa_chain = ConversationalRetrievalChain.from_llm(
#     llm, retriever=retriever, memory=memory, verbose=True
# )

graph = stardog_graph = StardogGraph(**conn_details)

# graph.load_schema()
# graph.get_schema

qa_chain = StardogQAChain.from_llm(
    ChatOpenAI(temperature=0.5), graph=graph, verbose=True
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
        # stream_handler = StreamHandler(st.empty())
        # response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
        response = qa_chain.run(user_query)