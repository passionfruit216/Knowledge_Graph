# -*- coding: utf-8 -*-
import re
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from Custom_paser import CustomOutputParser
from langchain.output_parsers import OutputFixingParser


# 实现用户输入的文本提取关系并插入数据库


class text2neo4j():
    def __init__(self, DataBase, LLM):
        self.db = DataBase
        self.llm = LLM

    def get_texts(self, text: str):
        template = """你擅长提取实体,请你提取所有的实体并组成关系三元组,必须把所有的实体都用到,请仔细检查,做到不遗漏每个实体的三元组\n
输出格式:{format_instructions}\n
用户输入的文字:
        """
        sys_message = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        OutputParser = CustomOutputParser()
        human_message = HumanMessagePromptTemplate.from_template(
            human_template)
        message = ChatPromptTemplate.from_messages(
            [sys_message, human_message])
        chain = LLMChain(llm=self.llm, prompt=message)
        res = chain.run(
            {"text": text, "format_instructions": OutputParser.get_format_instructions()})
        output = OutputParser.parse(res)
        if output is None:
            new_parser = OutputFixingParser.from_llm(parser=OutputParser, llm=self.llm)
            output=new_parser.parse(res)
        print(output)
        return output

    def text2db(self, output: dict):
        label = output["主题"]
        name = output["唯一主体"]
        if not self.db.node_is_exist(label, name):
            self.db.create_node(label, name)
        for i in output["关系"]:
            if not self.db.node_is_exist(label, i[0]):
                self.db.create_node(label, i[0])
            if not self.db.node_is_exist(label, i[2]):
                self.db.create_node(label, i[2])
            self.db.create_relation(label, i[0], i[2], i[1])
        print("关系创建成功")
