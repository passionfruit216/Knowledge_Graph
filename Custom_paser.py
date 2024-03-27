# -*- coding: utf-8 -*-
import re
from typing import Any, Literal
from langchain.schema import BaseOutputParser, OutputParserException
import ast

format = """输出以python字典的格式输出.其中包含三个键,一个是唯一主体,一个是关系三元组,一个是主题,格式如下:\n
        主题: 根据用户文本内容确定的主题\n
        唯一主体: 根据用户文本内容确定的唯一主体\n
        关系: 根据用户文本内容提取的关系三元组\n
        """
class CustomOutputParser(BaseOutputParser[str]):
    code_type: str = None

    def __init__(self,code_type:Literal["python"] = "python"):
        super().__init__()
        # self.format_instructions =format
        self.code_type = code_type

    def parse(self, response: str) -> str:
        pattern = r"\{([^}]+)\}"
        match = re.search(pattern, response)
        if match:
            dict_content = "{" + match.group(1) + "}"
            try:
                result = eval(dict_content)  # 使用eval函数将字符串转换为字典
                return result
            except Exception as e:
                raise OutputParserException(f"解析字典失败: {e}")
        else:
            OutputParserException("The response has no code block.", llm_output=response)

    def get_format_instructions(self) -> str:
        return format

    @property
    def _type(self) -> str:
        """返回该解析器的类型 这里返回的是自定义代码块解析器"""
        return "CustomOutputParser"