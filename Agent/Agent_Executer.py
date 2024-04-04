# -*- coding: utf-8 -*-
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
from Chat_GLM4 import chat_glm4
from Basic_OutputParser import Basic_OutPutParser
from Custom_Agent_Prompt import Custom_Agent_Promptlate
from Tool_List import BasicSearchTool
SERPAPI_API_KEY = "c77aa41c55a1ece06909530ccfbe99a6fb2242bded10bb4b7cac7aad6ebc600d"
llm = chat_glm4(zhipuai_api_key="9014647fdc7a2ea48bff0a141543bdf3.MLP0Fp7UeKjJ19II")
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
# 加载工具
Tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="基于搜索引擎的搜索工具,当您需要在互联网上搜索信息时很有用"
    ),

]

print(Tools)


# 加载模板

template = """
请尽可能以逻辑思维回答下列问题。您可以使用以下工具:

{tools}
使用以下格式:

问题: 你必须回答的输入问题
想法: 你应该经常思考该怎么做
行动: 要采取的行动，应是[{tool_names}]之一
行动输入: 行动的输入
观察: 行动的结果
......（这种想法/行动/行动输入/观察可以重复 N 次）
想法: 我现在知道最终答案了
最终答案: 原始输入问题的最终答案(严格按照格式输出)\n

例子:
提问: 电视剧狂飙的演员表?
问题: 电视剧狂飙的演员表?
想法: 我需要查询电视剧《狂飙》的演员表，这是一项需要搜索的任务。
行动: Search
行动输入: 电视剧狂飙演员表
观察: 电视剧狂飙的详细信息
想法: 我现在知道最终答案了
输出的文本:最终答案: 电视剧《狂飙》的演员阵容包括张译、张颂文、李一桐、张志坚、吴刚等主演，以及倪大红、韩童生、李建义、石兆琪等特邀主演。该剧由李健、高叶、王骁等演员主演。

开始！按照例子进行回答，记住要以助手的口吻说话。Let's think step by step
提问: {input}
{agent_scratchpad}
"""
prompt = Custom_Agent_Promptlate(
    template=template,
    tools=Tools,
    input_variables=["input", "intermediate_steps"]
)

output_parser = Basic_OutPutParser()
llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in Tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\n观察:"],
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=Tools, verbose=True,handle_parsing_errors=True)
res=agent_executor.run("电视剧狂飙的演员表?")
print(res)