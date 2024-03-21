# -*- coding: utf-8 -*-
from DataBase import *

db=Data2Neo4j(url="neo4j://localhost:7687",username="neo4j",password="12345678")
db.delete_all()
db.create_node(label="Person",name="ljc")
db.create_node(label="Person",name="ljc2")
db.create_relation(label="Person",head="ljc",tail="ljc2",relation="friend")
db.query("match (n) return n")
db.revise_add_node(label="Person",name="ljc",new_property="ljc3")
# # 定义要查询的属性和属性值
# property_key = "name"
# property_value = "ljc3"
# result=db.query(f"MATCH (n) WHERE n.{property_key} = '{property_value}' RETURN n")
# for i in result:
#     print(i)
db.print_all()
