# -*- coding: utf-8 -*-

from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import UnstructuredImageLoader
from langchain_community.vectorstores import Neo4jVector
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
import os
from tqdm import tqdm
import gradio as gr


os.environ["OPENAI_API_KEY"] = "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"
os.environ["http_proxy"] = "http://127.0.0.1:9421"
os.environ["https_proxy"] = "http://127.0.0.1:9421"
def get_files(file_path):
    print(type(file_path))
    print(file_path)
    file_list = []

    for root, dirs, files in os.walk(file_path):
        for file in files:
            # 判断 文件是否符合标准
            if file.endswith('.txt'):
                file_list.append(os.path.join(root, file))
            elif file.endswith('.md'):
                file_list.append(os.path.join(root, file))
            elif file.endswith('.pdf'):
                file_list.append(os.path.join(root, file))
            elif file.endswith('.jpg'):  # 添加图片 待测试功能
                file_list.append(os.path.join(root, file))

    return file_list


# 使用 langchain完成 文件文字内容提取
def get_text(file_path):
    # 调用定义的函数得到目标文件路径列表

    file_list = get_files(file_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    for file in tqdm(file_list):
        file_type = file.split('.')[-1]
        if file_type == 'md':
            loader = UnstructuredMarkdownLoader(file)
        elif file_type == 'txt':
            loader = UnstructuredFileLoader(file)
        elif file_type == 'pdf':
            loader = UnstructuredPDFLoader(file)
        elif file_type == 'jpg':
            loader = UnstructuredImageLoader(file)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs.extend(loader.load())
    return docs

def process(file_path="documentations"):
    try:
        files_loader = get_text(file_path)

        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)

        docs = text_splitter.split_documents(files_loader)

        embeddings = OpenAIEmbeddings()

        db = Neo4jVector.from_documents(docs, embeddings, url="neo4j://localhost:7687", username="neo4j",
                                        password="12345678")

        return "文档已经成功加载到数据库中"

    except Exception as e:
        return e


with gr.Blocks() as app:
    gr.Markdown(
        """提醒: <br>
    <b>1.本功能暂时未完善，请将所要添加的文档事先放到本项目documentations的文件夹内(输入别的文件夹也可以)<b><br>
    <b>2.非常建议使用相对路径<b><br>
    <b>3.支持添加PDF,TXT,MARKDOWN,HTML格式文档<b><br>
    """
    )
    inp = gr.Textbox(placeholder="请输入文件路径", label='文件路径',info="文件夹里面支持的文件都会被添加到数据库中")
    out = gr.Textbox(label='运行结果')
    button = gr.Button("提交")
    button.click(fn=process, inputs=inp, outputs=out)

app.launch(share=True)