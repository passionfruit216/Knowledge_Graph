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
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from langchain_community.chat_models import ChatZhipuAI
langchain_community.chat_models.zhipuai
async def main():
    llm = chat_glm4(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")
    prompt = ChatPromptTemplate.from_template("告诉我一个关于 {topic} 的笑话")
    parser = StrOutputParser()
    chain = prompt | llm | parser

    async for chunk in chain.stream({"topic": "鹦鹉"}):
        print(chunk, end="|", flush=True)

if __name__ == "__main__":
    asyncio.run(main())


