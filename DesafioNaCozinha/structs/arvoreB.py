import pickle
import os


class NodoB:

    contadorIds = 0

    def __init__(self, folha=True):

        self.idBloco = NodoB.contadorIds
        NodoB.contadorIds += 1

        self.folha = folha
        self.chaves = []
        self.filhos = []


class ArvoreB:

    def __init__(self):

        self.raiz = NodoB()
        self.maxChaves = 3
        self.blocos = {}
        self.idRaiz = self.raiz.idBloco

    def resumoReceita(self, receita):

        return (
            f"{receita.id}"
            f"{receita.nome}"
            f"{receita.categoria}"
            f"{receita.ingredientes}"
            f"{receita.tempo}"
            f"{receita.custo}"
            f"{receita.dificuldade}"
            f"{receita.avaliacao}"
            f"{receita.popularidade}"
        )

    def inserir(self, receita):

        if self.buscarMemoria(self.raiz, receita.id) is not None:
            return

        raiz = self.raiz

        if len(raiz.chaves) == self.maxChaves:

            novaRaiz = NodoB(False)

            novaRaiz.filhos.append(raiz)

            self.dividirFilho(novaRaiz, 0)

            self.raiz = novaRaiz
            self.idRaiz = novaRaiz.idBloco

            self.inserirNaoCheio(novaRaiz, receita)

        else:

            self.inserirNaoCheio(raiz, receita)

    def inserirNaoCheio(self, nodo, receita):

        i = len(nodo.chaves) - 1

        if nodo.folha:

            nodo.chaves.append(None)

            while i >= 0 and receita.id < nodo.chaves[i].id:

                nodo.chaves[i + 1] = nodo.chaves[i]
                i -= 1

            nodo.chaves[i + 1] = receita

        else:

            while i >= 0 and receita.id < nodo.chaves[i].id:
                i -= 1

            i += 1

            if len(nodo.filhos[i].chaves) == self.maxChaves:

                self.dividirFilho(nodo, i)

                if receita.id > nodo.chaves[i].id:
                    i += 1

            self.inserirNaoCheio(nodo.filhos[i], receita)

    def dividirFilho(self, pai, indice):

        cheio = pai.filhos[indice]

        novo = NodoB(cheio.folha)

        meio = len(cheio.chaves) // 2

        chaveMeio = cheio.chaves[meio]

        novo.chaves = cheio.chaves[meio + 1:]
        cheio.chaves = cheio.chaves[:meio]

        if not cheio.folha:

            novo.filhos = cheio.filhos[meio + 1:]
            cheio.filhos = cheio.filhos[:meio + 1]

        pai.filhos.insert(indice + 1, novo)
        pai.chaves.insert(indice, chaveMeio)

    def buscarMemoria(self, nodo, idReceita):

        i = 0

        while i < len(nodo.chaves) and idReceita > nodo.chaves[i].id:
            i += 1

        if i < len(nodo.chaves) and idReceita == nodo.chaves[i].id:
            return nodo.chaves[i]

        if nodo.folha:
            return None

        return self.buscarMemoria(nodo.filhos[i], idReceita)

    def salvarNodo(self, nodo, arquivo):

        dados = {
            "idBloco": nodo.idBloco,
            "folha": nodo.folha,
            "chaves": nodo.chaves,
            "filhos": [filho.idBloco for filho in nodo.filhos]
        }

        pickle.dump(dados, arquivo)

        for filho in nodo.filhos:
            self.salvarNodo(filho, arquivo)

    # Função para salvar a árvore inteira em um arquivo .dat no disco
    # Simula a persistência em memória secundária
    def salvarEmDisco(self, caminho="arvore.dat"):

        with open(caminho, "wb") as arquivo:

            metadata = {
                "raiz": self.idRaiz
            }

            pickle.dump(metadata, arquivo)

            self.salvarNodo(self.raiz, arquivo)

        print(f"Arvore salva em disco: {caminho}")

    def carregarBlocos(self, caminho):

        blocos = {}

        with open(caminho, "rb") as arquivo:

            metadata = pickle.load(arquivo)

            self.idRaiz = metadata["raiz"]

            while True:

                try:

                    dados = pickle.load(arquivo)

                    blocos[dados["idBloco"]] = dados

                except EOFError:
                    break

        return blocos

    # Função para carregar a árvore do disco sem precisar reinserir as receitas
    # Simula a leitura de blocos de disco
    def carregarDoDisco(self, caminho="arvore.dat"):

        if not os.path.exists(caminho):
            print(f"Arquivo {caminho} nao encontrado.")
            return False

        self.blocos = self.carregarBlocos(caminho)

        print(f"Arvore carregada do disco: {caminho}")

        return True

    def carregarNodo(self, idBloco):

        dados = self.blocos[idBloco]

        nodo = NodoB(dados["folha"])

        nodo.idBloco = dados["idBloco"]
        nodo.chaves = dados["chaves"]
        nodo.filhos = dados["filhos"]

        return nodo

    def buscar(self, idReceita):

        return self.buscarDisco(self.idRaiz, idReceita)

    def buscarDisco(self, idBloco, idReceita):

        nodo = self.carregarNodo(idBloco)

        i = 0

        while i < len(nodo.chaves) and idReceita > nodo.chaves[i].id:
            i += 1

        if i < len(nodo.chaves) and idReceita == nodo.chaves[i].id:

            print(f"[DISCO] Bloco {nodo.idBloco} acessado")

            return nodo.chaves[i]

        if nodo.folha:
            return None

        print(f"[DISCO] Navegando para bloco filho")

        return self.buscarDisco(nodo.filhos[i], idReceita)

    def modoInvestigacao(self, receitas):

        duplicatas = []
        alteradas = []

        ids = set()

        for receita in receitas:

            if receita.id in ids:
                duplicatas.append(receita)

            else:
                ids.add(receita.id)

            receitaArvore = self.buscarMemoria(self.raiz, receita.id)

            if receitaArvore is not None:

                resumoAtual = self.resumoReceita(receita)
                resumoOriginal = self.resumoReceita(receitaArvore)

                if resumoAtual != resumoOriginal:
                    alteradas.append(receita)

        return duplicatas, alteradas