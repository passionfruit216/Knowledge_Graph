# -*- coding: utf-8 -*-
from langchain.chains import LLMChain
from Chat_GLM4 import chat_glm4
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
# llm = chat_glm4(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")  # 自行填写自己的api
#
# conversation = ConversationChain(
#     llm=llm,
#     verbose=True,
#     memory=ConversationSummaryMemory(llm=llm,verbose=True)
# )
# print(conversation.predict(input="Hi there!"))
# print(conversation.predict(input="I'm doing well! Just having a conversation with an AI."))
from DataBase import Data2Neo4j
db= Data2Neo4j(url="neo4j://localhost:7687",username="neo4j",password="12345678")  # 自行填写自己的数据库
from Controller import controller
from Chat_GLM4 import chat_glm4
from Chat_GLM3 import Chat_GLM3
from Chat_GLM3_T import chat_glm3_t
llm = chat_glm3_t(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")  # 自行填写自己的api
controller =controller(DataBase=db,LLM=llm)
texts ="""松鼠，是啮齿目松鼠科松鼠属 [5]的哺乳动物。松鼠的体形细长，后肢更长；前后肢间无皮翼，四肢强健；眼大而明亮，耳朵长，耳尖有一束毛，冬季尤其显著；夏毛一般为黑褐色或赤棕色，冬毛多呈灰色、烟灰色或灰褐色，腹毛为白色；指、趾端有尖锐的钩爪，尾毛多而且蓬松，常朝向背部反卷。松鼠雌性个体比雄性个体稍重一些。 [6]因为松鼠的样子像老鼠，而且大多数喜欢啃食松果之类的坚果，习惯生活在树木尤其是松树上，故名。 [7]
松鼠广泛分布在亚洲、南北美洲和欧洲。 [8]松鼠的栖息地多种多样，从热带雨林到北温带针叶林、苔原、高山草甸，再到半干旱的沙漠地带、农业用地和城市公园；有些种类为树栖，在树枝上和树洞里做窝；有些是陆栖，在地下挖洞。
"""
print(controller.generate_short_text(texts))
# nodes = db.show_all_Node()
# print(nodes)
# print(type(nodes))
# relations = db.show_all_relation()
# print(relations)
# print(type(relations))
# db.save_as_Html(file_name="text.html")