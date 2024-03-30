# -*- coding: utf-8 -*-
import re
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from Custom_paser import CustomOutputParser


# 实现用户输入的文本提取关系并插入数据库


class text2neo4j():
    def __init__(self, DataBase, LLM):
        self.db = DataBase
        self.llm = LLM

    def get_texts(self, text: str):
        template = """你擅长关系提取,将用户输入的文字按照例子尽可能多的进行关系提取,并确定文本内容的唯一主体.并从主题列表确认用户输入文字的主题,如果主题列表中无法确定主题,请自行确认主题.
主题列表:[动物,植物,人物,地点,事件,其他]
并以{format_instructions}的格式输出.\n
例子: 树袋熊的生活几乎全部在桉树上度过，每天睡眠时间长达17-20小时，具有夜行性和领域性
提取到的关系:(树袋熊,生活在,树上),(树袋熊,睡眠时间,17-20小时),(树袋熊,习性,夜行性和领域性)
提取到的唯一主体: 树袋熊
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
