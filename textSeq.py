# -*- coding: utf-8 -*-
from zhipuai import ZhipuAI
from DataBase import Data2Neo4j
import re

url="neo4j://localhost:7687"
username="neo4j"
password="12345678"
db = Data2Neo4j(url=url,username=username,password=password)
# 后续封装成类 text2neo4j
def get_texts(text):
    llm = ZhipuAI(api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")
    response = llm.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
                  {"role": "system", "content": "请你将用户的内容提取实体,并将它们生成关系三元组,以python字典格式发送.注意输出所有python字典格式的三元组,格式为{'head':'实体1','relation':'关系','tail':'实体2'}.如果无法提取三元组,请返回'无法提取三元组'。"},
                  {"role": "user", "content":text }
        ]
    )
    return response.choices[0].message.content


def text2db(words):
    Relations = words.split('[')[1].split(']')[0]
    pattern = r"\{'head': '(.*?)', 'relation': '(.*?)', 'tail': '(.*?)'\}"

    matches = re.findall(pattern, Relations)
    res = ""
    for match in matches:
        db.create_node("疾病", match[0])
        db.create_node("疾病", match[2])
        db.create_relation("疾病", match[0], match[2], match[1])
        res += "添加了关系:" + match[0] + "-" + match[1] + "-" + match[2] + "\n"


# 实现 更详细的关系添加和关系融合