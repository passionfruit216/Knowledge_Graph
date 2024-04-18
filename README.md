
# Knowledge_Graph_QA_System

本项目使用LLM 大模型和图数据库进行"智能"询问和添加







## 在本地运行

Clone 这个 project

```bash
  git clone https://github.com/passionfruit216/Knowledge_Graph.git
```

前往项目目录

```bash
  cd 项目目录
```

安装依赖

```bash
  pip install -r requirements.txt
```

运行测试

```bash
streamlit run 1_DBquery.py --server.port 9091
```


## 项目结构参考

- documentations 文件夹存放待处理的文档
- app.py 未来的项目主文件
- Chat_GLM3.py GLM3类
- Chat_GLM4.py GLM4类
- Controller.py 总控制器
- Custom_paser.py 自定义输出解释器
- DataBase.py 数据库相关的操作
- db2LLM.py 根据问题寻找数据库
- requirements.txt 项目依赖文件
- temp.py 临时测试文件
- textSeq.py 文本提取关系
- utils.py 工具箱
- vector_db.py 建读取文件夹内容建立向量化数据库
- vector_db_query.py 向量化数据库询问

## API 参考


- Chat_GLM3, Chat_GLM4 类

| 函数     | 参数           | 描述                              |
| :------- | :------------- | :-------------------------------- |
| `__init__`   | `model_path`  | **必选**. 模型地址                |
| `_call`      | `prompt, stop, run_manager` | **必选**. prompt为提示词模板，stop和run_manager为停止词和回调函数（可选） |
| `_llm_type`  | 无             | 返回模型的类型                     |


- Controller 类

| 函数                  | 参数     | 描述                                       |
| :------------------- | :------- | :----------------------------------------- |
| `__init__`              | `DataBase, LLM` | **必选**. 数据库和模型（必须已经接入langchain） |
| `insert_short_text`   | `text`   | **必选**. 使用用户输入文本创建关系                 |
| `insert_long_text`    | `text`   | 待实现                                     |
| `query`               | `text`   | **必选**. 高效查询数据库的用户输入问题              |


- CustomOutputParser 类

| 函数                | 参数         | 描述                                    |
| :------------------- | :----------- | :-------------------------------------- |
| `__init__`            | `code_type`  | **可选**. 输出的语言类型（暂定为python） |
| `parse`              | `response`   | **必选**. 获取模型输出                      |
| `get_format_instructions` | 无       | 指导模型输出的格式                        |
| `_type`              | 无           | 输出解释器类型                             |





- Data2Neo4j 类

| 函数                | 参数                        | 描述                     |
| :------------------- | :-------------------------- | :----------------------- |
| `__init__`           | `url, username, password`   | **必选**. 数据库连接信息  |
| `create_node`        | `label, name`               | 创建节点                  |
| `create_relation`    | `label, head, tail, relation`| 创建关系                |
| `query`              | `query`                     | 执行查询语句并返回数据    |
| `revise_add_node`    | `label, name, new_property` | 修改节点属性              |
| `delete_all`         | 无                          | 删除所有节点和关系        |
| `print_all`          | 无                          | 打印所有节点和关系        |
| `Precise_queries`    | `label, names`               | 精确查询                 |
| `show_all_label`     | 无                          | 显示所有标签              |
| `show_all_Node`      | 无                          | 显示所有节点名称          |
| `node_is_exist`      | `label, name`               | 检查节点是否存在          |


- inputs2db 类

| 函数             | 参数                  | 描述                         |
| :---------------- | :-------------------- | :--------------------------- |
| `__init__`        | `DataBase, LLM`       | **必选**. 数据库和LLM模型    |
| `Cypher_Summary`  | `query`               | 进行关系三元组总结           |
| `text2Cypher`     | `texts`               | 将用户文本转换为Cypher语句   |


- text2neo4j 类

| 函数            | 参数        | 描述                                     |
| :-------------- | :---------- | :--------------------------------------- |
| `__init__`      | `DataBase, LLM` | **必选**. 数据库和LLM模型               |
| `get_texts`     | `text`      | 提取文本关系并确认主体和主题             |
| `text2db`       | `input`     | 将提取到的关系插入数据库中               |





## 特性

- 支持用户自行输入文本,提取其中的关系,插入关系数据库中
- 支持用户对数据内容进行询问
- 支持展示数据库结构(开发中.....)
- 更多功能尽请期待.....


## 未来展望


- 为项目添加前后端
- 暂时用gradio或streamlit框架展示
- 添加模型记忆功能
- 将模型template存入本地数据库
- 完善app.py
- 加入本地对话缓存,减少模型和用户压力
- balabala....



## FAQ

#### 我该怎么安装图数据库Neo4j?
进入此网址

https://neo4j.com/deployment-center/#enterprise
自行下载 社区版 

注意! 十分推荐下载5.18版本以前的版本

下载完成后,解压缩到任意路径 例如我的路径为

```
C:\neo4j-community-5.18.0\bin
```
将此路径(你自己的)添加到环境变量中

*****


下载JDK-21

https://www.oracle.com/cn/java/technologies/downloads/#jdk21-windows

下载完成后,还是到JDK文件夹 例如:
```
C:\Program Files\Java\jdk-21\bin
```

添加环境变量
*****

打开控制台

输入
```
neo4j.bat console
```
来测试是否开启成功

#### 我该怎么获取我的chatGLM4的apikey?

https://open.bigmodel.cn/usercenter/apikeys

自行注册充值获取


#### 我的Neo4j数据库报错了,提示缺少xxx
大概率缺少APOC 插件

https://blog.csdn.net/zz_dyx/article/details/135172438
查看此教程,自行安装


#### 我在进行生成关系组时,提示解析字典失败

大概率AI抽风,多试几次


####　我下载好了Neo4j数据库,但是我不知道默认的用户名和密码

默认 

User:neo4j

password: neo4j
## 支持

如需支持，请联系QQ: 1589220751


## 附录

langchain官方中文网

https://www.langchain.com.cn/


智谱AI官网

https://open.bigmodel.cn/

