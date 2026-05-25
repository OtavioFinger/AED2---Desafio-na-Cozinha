class HashTable:
    def __init__(self, tamanho = 103):
        self.tamanho = tamanho
        #cria uma lista de dicionários vazios, para evitar colisões de itens com o mesmo índice
        self.tabela = [[]for _ in range(tamanho)]

    #função para transformar a palavra em um indice hash
    def hash(self, chave):
        soma = 0

        for char in chave:
            soma += ord(char)
        
        return soma % self.tamanho
    #função para inserir ingredientes na receita
    def inserir(self, ingrediente, receita):
        indice = self.hash(ingrediente)
        bucket = self.tabela[indice]

        for item in bucket:
            if item[0] == ingrediente:
                item[1].append(receita)
                return
        
        bucket.append([ingrediente, [receita]])
    #função para buscar receitas com tal ingrediente
    def buscar(self, ingrediente):
        indice = self.hash(ingrediente)
        bucket = self.tabela[indice]

        for item in bucket:
            if item[0] == ingrediente:
                return item[1]

        return []

#Essa essa estrutura de dados foi escolhida para ser usada na busca por ingredientes devido seu alto desempenho, sendo O(1) na maioria dos casos.
