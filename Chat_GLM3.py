# -*- coding: utf-8 -*-
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModel

class Chat_GLM3(LLM):
    # 基于本地 InternLM 自定义 LLM 类
    # 声明分词器和模型
    max_token: int = 8192
    do_sample: bool = True
    temperature: float = 0.0  # 0.5
    top_p = 0.7
    tokenizer: AutoTokenizer = None
    model: AutoModel = None

    def __init__(self, model_path="THUDM/chatglm3-6b"):
        super().__init__()
        print("正在加载模型")
        # 加载分词器和模型
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True, local_files_only=True
        )
        # 注意 4bit量化仅供测试 服务器部署可以改成 fp16
        self.model = (
            AutoModel.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
            .quantize(4)
            .cuda()
        )
        self.model = self.model.eval()
        print("完成模型的加载")

    # 重载 _call 函数

    def _call(
        self,
        prompt: str,
        history: List = [],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ):
        if history is None:
            history = []
        # 重写调用函数
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        return response

    @property
    def _llm_type(self) -> str:
        return "ChatGLM3-6B"
