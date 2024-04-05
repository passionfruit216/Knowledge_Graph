# -*- coding: utf-8 -*-
import streamlit as st
from Controller import controller
from DataBase import Data2Neo4j
from Chat_GLM4 import chat_glm4
import streamlit.components.v1 as components
st.title("知识图谱的文本嵌入和展示")
# 加载模型
st_model_load = st.text('正在加载模型和数据库...')
api_key = st.sidebar.text_input('ChatGLM API Key', type='password',value="99035d83fb0030cfd79347eb96cd67f8.GeZj2XSObGEsgpB3")
url = st.sidebar.text_input('Neo4j URL', value="neo4j://localhost:7687",type='default')
username = st.sidebar.text_input('Neo4j Username', value="neo4j",type='default')
pwd = st.sidebar.text_input('Neo4j Password', type='password')
db= Data2Neo4j(url=url,username=username,password=pwd)
llm = chat_glm4(zhipuai_api_key=api_key)
controller = controller(DataBase=db,LLM=llm)
st.success('Model loaded!')
st_model_load.text("")
tab1, tab2 = st.tabs(["根据文本生成并展示知识图谱", "将关系插入到数据库"])
placeholder_string = """这是一个示例文本:松鼠，是啮齿目松鼠科松鼠属 [5]的哺乳动物。松鼠的体形细长，后肢更长；前后肢间无皮翼，四肢强健；眼大而明亮，耳朵长，耳尖有一束毛，冬季尤其显著；夏毛一般为黑褐色或赤棕色，冬毛多呈灰色、烟灰色或灰褐色，腹毛为白色；指、趾端有尖锐的钩爪，尾毛多而且蓬松，常朝向背部反卷。松鼠雌性个体比雄性个体稍重一些。 [6]因为松鼠的样子像老鼠，而且大多数喜欢啃食松果之类的坚果，习惯生活在树木尤其是松树上，故名。 [7]
松鼠广泛分布在亚洲、南北美洲和欧洲。 [8]松鼠的栖息地多种多样，从热带雨林到北温带针叶林、苔原、高山草甸，再到半干旱的沙漠地带、农业用地和城市公园；有些种类为树栖，在树枝上和树洞里做窝；有些是陆栖，在地下挖洞。 [9]松鼠在白天活动，清晨频繁，视觉和听觉发达，不冬眠，有贮存食物的习性。 [10]松鼠是杂食动物，吃多种植物，包括坚果、种子、松球、水果、菌类和绿色植物，也吃昆虫。 [11]松鼠1-2月发情，孕期35-40天，1年繁殖2次，一般每胎4-6仔， [12]寿命4-10年。 [13]
"""
if "state" not in st.session_state:
    st.session_state.state = False
if 'text' not in st.session_state:
    st.session_state.text = ""
text = st.session_state.text
text = st.text_area('Text:', value=text, height=300, disabled=False, max_chars=30000, placeholder=placeholder_string)
with tab1:
    button_text = "根据文本生成并展示知识图谱"
    with st.spinner('正在生成知识图谱...'):
        if st.button(button_text):
            result=controller.generate_short_text(text)
            # st.write(result["关系"])
            print(result)
            db.create_temp_html(relations=result)
            st.session_state.kb_chart = "./networks/temp.html"
            st.session_state.result = result
            if 'kb_chart' not in st.session_state:
                st.session_state.kb_chart = None
            if 'result' not in st.session_state:
                st.session_state.result = {}
            if st.session_state.kb_chart:
                with st.container():
                    st.subheader("生成的知识图谱")
                    st.markdown("你可以拖动并查看知识图谱")
                    html_source_code = open(st.session_state.kb_chart, 'r', encoding='utf-8').read()
                    components.html(html_source_code, width=700, height=700)
                    st.session_state.state= True
            st.success('知识图谱生成成功', icon="✅")
with tab2:
    if  st.session_state.state == False:
        st.warning("请先生成知识图谱",icon="⚠️")
        st.session_state.result = {}
    else:
        clicked = st.button("将关系插入到数据库",on_click=controller.insert_short_text(text=st.session_state.result))
        if clicked :
            relations_legth = len(st.session_state.result["关系"])
            st.success('成功插入{}条关系到数据库!'.format(relations_legth), icon="✅")
