# -*- coding: utf-8 -*-
import math
import torch

#　＊＊＊＊＊＊＊＊＊＊＊＊　弃用　＊＊＊＊＊＊＊＊＊＊＊＊＊
#　参见官方文档
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets




def from_text2kb(text,tokenizer, model,span_length =50,verbose = True):
    # 对整个字符串进行编码
    model_inputs = tokenizer(text, return_tensors = 'pt',max_length=256, padding=True)
    # 计算token
    num_tokens = len(model_inputs["input_ids"][0])

    gen_kwargs = {
        "max_length": 2048,
        "length_penalty": 0,
        "num_beams": 3,
        "num_return_sequences": 3,
    }

    if verbose:
        print(f"输入了{num_tokens}个token")

    num_spans = math.ceil(num_tokens / span_length)

    if verbose:
        print(f"分成了{num_spans}个文本块")

    # Generate
    generated_tokens = model.generate(
        model_inputs["input_ids"].to(model.device),
        attention_mask=model_inputs["attention_mask"].to(model.device),
        **gen_kwargs,
    )

    # 提取文本
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)


    # 提取三元组
    for idx, sentence in enumerate(decoded_preds):
        print(f'Prediction triplets sentence {idx}')
        print(extract_triplets(sentence))
