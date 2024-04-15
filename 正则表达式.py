# -*- coding: utf-8 -*-
import re

string  ="""
问题: 您想查询中国GDP初步核算数据
想法: 我们可以使用GDP工具来查询中国的GDP初步核算数据
行动: [GDP]
观察:`
"""

pattern = r"行动\s*\d*\s*:(.*?)\观察\s*"

match = re.search(pattern, string, re.DOTALL)
print(match)
action = match.group(1).strip()
print(action)
