import networkx as nx

def build_graph(data):
    G = nx.Graph()
    for item in data:
        question = item["question"]
        answer = item["answer"]
        G.add_node(question, type="question")
        G.add_node(answer, type="answer")
        G.add_edge(question, answer, relation="answers")
    nx.write_gpickle(G, "../data/graph/mosdac_kg.gpickle")

