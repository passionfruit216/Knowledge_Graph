# -*- coding: utf-8 -*-
from DataBase import Data2Neo4j
from Chat_GLM4 import chat_glm4

llm = chat_glm4(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")  # 自行填写自己的api
from langchain.memory import ConversationBufferMemory  #　实现连续对话
db= Data2Neo4j(url="neo4j://localhost:7687",username="neo4j",password="12345678",llm=llm)  # 自行填写自己的数据库
res = db.merge(label="动物")
for i in res:
    for j in res:
        if i==j:
            continue
        db.create_relation(label="动物",head=i,tail=j,relation="属于")