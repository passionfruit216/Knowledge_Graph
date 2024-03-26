# -*- coding: utf-8 -*-
import re
from langchain.prompts.chat import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
# 后续封装成类 text2neo4j
class text2neo4j():
    def __init__(self,DataBase,LLM):
        self.db =DataBase
        self.llm = LLM
    def get_texts(self,text:str):
        template="""请你根据用户的输入内容,尽量依据下面的主题列表归纳一个输入的主题,如果实在找不到就自行归纳一个主题.
        然后将用户的输入内容提取尽可能多的关系三元组,按照{format_instructions}的方式输出,可以自行完善一些关系.\n
        主题列表:{toxic}
        用户的输入:
        """
        sys_message= SystemMessagePromptTemplate.from_template(template)
        human_template =  "{text}"
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        message = ChatPromptTemplate.from_messages([sys_message,human_message])
        Responses = [
            ResponseSchema(name="主题",description="根据内容归纳出的主题"),
            ResponseSchema(name="主体",description="提取到的主体"),
            ResponseSchema(name="关系", description="提取到的关系"),
            ResponseSchema(name="主体",description="提取到的主体")
        ]
        OutputParser = StructuredOutputParser.from_response_schemas(Responses)
        chain = LLMChain(llm=self.llm,prompt=message)
        chain.run({"text":text,"format_instructions":OutputParser.get_format_instructions(),"toxic":self.db.show_all_label()})




    # def text2db(self,words):
    #     Relations = words.split('[')[1].split(']')[0]
    #     pattern = r"\{'head': '(.*?)', 'relation': '(.*?)', 'tail': '(.*?)'\}"
    #
    #     matches = re.findall(pattern, Relations)
    #     res = ""
    #     for match in matches:
    #         db.create_node("疾病", match[0])
    #         db.create_node("疾病", match[2])
    #         db.create_relation("疾病", match[0], match[2], match[1])
    #         res += "添加了关系:" + match[0] + "-" + match[1] + "-" + match[2] + "\n"

# 实现 更详细的关系添加和关系融合


