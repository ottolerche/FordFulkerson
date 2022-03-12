from sys import stdin
from sys import stdout

class DirectedEdge:
    def __init__(self, f, t, cap, flow):
        self.f = f
        self.t = t
        self.cap = cap
        self.flow = 0

class EdgeWeightedDigraph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[0 for x in range(0)] for y in range(V)]

    def addEdge(self, e):
        self.adj[e.f].append(e)
        self.E = self.E + 1

class DepthFirstPaths:
    def __init__(self, G, s):
        self.marked = [False for x in range(G.V)]
        self.edgeTo = [None for x in range(G.V)]
        self.s = s
        self.dfs(G, s)

    def dfs(self, G, v):
        self.marked[v] = True
        for w in G.adj[v]:
            if self.marked[w.t] is not True and w.cap > 0:
                self.edgeTo[w.t] = w
                self.dfs(G, w.t)

    def hasPathTo(self, v):
        return self.marked[v]

    def pathTo(self, v):
        if self.hasPathTo(v) is False:
            return None
        path = []
        while v is not self.s:
            path.append(self.edgeTo[v])
            v = self.edgeTo[v].f
        return path

def hasParralel(e, adj):
    for i, v in enumerate(adj):
        if e.f is v.t and e.t is v.f:
            return i
    return False

line = [int(x) for x in stdin.readline().split()]
n = line[0] #nodes
m = line[1] #edges
s = line[2] #source
t = line[3] #sink

G = EdgeWeightedDigraph(n)

for i in range(m):
    line = [int(x) for x in stdin.readline().split()]
    f = line[0]
    t = line[1]
    c = line[2]
    e = DirectedEdge(f, t, c, 0)
    G.addEdge(e)

search = DepthFirstPaths(G, s)
path = search.pathTo(t)

while path is not None:
    bottleneck = 1000
    for v in path:
        bottleneck = min(bottleneck, v.cap)

    residualG = G

    for v in path:
        # print(v.f, v.t, v.cap)
        for i, e in enumerate(residualG.adj[v.f]):
            if e is v:
                # newEdge = DirectedEdge(residualG.adj[v.f][i].t, residualG.adj[v.f][i].f, bottleneck, 0)
                newEdge = DirectedEdge(v.t, v.f, bottleneck, 0)
                parallel = hasParralel(v, residualG.adj[v.f])

                residualG.adj[v.f][i].cap = residualG.adj[v.f][i].cap - bottleneck
                residualG.adj[v.f][i].flow = residualG.adj[v.f][i].flow + bottleneck

                if parallel is False:
                    residualG.addEdge(newEdge)
                if parallel is True:
                    residualG.adj[v.t][parallel].cap = residualG.adj[v.t][parallel].cap + bottleneck
                    residualG.adj[v.t][parallel].flow = residualG.adj[v.t][parallel].flow - bottleneck

    search = DepthFirstPaths(residualG, s)
    path = search.pathTo(t)

maxflow = 0
for e in residualG.adj[t]:
    maxflow = maxflow + e.cap

edges = []
for v in range(n):
    for e in residualG.adj[v]:
        if e.flow > 0:
            edges.append(e)

print (n, maxflow, len(edges))
for e in edges:
    print(e.f, e.t, e.flow)

# print(bottleneck)
# Lav digraph med capacity
# find path s t
# skub flow
# byg residual
