# -*- coding: utf-8 -*-
import streamlit as st
import time
import numpy as np
from DataBase import Data2Neo4j
from Chat_GLM4 import chat_glm4
from Controller import controller
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
st.title("知识图谱问答系统")
with st.spinner("正在加载模型..."):
    time.sleep(1.5)
with st.container():
    on = st.toggle('知识库聊天模式')
# st.session_state.clear()
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory= ConversationBufferMemory(verbose=True)
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

if 'requests' not in st.session_state:
    st.session_state['requests'] = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
api_key = st.sidebar.text_input('ChatGLM API Key', type='password',value="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")
url = st.sidebar.text_input('Neo4j URL', value="neo4j://localhost:7687",type='default')
username = st.sidebar.text_input('Neo4j Username', value="neo4j",type='default')
pwd = st.sidebar.text_input('Neo4j Password', type='password')
db= Data2Neo4j(url=url,username=username,password=pwd)
llm = chat_glm4(zhipuai_api_key=api_key)
controller = controller(DataBase=db,LLM=llm)


if on:
    prompt=st.chat_input("请输入问题")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        responce = controller.query(text=prompt)

        with st.chat_message("bot"):
            st.markdown(responce)
        st.session_state.messages.append({"role": "bot", "content": responce})
else:
    if len(st.session_state.messages) == 0:
        st.warning("历史消息列表为空")
    question = st.chat_input("请输入问题")
    if question:
        conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=st.session_state.buffer_memory
        )
        result = conversation.predict(input=question)
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("bot"):
            st.markdown(result)
        st.session_state.messages.append({"role": "bot", "content": result})