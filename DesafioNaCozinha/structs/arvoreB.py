# Opção C: Árvores B e Simulação de Memória Secundária (I/O)

#     Público-alvo: Duplas que indicaram ter maior dificuldade nas regras estruturais de divisão (split), 
# fusão ou na motivação de hardware das Árvores B.
#     O Desafio: A Árvore B de vocês não pode viver apenas na memória RAM. 
# Vocês deverão implementar uma rotina de persistência em disco via arquivo binário (.dat ou .bin). 
#     O código deve simular que cada nó da árvore B é uma página/bloco de disco físico. O sistema deve ser 
# capaz de salvar a estrutura em disco e carregá-la sob demanda, realizando buscas diretamente no 
# arquivo binário  sem precisar reconstruir a árvore na RAM do zero por inserções repetidas.
#     Exigência na Apresentação: Inicializar o sistema com a RAM limpa, abrir o arquivo binário gerado 
# previamente e realizar uma busca com sucesso, provando o isolamento e leitura dos blocos de dados.


class NodoB:

    def __init__(self):
        self.chaves = []
        self.filhos = []


class ArvoreB:

    def __init__(self):
        self.raiz = NodoB()
        self.maxChaves = 3

    # Função para juntar todos os campos da receita em uma string,
    # serve para comparar se a receita foi alterada depois de inserida
    def resumoReceita(self, receita):
        return f"{receita.id}{receita.nome}{receita.categoria}{receita.ingredientes}{receita.tempo},{receita.custo}{receita.dificuldade}{receita.avaliacao}{receita.popularidade}"

    # Função para inserir a receita na árvore pelo id
    def inserir(self, receita):

        # Verifica se o id já existe, se sim é duplicata
        if self.buscar(receita.id) is not None:
            return False

        resumo = self.resumoReceita(receita)

        # Se a raiz estiver cheia, cria uma nova raiz e divide
        if len(self.raiz.chaves) == self.maxChaves:
            novaRaiz = NodoB()
            novaRaiz.filhos.append(self.raiz)
            self.dividirFilho(novaRaiz, 0)
            self.raiz = novaRaiz

        self.inserirNaoCheio(self.raiz, receita, resumo)
        return True

    def inserirNaoCheio(self, nodo, receita, resumo):

        i = len(nodo.chaves) - 1

        # Se for folha, insere direto na posição correta
        if len(nodo.filhos) == 0:
            nodo.chaves.append(None)

            while i >= 0 and receita.id < nodo.chaves[i][0]:
                nodo.chaves[i + 1] = nodo.chaves[i]
                i -= 1

            nodo.chaves[i + 1] = (receita.id, receita, resumo)

        else:
            # Acha em qual filho deve descer
            while i >= 0 and receita.id < nodo.chaves[i][0]:
                i -= 1

            i += 1

            # Se o filho estiver cheio, divide antes de descer
            if len(nodo.filhos[i].chaves) == self.maxChaves:
                self.dividirFilho(nodo, i)

                if receita.id > nodo.chaves[i][0]:
                    i += 1

            self.inserirNaoCheio(nodo.filhos[i], receita, resumo)

    def dividirFilho(self, pai, i):

        filhoCheio = pai.filhos[i]
        novoFilho = NodoB()
        meio = 1

        # A chave do meio sobe para o pai
        chaveMeio = filhoCheio.chaves[meio]

        # Divide as chaves entre o filho atual e o novo filho
        novoFilho.chaves = filhoCheio.chaves[meio + 1:]
        filhoCheio.chaves = filhoCheio.chaves[:meio]

        # Divide os filhos também se não for folha
        if len(filhoCheio.filhos) > 0:
            novoFilho.filhos = filhoCheio.filhos[meio + 1:]
            filhoCheio.filhos = filhoCheio.filhos[:meio + 1]

        pai.filhos.insert(i + 1, novoFilho)
        pai.chaves.insert(i, chaveMeio)

    # Função para buscar uma receita pelo id
    def buscar(self, idReceita):

        return self.buscarNodo(self.raiz, idReceita)

    def buscarNodo(self, nodo, idReceita):

        i = 0

        while i < len(nodo.chaves) and idReceita > nodo.chaves[i][0]:
            i += 1

        if i < len(nodo.chaves) and idReceita == nodo.chaves[i][0]:
            return nodo.chaves[i][1]

        if len(nodo.filhos) == 0:
            return None

        return self.buscarNodo(nodo.filhos[i], idReceita)

    # Função auxiliar para pegar o resumo guardado na árvore
    def buscarResumo(self, nodo, idReceita):

        i = 0

        while i < len(nodo.chaves) and idReceita > nodo.chaves[i][0]:
            i += 1

        if i < len(nodo.chaves) and idReceita == nodo.chaves[i][0]:
            return nodo.chaves[i][2]

        if len(nodo.filhos) == 0:
            return None

        return self.buscarResumo(nodo.filhos[i], idReceita)

    # Função do modo investigação

    # Verifica duplicatas e alterações em todas as receitas
    def modoInvestigacao(self, receitas):

        duplicatas = []
        alteradas = []
        idsVistos = []

        for receita in receitas:

            # Se o id já apareceu antes na lista, é duplicata
            if receita.id in idsVistos:
                duplicatas.append(receita)
            else:
                idsVistos.append(receita.id)

            # Compara o resumo atual com o resumo guardado na árvore
            resumoGuardado = self.buscarResumo(self.raiz, receita.id)
            resumoAtual = self.resumoReceita(receita)

            if resumoGuardado is not None and resumoAtual != resumoGuardado:
                alteradas.append(receita)

        return duplicatas, alteradas