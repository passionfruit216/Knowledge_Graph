# -*- coding: utf-8 -*-
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import RetrievalQA
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
os.environ["OPENAI_API_KEY"] = "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"
url = "neo4j://localhost:7687"
username = "neo4j"
password = "12345678"
index_name = "*"
store = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    index_name=index_name,
)
result = store.similarity_search("感冒怎么护理?", k=2)
print(result)
retriever = store.as_retriever()

template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案。尽量使答案简明扼要。”。
{context}
问题: {question}
有用的回答:"""
prompt = PromptTemplate(
    template=template,
    input_variables=[
        "context",
        "question"])
qa_chain = RetrievalQA.from_chain_type(
    ChatOpenAI(temperature=0),
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)

print(qa_chain({"query": "感冒怎么护理?"})["result"])
