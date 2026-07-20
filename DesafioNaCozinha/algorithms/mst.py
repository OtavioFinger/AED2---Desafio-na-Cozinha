from structs.uFind import UnionFind
from structs.heap import MinHeap  # Nova importação adicionada

class PlanejamentoLogistico:
    def __init__(self, grafo):
        self.grafo = grafo

    def otimizar_infraestrutura_kruskal(self):
        vertices = self.grafo.obter_vertices()

        uf = UnionFind(vertices)
        
        arestas_unicas = []
        visitadas = set()
        
        for u in vertices:
            for aresta in self.grafo.obter_vizinhos(u):
                v = aresta["destino"]
                peso = aresta["peso"]
                
                id_aresta = tuple(sorted([u, v]))
                if id_aresta not in visitadas:
                    visitadas.add(id_aresta)
                    arestas_unicas.append((peso, u, v))
                    
        arestas_unicas.sort()
        
        mst_conexoes = []
        custo_total = 0
        
        for peso, u, v in arestas_unicas:
            if uf.union(u, v):
                mst_conexoes.append({"origem": u, "destino": v, "custo": peso})
                custo_total += peso
                
        return mst_conexoes, custo_total
    
    def calcular_rota_mais_rapida(self, origem, destino):
        # Inicializa as distâncias para todos os vértices como infinito
        distancias = {v: float('inf') for v in self.grafo.obter_vertices()}
        distancias[origem] = 0
        
        anteriores = {v: None for v in self.grafo.obter_vertices()}
        
        heap = MinHeap()
        # O heap armazena (prioridade, item) -> (tempo_acumulado, vertice_atual)
        heap.push(0, origem)
        
        visitados = set()

        while not heap.is_empty():
            distancia_atual, atual = heap.pop()
            
            if atual in visitados:
                continue
                
            visitados.add(atual)

            if atual == destino:
                break

            # Explora os vizinhos
            for aresta in self.grafo.obter_vizinhos(atual):
                vizinho = aresta["destino"]
                peso_tempo = aresta["peso"] # minutos de viagem
                
                if vizinho in visitados:
                    continue

                nova_distancia = distancia_atual + peso_tempo
                
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
                    heap.push(nova_distancia, vizinho)

        caminho = []
        passo_atual = destino
        
        while passo_atual is not None:
            caminho.append(passo_atual)
            passo_atual = anteriores[passo_atual]
            
        caminho.reverse()
        
        if len(caminho) == 1 and origem != destino:
            return float('inf'), []
            
        return distancias[destino], caminho
    
    def calcular_capacidade_maxima(self, origem, destino):
        residual = {}
        for u in self.grafo.obter_vertices():
            for aresta in self.grafo.obter_vizinhos(u):
                v = aresta["destino"]
                cap = aresta.get("capacidade", 0) 
                residual[(u, v)] = cap
                
                if (v, u) not in residual:
                    residual[(v, u)] = 0

        fluxo_maximo = 0

        def bfs_caminho_aumentante():
            visitados = set([origem])
            fila = [origem]
            caminho = {origem: None}
            i = 0
            
            while i < len(fila):
                atual = fila[i]
                i += 1
                
                for v in self.grafo.obter_vertices():
                    if (atual, v) in residual and residual[(atual, v)] > 0 and v not in visitados:
                        visitados.add(v)
                        caminho[v] = atual
                        fila.append(v)
                        
                        if v == destino:
                            return caminho
            return None

        while True:
            caminho = bfs_caminho_aumentante()
            if not caminho:
                break  
            
            fluxo_caminho = float('inf')
            atual = destino
            while atual != origem:
                anterior = caminho[atual]
                fluxo_caminho = min(fluxo_caminho, residual[(anterior, atual)])
                atual = anterior
                
            atual = destino
            while atual != origem:
                anterior = caminho[atual]
                residual[(anterior, atual)] -= fluxo_caminho
                residual[(atual, anterior)] += fluxo_caminho
                atual = anterior
                
            fluxo_maximo += fluxo_caminho

        visitados_finais = set([origem])
        fila = [origem]
        i = 0
        while i < len(fila):
            atual = fila[i]
            i += 1
            for v in self.grafo.obter_vertices():
                if (atual, v) in residual and residual[(atual, v)] > 0 and v not in visitados_finais:
                    visitados_finais.add(v)
                    fila.append(v)

        gargalos = []
        for u in self.grafo.obter_vertices():
            for aresta in self.grafo.obter_vizinhos(u):
                v = aresta["destino"]
                if u in visitados_finais and v not in visitados_finais:
                    gargalos.append({"de": u, "para": v})

        return fluxo_maximo, gargalos