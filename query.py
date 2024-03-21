# -*- coding: utf-8 -*-

import os
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from Chat_GLM import *
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = "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"

db=Neo4jGraph(url="neo4j://localhost:7687", username="neo4j", password="12345678")

db.refresh_schema()
chain = GraphCypherQAChain.from_llm(ChatOpenAI(temperature=0), graph=db, verbose=True)

print(chain.invoke("感冒的别称是什么?"))
