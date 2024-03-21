# -*- coding: utf-8 -*-
import re
text ="""
根据提供的内容，我们可以提取以下实体和关系三元组：

实体1: 感冒
实体2: 普通感冒/伤风/急性鼻炎/上呼吸道感染
关系: 同义词

实体1: 感冒
实体2: 急性上呼吸道病毒性感染性疾病
关系: 定义

实体1: 感冒
实体2: 鼻病毒/副流感病毒/呼吸道合胞病毒/埃可病毒/柯萨奇病毒/冠状病毒/腺病毒
关系: 引起原因

实体1: 感冒
实体2: 鼻塞/喷嚏/流涕/发热/咳嗽/头痛
关系: 临床表现

实体1: 感冒
实体2: 自限性
关系: 疾病特点

实体1: 感冒
实体2: 冬、春季节
关系: 多发季节

以下是以上实体的关系三元组，以Python字典格式表示：

```python
[
    {'head': '感冒', 'relation': '同义词', 'tail': '普通感冒'},
    {'head': '感冒', 'relation': '同义词', 'tail': '伤风'},
    {'head': '感冒', 'relation': '同义词', 'tail': '急性鼻炎'},
    {'head': '感冒', 'relation': '同义词', 'tail': '上呼吸道感染'},
    {'head': '感冒', 'relation': '定义', 'tail': '急性上呼吸道病毒性感染性疾病'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '鼻病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '副流感病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '呼吸道合胞病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '埃可病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '柯萨奇病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '冠状病毒'},
    {'head': '感冒', 'relation': '引起原因', 'tail': '腺病毒'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '鼻塞'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '喷嚏'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '流涕'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '发热'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '咳嗽'},
    {'head': '感冒', 'relation': '临床表现', 'tail': '头痛'},
    {'head': '感冒', 'relation': '疾病特点', 'tail': '自限性'},
    {'head': '感冒', 'relation': '多发季节', 'tail': '冬、春季节'}
]
```

请注意，上述三元组是基于提供信息的概括和假设，实际的实体和关系取决于具体上下文和专业领域知识。
"""
print(text.find('['))
print(text.find(']'))
t=text.split('[')[1].split(']')[0]
print(t)
pattern = r"\{'head': '(.*?)', 'relation': '(.*?)', 'tail': '(.*?)'\}"

matches = re.findall(pattern, t)

for match in matches:
    print("Head:", match[0])
    print("Relation:", match[1])
    print("Tail:", match[2])
    print()