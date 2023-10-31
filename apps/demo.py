import os
import tempfile
import streamlit as st
import openai

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.graphs import RdfGraph
from langchain.chains import GraphSparqlQAChain


st.set_page_config(page_title="LangChain: Chat with Knowledge Graph", page_icon="🦜")
st.title("🦜 LangChain: Chat with Knowledge Graph at UAM domain")


# @st.cache_resource(ttl="1h")
# def configure_retriever(uploaded_files):
#     # Read documents
#     docs = []
#     temp_dir = tempfile.TemporaryDirectory()
#     for file in uploaded_files:
#         temp_filepath = os.path.join(temp_dir.name, file.name)
#         with open(temp_filepath, "wb") as f:
#             f.write(file.getvalue())
#         loader = PyPDFLoader(temp_filepath)
#         docs.extend(loader.load())

#     # Split documents
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
#     splits = text_splitter.split_documents(docs)

#     # Create embeddings and store in vectordb
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

#     # Define retriever
#     retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})

#     return retriever


# class StreamHandler(BaseCallbackHandler):
#     def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
#         self.container = container
#         self.text = initial_text
#         self.run_id_ignore_token = None

#     def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
#         # Workaround to prevent showing the rephrased question as output
#         if prompts[0].startswith("Human"):
#             self.run_id_ignore_token = kwargs.get("run_id")

#     def on_llm_new_token(self, token: str, **kwargs) -> None:
#         if self.run_id_ignore_token == kwargs.get("run_id", False):
#             return
#         self.text += token
#         self.container.markdown(self.text)


# class PrintRetrievalHandler(BaseCallbackHandler):
#     def __init__(self, container):
#         self.status = container.status("**Context Retrieval**")

#     def on_retriever_start(self, serialized: dict, query: str, **kwargs):
#         self.status.write(f"**Question:** {query}")
#         self.status.update(label=f"**Context Retrieval:** {query}")

#     def on_retriever_end(self, documents, **kwargs):
#         for idx, doc in enumerate(documents):
#             source = os.path.basename(doc.metadata["source"])
#             self.status.write(f"**Document {idx} from {source}**")
#             self.status.markdown(doc.page_content)
#         self.status.update(state="complete")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.")
#     st.stop()

# uploaded_files = st.sidebar.file_uploader(
#     label="Upload PDF files", type=["pdf"], accept_multiple_files=True
# )
# if not uploaded_files:
#     st.info("Please upload PDF documents to continue.")
#     st.stop()

# retriever = configure_retriever(uploaded_files)

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

graph = RdfGraph(
    source_file="http://www.w3.org/People/Berners-Lee/card",
    standard="rdf",
    local_copy="test.ttl",
)

graph.load_schema()
# graph.get_schema

qa_chain = GraphSparqlQAChain.from_llm(
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
        # retrieval_handler = PrintRetrievalHandler(st.container())
        # stream_handler = StreamHandler(st.empty())
        # response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
        response = qa_chain.run(user_query)