# -*- coding: utf-8 -*-

from db2LLM import *
import ast
from DataBase import Data2Neo4j
from textSeq import *
from langchain.prompts.chat import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate
from langchain.chains import LLMChain
from Chat_GLM4 import chat_glm4
from textSeq import text2neo4j
from Custom_paser import CustomOutputParser
from Controller import controller
llm = chat_glm4(zhipuai_api_key="")  # 自行填写自己的api
from langchain.memory import ConversationBufferMemory  #　实现连续对话
db= Data2Neo4j(url="",username="",password="")  # 自行填写自己的数据库
controller=controller(DataBase=db,LLM=llm)  # 实例化控制器
question = "感冒的症状有哪些?"  #　 需要询问的问题
result=controller.query(text=question)
print(result)
texts="""李白（701年2月28日—762年12月） [28]，字太白，号青莲居士 [20]，祖籍陇西成纪（今甘肃省秦安县），出生于蜀郡绵州昌隆县（今四川省江油市青莲乡），一说出生于西域碎叶 [29]。唐朝伟大的浪漫主义诗人，凉武昭王李暠九世孙 [16] [23]。
为人爽朗大方，乐于交友，爱好饮酒作诗，名列“酒中八仙” [2]。曾经得到唐玄宗李隆基赏识，担任翰林供奉 [126]，赐金放还，游历全国，先后迎娶宰相许圉师、宗楚客的孙女。唐肃宗李亨即位后，卷入永王之乱，流放夜郎，辗转到达当涂县令李阳冰家。上元二年，去世，时年六十二 [16]。
著有《李太白集》 [26]，代表作有《望庐山瀑布》《行路难》《蜀道难》《将进酒》《早发白帝城》《黄鹤楼送孟浩然之广陵》等 [2]。李白所作词赋，就其开创意义及艺术成就而言，享有极为崇高的地位，后世誉为“诗仙”，与诗圣杜甫并称“李杜”。
"""
controller.insert_short_text(texts)  #　根据文本插入数据库
