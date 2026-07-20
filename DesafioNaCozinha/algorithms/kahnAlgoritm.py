class OficinaProducao:
    def __init__(self, grafo):
        self.grafo = grafo

    def ordenacao_topologica(self):
        grau_entrada = self.grafo.grau_entrada()
        
        # Inicializa a fila com os vértices que não têm dependências
        fila = [v for v in grau_entrada if grau_entrada[v] == 0]
        ordem = []
        i = 0  # Ponteiro que simula a remoção no início da fila

        while i < len(fila):
            atual = fila[i]
            i += 1  
            ordem.append(atual)

            for aresta in self.grafo.obter_vizinhos(atual):
                vizinho = aresta["destino"]
                grau_entrada[vizinho] -= 1
                
                if grau_entrada[vizinho] == 0:
                    fila.append(vizinho)

        tem_ciclo = len(ordem) != len(self.grafo.obter_vertices())
        
        return ordem, tem_ciclo

    def buscar_pre_requisitos(self, receita_alvo):
        grafo_reverso = {v: [] for v in self.grafo.obter_vertices()}
        for u in self.grafo.obter_vertices():
            for aresta in self.grafo.obter_vizinhos(u):
                grafo_reverso[aresta["destino"]].append(u)

        if receita_alvo not in grafo_reverso:
            return []

        visitados = set([receita_alvo])
        fila = [receita_alvo]
        pre_requisitos = []
        i = 0

        while i < len(fila):
            atual = fila[i]
            i += 1
            
            for vizinho in grafo_reverso[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
                    pre_requisitos.append(vizinho)

        return pre_requisitos