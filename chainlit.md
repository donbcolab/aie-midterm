# RAG Application for 10-Q Filing Reviews

## Built using the following specs:
- Data:  [AirBnB Securities Commision pdf](https://airbnb2020ipo.q4web.com/files/doc_financials/2024/q1/fdb60f7d-e616-43dc-86ef-e33d3a9bdd05.pdf) - Form 10-Q filing for Q1 of 2024
- LLM:  Llama3-70B running on Groq
- Embedding model:  OpenAI text-embedding-3-small
- Infrastructure / Framework:  LangChaing
- Vector Store: Qdrant
- UI:  Chainlit
- Deployment: Docker on HuggingFace Spaces

## RAG Data Ingestion

- Additional details on the Data Pipeline are in this [Jupyter Notebook](./airbnb_langchain_rag_loader_retriever.ipynb)

!["RAG Data Pipeline"](./airbnb-langchain-rag-loader.png)

## RAG Inference

!["RAG Inference"](./airbnb-langchain-rag-inference.png)

### Sample Questions

#### Question 1
- Question: What is Airbnb's 'Description of Business'?
- Response: Airbnb's 'Description of Business' is operating a global platform for unique stays and experiences, connecting hosts and guests online or through mobile devices to book spaces and experiences around the world.
- LangSmith trace: https://smith.langchain.com/public/ebdf5473-64ac-4f85-81ab-bd3c3d624969/r

#### Question 2
- Question: What was the total value of 'Cash and cash equivalents' as of December 31, 2023?
- Response: The total value of 'Cash and cash equivalents' as of December 31, 2023, is $2,369.
- LangSmith trace: https://smith.langchain.com/public/b0f93487-c729-4ccf-93f9-0354078282d8/r

#### Question 3
- Question: What is the 'maximum number of shares to be sold under the 10b5-1 Trading plan' by Brian Chesky?
- Response: The maximum number of shares to be sold under the 10b5-1 Trading plan by Brian Chesky is 1,146,000.
- LangSmith trace: https://smith.langchain.com/public/7fc4b549-2ea5-4b86-abf9-71d5e9a62738/r