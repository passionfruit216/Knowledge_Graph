# -*- coding: utf-8 -*-
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union, Any
from langchain.tools import Tool
from langchain_core.prompts.base import FormatOutputType




class Custom_Agent_Promptlate(StringPromptTemplate):
    template:str

    tools: List

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        print(intermediate_steps)
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\n观察: {observation}\n"

        print("-----{}".format(thoughts))
        kwargs["agent_scratchpad"] = thoughts

        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)




