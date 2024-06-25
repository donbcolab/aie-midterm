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

# from starters import set_starters

load_dotenv()

LANGCHAIN_PROJECT = os.environ["LANGCHAIN_PROJECT"]
LANGCHAIN_ENDPOINT = os.environ["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]
LANGCHAIN_TRACING_V2 = os.environ["LANGCHAIN_TRACING_V2"]
LANGCHAIN_HUB_PROMPT = os.environ["LANGCHAIN_HUB_PROMPT"]

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)
prompt = hub.pull(LANGCHAIN_HUB_PROMPT)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_API_URL = os.environ["QDRANT_API_URL"]
QDRANT_COLLECTION = os.environ["QDRANT_COLLECTION"]
collection = QDRANT_COLLECTION

qdrant = Qdrant.from_existing_collection(
    embedding=embedding,
    collection_name=collection,
    url=QDRANT_API_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,   
)

retriever = qdrant.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 5}
)

@cl.on_chat_start
async def start_chat():
    rag_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": prompt | llm, "context": itemgetter("context")}
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
