# -*- coding: utf-8 -*-
from Chat_GLM3 import Chat_GLM3
from Chat_GLM3_T import chat_glm3_t
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
llm = chat_glm3_t(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")  # 自行填写自己的api
format = """输出以python字典的格式输出.其中包含三个键,一个是唯一主体,一个是关系三元组,一个是主题,格式如下:\n
        主题: 根据用户文本内容确定的主题\n
        唯一主体: 根据用户文本内容确定的唯一主体\n 
        关系: 根据用户文本内容提取的关系三元组\n
        """
texts = """松鼠，是啮齿目松鼠科松鼠属 [5]的哺乳动物。松鼠的体形细长，后肢更长；前后肢间无皮翼，四肢强健；眼大而明亮，耳朵长，耳尖有一束毛，冬季尤其显著；夏毛一般为黑褐色或赤棕色，冬毛多呈灰色、烟灰色或灰褐色，腹毛为白色；指、趾端有尖锐的钩爪，尾毛多而且蓬松，常朝向背部反卷。松鼠雌性个体比雄性个体稍重一些。 [6]因为松鼠的样子像老鼠，而且大多数喜欢啃食松果之类的坚果，习惯生活在树木尤其是松树上，故名。 [7]
松鼠广泛分布在亚洲、南北美洲和欧洲。 [8]松鼠的栖息地多种多样，从热带雨林到北温带针叶林、苔原、高山草甸，再到半干旱的沙漠地带、农业用地和城市公园；有些种类为树栖，在树枝上和树洞里做窝；有些是陆栖，在地下挖洞。
"""
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
human_message = HumanMessagePromptTemplate.from_template(
    human_template)
message = ChatPromptTemplate.from_messages(
    [sys_message, human_message])
chain = LLMChain(llm=llm, prompt=message)
res = chain.run(
    {"text": texts, "format_instructions": format})
print(res)
