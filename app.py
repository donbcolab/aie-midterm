import os
import chainlit as cl
from dotenv import load_dotenv
from operator import itemgetter
from langchain import hub
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable.config import RunnableConfig

from starters import set_starters

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_API_URL = os.environ["QDRANT_API_URL"]

LANGCHAIN_PROJECT = "AirBnB PDF Jun18"
LANGCHAIN_ENDPOINT = os.environ["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]
LANGCHAIN_TRACING_V2 = os.environ["LANGCHAIN_TRACING_V2"]

LLAMA3_PROMPT = hub.pull("rlm/rag-prompt-llama3")
# LLAMA3_PROMPT = hub.pull("cracked-nut/securities-comm-llama3-v2")

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
collection = "airbnb_pdf_rec_1000_200_images"
llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)

qdrant = Qdrant.from_existing_collection(
    embedding=embedding,
    collection_name=collection,
    url=QDRANT_API_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,   
)

retriever = qdrant.as_retriever(search_kwargs={"k": 5})

@cl.on_chat_start
async def start_chat():
    rag_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": LLAMA3_PROMPT | llm, "context": itemgetter("context")}
    )

    cl.user_session.set("rag_chain", rag_chain)

@cl.on_message
async def main(message: cl.Message):
    rag_chain = cl.user_session.get("rag_chain")

    msg = cl.Message(content="")

    response = await rag_chain.ainvoke(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    )

    context = response["context"]
    response_content = response["response"].content

    await msg.stream_token(response_content)
    await msg.send()
