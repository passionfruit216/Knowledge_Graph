# -*- coding: utf-8 -*-
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.utilities import SerpAPIWrapper
import os
from langchain.tools import BaseTool
os.environ["SERPAPI_API_KEY"]="c77aa41c55a1ece06909530ccfbe99a6fb2242bded10bb4b7cac7aad6ebc600d"
class BasicSearchTool(BaseTool):
    llm: BaseLanguageModel
    base_template = """
     请根据下面带```分隔符的文本来回答问题。
    如果该文本中没有相关内容可以回答问题，请直接回复：“抱歉，该问题需要更多上下文信息。”
    ```{text}```
    问题:{query}
    """
    name= "Serach"
    description = "基于搜索引擎的搜索工具,当您需要在互联网上搜索信息时很有用"
    prompt = PromptTemplate.from_template(base_template)
    llm_chain: LLMChain = None

    # 生成基于知识的回答
    def _run(self, query) -> str:
        self.get_llm_chain()
        serach = SerpAPIWrapper()
        context =serach.run(query)
        print("调用工具生成的文本:{}".format(context))
        # print(context)
        resp = self.llm_chain.predict(text=context, query=query)
        # print(resp)
        return resp

    def get_llm_chain(self):
        if not self.llm_chain:
            self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
