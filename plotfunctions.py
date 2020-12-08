import networkx as nx
import pygraphviz as pgv

def plotGraphFromVariantsSimple(variants):
    G = nx.DiGraph()
    for v in variants:
        nx.add_path(G, v[0])

    nodes = G.nodes()

    es = []
    for v in variants:
        Gtemp = nx.DiGraph()
        nx.add_path(Gtemp, v[0], weight=v[1])
        es.append({(e[0],e[1]):e[2]["weight"] for e in Gtemp.edges(data=True)})
    eout = {}
    for ein in es:
        for e in set(list(ein.keys()) + list(eout.keys())):
            if e in ein and e in eout:
                eout[e] = ein[e] + eout[e]
            elif e in ein:
                eout[e] = ein[e]
            elif e in eout:
                eout[e] = eout[e]
    edges = [{"from":edge[0], "to":edge[1], "value":eout[edge]} for edge in eout]
    G = pgv.AGraph(directed=True)
    G.graph_attr.update(rankdir="LR")
    fr = [e["from"] for e in edges]
    to = [e["to"] for e in edges]
    we = [e["value"] for e in edges]
    maxw = max(we)
    minw = min(we)

    we = [(w-minw)/maxw*2.5+0.5 for w in we]
    
    for n in set(fr+to):
        G.add_node(n.replace(" ", ""), label=n, shape="rectangle")

    for f,t,w in zip(fr,to,we):
        G.add_edge(f.replace(" ",""),t.replace(" ",""),penwidth=w)

    G = str(G)
    #for n in set(fr+to):
    #    G = G.replace(n.replace(" ","") + " ->", n.replace(" ","") + ":port ->")
    #    G = G.replace("-> "+ n.replace(" ",""), "-> "+n.replace(" ","") + ":port")
    G = pgv.AGraph(G)
    G.layout(prog='dot')
    #return str(G)
    return G