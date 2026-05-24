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



class NodoB: # Estrutura do nodo da Árvore B
 
    def __init__(self):
        self.chaves = []
        self.filhos = []
 
    def ehFolha(self):
        return len(self.filhos) == 0

# Instância da Árvore B em si
class ArvoreB:
 
     def __init__(self):
        self.raiz = NodoB()
