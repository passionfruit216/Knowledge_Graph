# -*- coding: utf-8 -*-
# 完成数据库的查询 以及返回结果
from py2neo import Graph, Node, Relationship, NodeMatcher
from pyvis.network import Network

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

    def show_all_relation(self):
        query = """
        MATCH (n1)-[r]->(n2)
        RETURN n1, TYPE(r) AS relationship, n2
        """
        result = self.query(query)
        # 将查询结果转换为字典列表
        relationships_list = []
        for record in result:
            relationship_dict = {
                "node1": record["n1"],
                "relationship": record["relationship"],
                "node2": record["n2"]
            }
            relationships_list.append(relationship_dict)
        return relationships_list
    def node_is_exist(self, label, name):
        result = self.query(
            f"MATCH (n:{label} {{name: '{name}'}})RETURN COUNT(n) > 0 as nodeExists")
        res = result[0]["nodeExists"]
        return res


    def save_as_Html(self,file_name):
        # 创建网络

        net = Network(directed=True, width="1920px", height="1080px", cdn_resources="in_line")
        # 节点
        color_entity = "#00FF00"
        # 添加节点和关系
        nodes = self.show_all_Node()
        for e in nodes:
            net.add_node(e, shape="circle", color=color_entity,labelHighlightBold=True)

        relationships = self.show_all_relation()
        for r in relationships:
            net.add_edge(r["node1"]["name"], r["node2"]["name"],
                        title=r["relationship"], label=r["relationship"])

            # save network
        net.repulsion(
            node_distance=200,
            central_gravity=0.2,
            spring_length=200,
            spring_strength=0.05,
            damping=0.09
        )

        net.show_buttons(filter_=['physics'])
        net.set_edge_smooth(smooth_type='dynamic')
        # net.save_graph("./networks/" + file_name)
        net.show('./networks/' + file_name, notebook=False)


    def create_temp_html(self,relations:dict, file_name:str="temp.html"):
        net = Network(directed=True, width="1920px", height="1080px", cdn_resources="in_line")
        # 节点
        color_entity = "#00FF00"
        # 添加节点和关系
        for e in relations["关系"]:
            net.add_node(e[0], shape="circle", color=color_entity,labelHighlightBold=True)
            net.add_node(e[2], shape="circle", color=color_entity,labelHighlightBold=True)
            net.add_edge(e[0],e[2],title=e[1],label=e[1])

        net.repulsion(
            node_distance=200,
            central_gravity=0.2,
            spring_length=200,
            spring_strength=0.05,
            damping=0.09
        )
        net.show_buttons(filter_=['physics'])
        net.set_edge_smooth(smooth_type='dynamic')
        net.show('./networks/{}'.format(file_name), notebook=False)