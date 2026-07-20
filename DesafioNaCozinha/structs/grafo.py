class Grafo:
    def __init__(self, dirigido=False):
        self.adjacencias = {}
        self.dirigido = dirigido

    def adicionar_vertice(self, v):
        if v not in self.adjacencias:
            self.adjacencias[v] = []

    def adicionar_aresta(self, u, v, peso=1, dados_extras=None):
        #u: Vértice de origem
        #v: Vértice de destino
        #peso: Custo, distância ou peso da aresta (padrão é 1)
        #dados_extras: Dicionário com informações adicionais (ex: capacidade para fluxo)
        
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        aresta_ida = {"destino": v, "peso": peso}
        if dados_extras:
            aresta_ida.update(dados_extras)
            
        self.adjacencias[u].append(aresta_ida)

        # Se não for dirigido, cria a aresta de volta automaticamente
        if not self.dirigido:
            aresta_volta = {"destino": u, "peso": peso}
            if dados_extras:
                aresta_volta.update(dados_extras)
            self.adjacencias[v].append(aresta_volta)

    def obter_vizinhos(self, u):
        return self.adjacencias.get(u, [])

    def obter_vertices(self):
        #Retorna uma lista com todos os vértices do grafo
        return list(self.adjacencias.keys())

    def grau_entrada(self):
        #Calcula o grau de entrada de todos os vértices.
        grau = {v: 0 for v in self.adjacencias}
        for u in self.adjacencias:
            for aresta in self.adjacencias[u]:
                v = aresta["destino"]
                grau[v] += 1
        return grau