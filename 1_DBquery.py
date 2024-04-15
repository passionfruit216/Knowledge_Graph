# -*- coding: utf-8 -*-
import streamlit as st
import time
import numpy as np
from DataBase import Data2Neo4j
from Chat_GLM4 import chat_glm4
from Chat_GLM3_T import chat_glm3_t
from Controller import controller
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from vector_store import vector_store
st.title("知识图谱问答系统")
with st.spinner("正在加载模型..."):
    time.sleep(1.5)
with st.container():
    option = st.selectbox("请选择对话模型", ["Chat-GLM4", "Chat-GLM3-TURBO"])
with st.container():
    on = st.toggle('知识库聊天模式')
with st.container():
    network = st.toggle("联网开关")
# st.session_state.clear()
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory= ConversationBufferMemory(verbose=True)
if 'responses' not in st.session_state:
    st.session_state['responses'] = []
if "buffer_window_memory" not in st.session_state:
    st.session_state.buffer_window_memory = ConversationBufferWindowMemory( memory_key='chat_history',
        k=5,
        return_messages=True)
if 'requests' not in st.session_state:
    st.session_state['requests'] = []
if "history" not in st.session_state:
    st.session_state.history = False
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
api_key = st.sidebar.text_input('ChatGLM API Key', type='password',value="99035d83fb0030cfd79347eb96cd67f8.GeZj2XSObGEsgpB3")
url = st.sidebar.text_input('Neo4j URL', value="neo4j://localhost:7687",type='default')
username = st.sidebar.text_input('Neo4j Username', value="neo4j",type='default')
pwd = st.sidebar.text_input('Neo4j Password', type='password',placeholder="12345678",value="12345678")
if pwd == "":
    st.toast('请填写Neo4j密码', icon="⚠️")
db= Data2Neo4j(url=url,username=username,password=pwd)
if option == "Chat-GLM4":
    llm = chat_glm4(zhipuai_api_key=api_key)
elif option == "Chat-GLM3-TURBO":
    llm = chat_glm3_t(zhipuai_api_key=api_key)

if "pwd" not in st.session_state:
    st.session_state.pwd = pwd
if "vector_db" not in st.session_state:
    st.session_state.vector_db = vector_store()

if "controller" not in st.session_state:
    st.session_state.controller = controller(DataBase=db,LLM=llm,Vector_Store=st.session_state.vector_db)


if on:
    prompt=st.chat_input("请输入问题")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.progress(0, text=None):
            responce = st.session_state.controller.query(text=prompt)

        with st.chat_message("bot"):
            st.markdown(responce)
        st.session_state.messages.append({"role": "bot", "content": responce})
        st.session_state.history = True
    if network:
        st.warning("知识库聊天模式下无法联网")
else:
    question = st.chat_input("请输入问题")
    if question:
        if network:
            agent=st.session_state.controller.agent_init()
            result=agent.run(question,chat_history=st.session_state.buffer_window_memory)
        else:
            conversation = ConversationChain(
                llm=llm,
                verbose=True,
                memory=st.session_state.buffer_memory
            )
            result = conversation.stream(input=question)
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("bot"):
            st.write(result)
        st.session_state.messages.append({"role": "bot", "content": result})
        st.session_state.history = True