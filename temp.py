# -*- coding: utf-8 -*-
from db2llm import *
import ast
from DataBase import Data2Neo4j
from textSeq import *
from langchain.prompts.chat import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate
from langchain.chains import LLMChain
from Chat_GLM4 import chat_glm4
from textSeq import text2neo4j
from Custom_paser import CustomOutputParser
llm = chat_glm4(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")
db= Data2Neo4j(url="neo4j://localhost:7687",username="neo4j",password="12345678")
# db2llm = inputs2db(db)
# text2db =text2neo4j(DataBase=db,LLM=llm)
# texts = """树袋熊，是双门齿目树袋熊科树袋熊属动物。树袋熊体型粗壮；头大；耳圆；无尾；鼻大而裸露，呈匙状；毛被厚实，背毛毛色从浅灰色到巧克力色；腹毛白色；眼小；育儿袋口由括约肌控制，防止幼仔跌落。 [12]树袋熊因其外形像小熊而得名。 [13]
# 树袋熊是澳大利亚特有类群，分布在昆士兰东南部、新南威尔士东部、南澳大利亚东南部及维多利亚。树袋熊栖息于空旷桉树林中，一生大部分时间生活在桉树上。树袋熊每天睡眠17-20小时；具夜行性；行动迟缓；具领域性，通过在树基部留下排泄物进行领地标记；属非社会性动物；成年雄性利用大声吼叫威胁对手并吸引配偶； [12]性情温顺。 [15]树袋熊以桉树叶及其嫩枝为食。树袋熊的繁殖季节从仲春至早秋，孕期33-35天，1胎1仔，偶有双胞胎，通常2年繁殖一次。树袋熊寿命13-18年。 [12]
# 树袋熊的威胁在1924年达到了顶峰，当年有200多万张树袋熊皮出口，在此之前，树袋熊在澳大利亚南部已灭绝，在维多利亚和新南威尔士州也基本消失，之后当地政府开始颁布狩猎禁令，加强管理，衰减趋势才得以逆转。树袋熊是澳大利亚的标志性动物，也是世界上最有魅力的哺乳动物之一。 [14]树袋熊被世界自然保护联盟（IUCN）收入在《世界自然保护联盟濒危物种红色名录》中，为易危（VU）保护等级。 [16]
# """
# text2db.get_texts(texts)
# db2llm.text2Cypher("感冒的症状有哪些")
# human_message = "{text}"
# human_template=HumanMessagePromptTemplate.from_template(human_message)
# template="""你擅长关系提取,将用户输入的文字按照例子尽可能多的进行关系提取,并确定文本内容的唯一主体.并从主题列表确认用户输入文字的主题,如果主题列表中无法确定主题,请自行确认主题.
# 主题列表:[动物,植物,人物,地点,事件,其他]
# 并以{format_instructions}的格式输出.\n
# 例子: 树袋熊的生活几乎全部在桉树上度过，每天睡眠时间长达17-20小时，具有夜行性和领域性
# 提取到的关系:(树袋熊,生活在,树上),(树袋熊,睡眠时间,17-20小时),(树袋熊,习性,夜行性和领域性)
# 提取到的唯一主体: 树袋熊
# 用户输入的文字:
# """
# sys_message=  SystemMessagePromptTemplate.from_template(template)
# chat_template = ChatPromptTemplate.from_messages([sys_message,human_template])
# chain = LLMChain(llm=llm,prompt=chat_template)
# OutputParser=CustomOutputParser()
# texts="""袋鼠是双门齿目袋鼠亚目袋鼠科大袋鼠属的哺乳动物。 [6]袋鼠跳得最高、最远。 [7]雌性袋鼠都长有一个前开的育儿袋，袋鼠也因此得名。 [8]袋鼠泛指任一种属于袋鼠目的有袋动物， [7]它头小眼大耳朵长，面部较长，鼻孔两侧有黑色须痕。袋鼠胆小而机警，视觉、听觉、嗅觉都很灵敏。袋鼠以跳跃的方式生活，前肢短小而瘦弱，可以用来搂取食物，后肢强大，趾有合并现象。其粗壮的尾巴在栖息时起支撑作用，跳跃时起平衡作用。袋鼠喜欢聚成二三十只群体活动，为植食性动物。 [6]
# 袋鼠主要分布于澳洲大陆和巴布亚新几内亚的部分地区。其中，有些种类为澳大利亚独有。袋鼠是食草动物，也吃真菌类。 [7]以矮小润绿离地面近的小草为生，个别种类的也吃树叶或小树芽。 [9]它们大多在夜间活动，但也有些在清晨或傍晚活动。不同种类的袋鼠在澳大利亚各种不同的自然环境中生活，从凉性气候的雨林、沙漠、平原到热带地区都能看到它们的身影。 [7]袋鼠胎生，无胎盘，1—2月交配繁殖， [10]怀孕时间4—5周后分娩，幼崽出生时只有约2.5厘米。 [11-12]
# 袋鼠是澳大利亚的象征物，出现在澳大利亚的货币图案， [13]绿色三角形袋鼠代表澳大利亚制造，澳洲航空标识采用飞行袋鼠， [14]袋鼠也成为澳大利亚国徽上动物之一。 [13]
# """
# res =chain.run(text=texts,format_instructions=OutputParser.get_format_instructions())
# print(res)
# pattern = r"\{([^}]+)\}"
# # 匹配文本中的字典内容
# match = re.search(pattern, res)
# if match:
#     dict_content = "{" + match.group(1) + "}"
#     result = eval(dict_content)  # 使用eval函数将字符串转换为字典
#     print(result)
#     print(type(result))
# else:
#     print("未找到匹配的字典内容")
tool=text2neo4j(db,llm)
texts="""袋鼠是双门齿目袋鼠亚目袋鼠科大袋鼠属的哺乳动物。 [6]袋鼠跳得最高、最远。 [7]雌性袋鼠都长有一个前开的育儿袋，袋鼠也因此得名。 [8]袋鼠泛指任一种属于袋鼠目的有袋动物， [7]它头小眼大耳朵长，面部较长，鼻孔两侧有黑色须痕。袋鼠胆小而机警，视觉、听觉、嗅觉都很灵敏。袋鼠以跳跃的方式生活，前肢短小而瘦弱，可以用来搂取食物，后肢强大，趾有合并现象。其粗壮的尾巴在栖息时起支撑作用，跳跃时起平衡作用。袋鼠喜欢聚成二三十只群体活动，为植食性动物。 [6]
袋鼠主要分布于澳洲大陆和巴布亚新几内亚的部分地区。其中，有些种类为澳大利亚独有。袋鼠是食草动物，也吃真菌类。 [7]以矮小润绿离地面近的小草为生，个别种类的也吃树叶或小树芽。 [9]它们大多在夜间活动，但也有些在清晨或傍晚活动。不同种类的袋鼠在澳大利亚各种不同的自然环境中生活，从凉性气候的雨林、沙漠、平原到热带地区都能看到它们的身影。 [7]袋鼠胎生，无胎盘，1—2月交配繁殖， [10]怀孕时间4—5周后分娩，幼崽出生时只有约2.5厘米。 [11-12]
袋鼠是澳大利亚的象征物，出现在澳大利亚的货币图案， [13]绿色三角形袋鼠代表澳大利亚制造，澳洲航空标识采用飞行袋鼠， [14]袋鼠也成为澳大利亚国徽上动物之一。 [13]
"""
tool.text2db(texts)
# res=db.node_is_exist(label="疾病",name="感冒")
# if res :
#     print("节点存在")
# else:
#     print("节点不存在")