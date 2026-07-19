class UnionFind:
    def __init__(self, vertices):
        self.pai = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, v):
        if self.pai[v] != v:
            self.pai[v] = self.find(self.pai[v])
        return self.pai[v]

    def union(self, u, v):
        raiz_u = self.find(u)
        raiz_v = self.find(v)

        if raiz_u == raiz_v:
            return False

        if self.rank[raiz_u] > self.rank[raiz_v]:
            self.pai[raiz_v] = raiz_u
        elif self.rank[raiz_u] < self.rank[raiz_v]:
            self.pai[raiz_u] = raiz_v
        else:
            self.pai[raiz_v] = raiz_u
            self.rank[raiz_u] += 1

        return True