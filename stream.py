# -*- coding: utf-8 -*-
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
import gradio as gr
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from Chat_GLM4 import chat_glm4
llm = chat_glm4(zhipuai_api_key="")  # 自行填写自己的api
from langchain.memory import ConversationBufferMemory  #　实现连续对话
import streamlit as st
question = st.text_input("请输入您的问题")
if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory= ConversationBufferMemory(verbose=True)
# conversation = ConversationChain(
#     llm=llm,
#     verbose=True,
#     memory=st.session_state.buffer_memory
# )
# result = conversation.stream(input=question)
if question:
    chain = LLMChain(llm=llm, memory=st.session_state.buffer_memory, verbose=True,prompt=PromptTemplate(input_variables=["input"], template="用户的提问:{input}"))
    # result=chain.stream(input=question)
    result = chain.stream(input=question)
    st.write(result)
    print(type(result))
    st.write_stream(result)
