# -*- coding: utf-8 -*-
from DataBase import Data2Neo4j

url ="neo4j://localhost:7687"
username ="neo4j"
password ="12345678"
db = Data2Neo4j(url,username,password)
db.show_label_name("疾病","头痛")