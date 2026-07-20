from collections import defaultdict


class ComunidadesGastronomicas:

    def __init__(self, receitas):
        self.receitas = receitas
        self.grafo = defaultdict(list)

    def construir_grafo(self):
        """
        Liga duas receitas caso compartilhem
        pelo menos um ingrediente.
        """

        n = len(self.receitas)

        for i in range(n):
            for j in range(i + 1, n):

                ingredientes1 = {
                    ingrediente.lower()
                    for ingrediente in self.receitas[i].ingredientes
                }

                ingredientes2 = {
                    ingrediente.lower()
                    for ingrediente in self.receitas[j].ingredientes
                }

                if ingredientes1.intersection(ingredientes2):

                    id1 = self.receitas[i].id
                    id2 = self.receitas[j].id

                    self.grafo[id1].append(id2)
                    self.grafo[id2].append(id1)

    def dfs(self, vertice, visitados, componente):

        visitados.add(vertice)
        componente.append(vertice)

        for vizinho in self.grafo[vertice]:
            if vizinho not in visitados:
                self.dfs(vizinho, visitados, componente)

    def encontrar_comunidades(self):

        self.construir_grafo()

        visitados = set()
        comunidades = []

        for receita in self.receitas:

            if receita.id not in visitados:

                componente = []

                self.dfs(
                    receita.id,
                    visitados,
                    componente
                )

                comunidades.append(componente)

        return comunidades

    def imprimir(self):

        comunidades = self.encontrar_comunidades()

        mapa = {
            r.id: r.nome
            for r in self.receitas
        }

        print("\n======= COMUNIDADES GASTRONÔMICAS =======\n")

        for i, comunidade in enumerate(comunidades, start=1):

            print(f"Comunidade {i}")

            for receita in comunidade:
                print(f" - {mapa[receita]}")

            print()