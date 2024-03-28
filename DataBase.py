# -*- coding: utf-8 -*-
# 完成数据库的查询 以及返回结果
from py2neo import Graph, Node, Relationship, NodeMatcher

# 数据库操作类
class Data2Neo4j:
    def __init__(self, url, username, password):
        self.graph = Graph(url, user=username, password=password)
        self.matcher = NodeMatcher(self.graph)
        print("*********数据库连接成功***********")

    def create_node(self, label, name):
        node = Node(label, name=name)
        self.graph.create(node)

    def create_relation(self, label, head, tail, relation):
        try:
            head_node = self.matcher.match(label, name=head).first()
            tail_node = self.matcher.match(label, name=tail).first()
            self.graph.create(Relationship(head_node, relation, tail_node))
        except BaseException:
            raise Exception("Node not found")

    def query(self, query):
        return self.graph.run(query).data()

    def revise_add_node(self, label, name, new_property):
        node = self.matcher.match(label, name=name).first()
        node["name"] = new_property
        self.graph.push(node)

    def delete_all(self):
        self.graph.delete_all()

    def print_all(self):
        result = self.query("MATCH (n) RETURN n")

        for i in result:
            print(i)

    def Precise_queries(self, label, names):
        query = f"MATCH (disease:{label}{{name:'{names}'}})-[r]-(related) RETURN disease, r, related"
        result = self.query(query)
        for i in result:
            print(i)

        return query,result

    def show_all_label(self):
        result = self.query(f"CALL db.labels()")
        res = []
        for i in result:
            res.append(i["label"])
        return res

    def show_all_Node(self):
        result = self.query(f"MATCH (n) RETURN n.name")
        res = set()
        for i in result:
            if i["n.name"] is None:
                continue
            res.add(i["n.name"])
        return res

    def node_is_exist(self, label, name):
        result = self.query(
            f"MATCH (n:{label} {{name: '{name}'}})RETURN COUNT(n) > 0 as nodeExists")
        res = result[0]["nodeExists"]
        return res
