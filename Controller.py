# -*- coding: utf-8 -*-
from db2LLM import inputs2db
from textSeq import text2neo4j
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
import pandas as pd
import re
import os
from DataBase import *

# 程序的核心控制器
class controller():
    def __init__(self,DataBase,LLM):
        self.db = DataBase
        self.llm = LLM
        self.text2neo4j = text2neo4j(self.db, self.llm)
        self.input2db = inputs2db(DataBase=self.db,LLM=self.llm)

    def insert_short_text(self,text:str):
        self.text2neo4j.text2db(text)
        # self.show_network()  待实现


    def insert_long_text(self,text:str):
        # 待使用vector_db实现
        pass


    def query(self,text:str):

        template="""请你根据以下关系数据库的查询结果,对用户的提问进行解答,如果无法解答,请返回'无法解答'.\n
        查询结果:{query_result}
        用户的提问:
        """
        human_template = "{text}"
        system_message=SystemMessagePromptTemplate.from_template(template)
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        chat_message = ChatPromptTemplate.from_messages([system_message,human_message])
        chain = LLMChain(llm=self.llm,prompt=chat_message)
        result=chain.run(text=text,query_result=self.input2db.text2Cypher(text))
        # print(result)
        return result
