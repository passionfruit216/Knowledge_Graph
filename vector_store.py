# -*- coding: utf-8 -*-
from langchain_community.vectorstores import Neo4jVector
import os
from tqdm import tqdm
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_community.vectorstores import Chroma


class vector_store():git 
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="infgrad/stella-mrl-large-zh-v3.5-1792d")
        vectordb = Chroma(persist_directory="database/vector_db", embedding_function=self.embeddings)
        self.store = vectordb
        # self.embeddings = OpenAIEmbeddings()



    def serach_node(self,question:str):
        return self.store.similarity_search_with_score(question,k=1)

    def add_node(self,name:List):
        self.store.add_texts(name)
        print("添加节点成功")

    def create_database(self,path:str="database/vector_db"):
        # 构建向量数据库
        persist_directory = path

        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
            print(f"文件夹 '{persist_directory}' 创建成功！")
        else:
            print(f"文件夹 '{persist_directory}' 已经存在。")

        # 加载数据库
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        # 将加载的向量数据库存到磁盘上
        vectordb.persist()
        self.store=vectordb

