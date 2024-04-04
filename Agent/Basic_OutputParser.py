# -*- coding: utf-8 -*-
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re


class Basic_OutPutParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "最终答案"  in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("最终答案:")[-1].strip()},
                log=llm_output,
            )


        pattern = r"行动\s*\d*\s*:(.*?)\行动\s*\d*\s*输入\s*\d*\s*:[\s]*(.*)"
        match = re.search(pattern, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"无法解析模型的输出: `{llm_output}`")
        print(match)
        action = match.group(1).strip()
        print(action)
        action_input = match.group(2)
        print(action_input)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)