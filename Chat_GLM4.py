from zhipuai import ZhipuAI
import json
import time
from langchain.llms.base import LLM
from typing import Optional, List, Any, Mapping, Iterator
from langchain.schema.output import GenerationChunk  # 用于流式传输
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models import openai

class chat_glm4(LLM):
    # 模型的各个参数
    max_token: int = 8192
    do_sample: bool = True
    temperature: float = 0.0   # 0.5
    top_p = 0.7
    tokenizer: object = None
    model: object = None
    history: List = []
    tool_names: List = []
    has_search: bool = False
    client: object = None  # 额外实现这个
    @property
    def _llm_type(self) -> str:
        return "ChatGLM4"

    def __init__(self, zhipuai_api_key):
        super().__init__()
        self.client = ZhipuAI(api_key=zhipuai_api_key)

# 重载call函数
    def _call(self, prompt: str,
              history: List = [],
              stop: Optional[List[str]] = None
              ):
        if history is None:
            history = []
         # 常规调用
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8192,

        )
        result = response.choices[0].message.content
        return result

#　流式传输(算一个字输出一个字)
    def _stream(self, prompt: str, history: List = None)-> Iterator[GenerationChunk]:
        if history is None:
            history = []
         # 常规调用
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        print(type(response))
        for chunk in response:
            print(chunk.choices[0].delta)


# 后续实现工具调用?