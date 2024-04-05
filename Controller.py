# -*- coding: utf-8 -*-
from db2LLM import inputs2db
from textSeq import text2neo4j
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.llm import LLMChain
from langchain.cache import SQLiteCache
from Agent.Agent_Executer import Custom_Agent
from langchain.chains import ConversationChain
from pyvis.network import Network
import time
from langchain.agents import AgentExecutor

# 程序的核心控制器
class controller():
    def __init__(self,DataBase,LLM):
        self.db = DataBase
        self.llm = LLM
        self.text2neo4j = text2neo4j(self.db, self.llm)
        self.input2db = inputs2db(DataBase=self.db,LLM=self.llm)
        self.cache = SQLiteCache(database_path="./cache.db")

    def insert_short_text(self,text:str):
        self.text2neo4j.text2db(text)
        # self.show_network()  待实现

    def generate_short_text(self,text:str):
        result =self.text2neo4j.get_texts(text)
        return result

    def insert_long_text(self,text:str):
        # 待使用vector_db实现
        pass


    def query(self,text:str):
        start_time = time.time()

        template="""请你根据以下关系数据库的查询结果,对用户的提问进行解答,如果无法解答,请返回'无法解答'.\n
        查询结果:{query_result}\n
        {chat_history}
        用户的提问:"{text}"
        """
        memory = ConversationSummaryMemory(llm=self.llm,memory_key="chat_history",input_key="text")
        prompt=PromptTemplate(input_variables=["query_result","chat_history","text"],
                       template=template)
        chain = LLMChain(llm=self.llm,prompt=prompt,memory=memory,verbose=True)
        result=chain.predict(text=text,query_result=self.input2db.text2Cypher(text))
        end_time = time.time()
        print(f"程序运行时间：{end_time - start_time}")
        # print(result)

        return result


    def show_network(self):
        pass


    def ordinary_chat(self,text:str):
        start_time = time.time()
        template = """You are a chatbot having a conversation with a human.

        {chat_history}
        Human: {human_input}
        Chatbot:"""

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template=template
        )
        memory = ConversationBufferWindowMemory(memory_key="chat_history",k=5)
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )
        result=llm_chain.predict(human_input=text)
        end_time = time.time()
        print(f"程序运行时间：{end_time - start_time}")
        return result


    def agent_init(self):
        self.agent=Custom_Agent(llm=self.llm)
        print("Agent初始化成功")
        return self.agent
