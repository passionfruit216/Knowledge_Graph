# -*- coding: utf-8 -*-
import re

# 输入文本
text = "思考: 我需要查找高启强扮演者的信息。<|assistant|>搜索工具\n操作: [['搜索工具']]\n操作输入: 高启强 扮演者"

# 正则表达式模式
pattern = r"<\|assistant\|>搜索工具\n操作: \[\['(.*?)'\]\]\n操作输入: (.*?)$"

# 使用正则表达式匹配文本
matches = re.search(pattern, text, re.MULTILINE)

# 输出匹配结果
if matches:
    print(matches.group(1))  # 输出 "搜索工具"
    print(matches.group(2))  # 输出 "高启强 扮演者"
