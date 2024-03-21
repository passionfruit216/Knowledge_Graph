# -*- coding: utf-8 -*-

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gradio as gr
import tqdm
# ********************** 暂时弃用 ***************************
def load_model():
    print("开始加载model")
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    print("完成模型的加载")
    return tokenizer, model



