from langchain_core.outputs import ChatGenerationChunk
from zhipuai import ZhipuAI
import json
import time
from langchain.llms.base import LLM
from typing import Optional, List, Any, Mapping, Iterator
from langchain.schema.output import GenerationChunk  # 用于流式传输
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models import openai
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages.ai import AIMessageChunk
from typing import Dict
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
              stop: Optional[List[str]] =None
              ):
        if history is None:
            history = []
         # 常规调用
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8192,
            temperature=0.95,
            top_p=0.7,
            stop = stop
        )
        result = response.choices[0].message.content
        return result

    def sse_invoke(self, prompt: str, history=[]):
        if history is None:
            history = []

        history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=history,
            stream=True,
        )
        return response

    def _stream(  # type: ignore[override]
            self,
            prompt: List[Dict[str, str]],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the chat response in chunks."""
        response = self.sse_invoke(prompt)

        for chunk in response:
            if chunk.choices[0].delta:
                delta = chunk.choices[0].delta.content

                chunk = ChatGenerationChunk(message=AIMessageChunk(content=delta))
                if run_manager:
                    run_manager.on_llm_new_token(delta, chunk=chunk)
                yield chunk

"""
  for r in response.events():
            if r.event == "add":
                delta = r.data
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=delta))
                if run_manager:
                    run_manager.on_llm_new_token(delta, chunk=chunk)
                yield chunk

            elif r.event == "error":
                raise ValueError(f"Error from ZhipuAI API response: {r.data}")
"""

# 后续实现工具调用?