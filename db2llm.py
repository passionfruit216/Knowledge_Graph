# -*- coding: utf-8 -*-
from Chat_GLM4 import chat_glm4
from DataBase import Data2Neo4j
import re
from langchain.prompts.chat import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.output_parsers import StructuredOutputParser,ResponseSchema

class inputs2db():
    def __init__(self,DataBase,apikey ="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II"):
        self.db = DataBase
        self.llm = chat_glm4(apikey)
        print("**************** 根据用户的提问生成查询语句 *******************")


    def text2Cypher(self,texts:str):
        template = """请你将用户的内容根据主体列表提取分别提取 唯一主体 和 主题 ,并从主题列表中确定这句话所询问的主题是什么,然后以{format_instructions}的格式返回,如果无法确定主题,请返回'无法确定主题'。\n
        主题列表:{topic}
        主体列表:{Subject}
        """
        human_template = "{text}"
        Human_message = HumanMessagePromptTemplate.from_template(human_template)
        Sys_message=SystemMessagePromptTemplate.from_template(template)
        response_schemas =[
            ResponseSchema(name="主题", description="提取到的主题"),
            ResponseSchema(name="主体",description="提取到的唯一主体")
        ]
        OutputParser=StructuredOutputParser.from_response_schemas(response_schemas)
        message = ChatPromptTemplate.from_messages([Human_message, Sys_message])
        chain=LLMChain(llm = self.llm,prompt=message)
        res = chain.run({"text":texts,"format_instructions":OutputParser.get_format_instructions(),"topic":db.show_all_label(),"Subject":db.show_all_Node()})
        print(res)
        pattern = r'": "(.*?)"'
        matches = re.findall(pattern, res)
        label = matches[0]
        name = matches[1]
        query=self.db.Precise_queries(label, name)
        print("生成的Cypher语句为{}".format(query))



