# -*- coding: utf-8 -*-
from zhipuai import ZhipuAI
from DataBase import Data2Neo4j
import re
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

url="neo4j://localhost:7687"
username="neo4j"
password="12345678"
db = Data2Neo4j(url=url,username=username,password=password)
text = """感冒是指百姓所说的“普通感冒”，又称“伤风”、急性鼻炎或上呼吸道感染。感冒是一种常见的急性上呼吸道病毒性感染性疾病，多由鼻病毒、副流感病毒、呼吸道合胞病毒、埃可病毒、柯萨奇病毒、冠状病毒、腺病毒等引起。临床表现为鼻塞、喷嚏、流涕、发热、咳嗽、头痛等，多呈自限性。大多散发，冬、春季节多发，季节交替时多发。
   """
result = get_texts(text)
print(result)
Relations = result.split('[')[1].split(']')[0]
pattern = r"\{'head': '(.*?)', 'relation': '(.*?)', 'tail': '(.*?)'\}"

matches = re.findall(pattern, Relations)

for match in matches:
    db.create_node("疾病", match[0])
    db.create_node("疾病", match[2])
    db.create_relation("疾病", match[0], match[2], match[1])
