#imports para o projeto
import json
import os

#imports das classes
from models.receita import Receita
from models.recomendacao import recomendarReceitas
from structs.hash import HashTable
from structs.trie import Trie
from structs.arvoreB import ArvoreB

os.system('cls')

receitas = []

# Função para inserir as receitas na hashtable
def adicionarIngredientes(tabela, receitas):

    for receita in receitas:

        for ingrediente in receita.ingredientes:

            tabela.inserir(
                ingrediente.lower(),
                receita
            )


# pega e le o arquivo json
with open("DesafioNaCozinha/data/receita.json", "r", encoding="utf-8") as doc:

    dados = json.load(doc)

    for item in dados:

        receita = Receita(
            item["id"],
            item["nome"],
            item["categoria"],
            item["ingredientes"],
            item["tempo"],
            item["custo"],
            item["dificuldade"],
            item["avaliacao"],
            item["popularidade"]
        )

        receitas.append(receita)

tabelaIngredientes = HashTable()
adicionarIngredientes(tabelaIngredientes, receitas)

trie = Trie()
for receita in receitas:
    trie.inserir(receita.nome.lower())

arvore = ArvoreB()
for receita in receitas:
    arvore.inserir(receita)

# Se o arquivo .dat já existe, carrega do disco
# Se não, insere todas as receitas e salva
if arvore.carregarDoDisco("DesafioNaCozinha/data/arvore.dat"):
    print("Árvore carregada do disco com sucesso!")
else:
    for receita in receitas:
        arvore.inserir(receita)
    arvore.salvarEmDisco("DesafioNaCozinha/data/arvore.dat")
    print("Árvore criada e salva em disco!")


while True:
    print("=======Bem vindo=======")
    print("--Menu--")
    print("1- Buscar receita por ingrediente")
    print("2- Buscar receita por nome")
    print("3- Recomendar receita")
    print("4- Modo Investigação")
    print("5- Sair")

    opcao = input("Escolha uma opção: ").lower()

    if opcao == "1":
        ingrediente = input("\n Digite o ingrediente:").lower()
        resultado = tabelaIngredientes.buscar(ingrediente)
        print()

        if len(resultado) == 0:
            print("Nenhuma receita encontrada!")
        
        else:
            print("--Receitas--")
            for r in resultado:
                print(f"-{r.nome}")
    
    elif opcao == "2":
        prefixo = input("Digite o nome da receita:").lower()
        resultado = trie.buscar(prefixo)
        print()

        if len(resultado) == 0:
            print("Nenhuma receita encontrada!")

        else:
            print("--Receitas--")
            for r in resultado:
                print(f"-{r.nome}")

    elif opcao == "3":
        orcamento = float(input("Qual o orçamento máximo? "))
        resultado = recomendarReceitas(receitas, orcamento)
        print()

        if len(resultado) == 0:
            print("Nenhuma receita do sistema está de acordo com esses parâmentros")
        
        else:
            for r in resultado:
                print(f"-{r.nome}")
                print(f"-R${r.custo}")
                print(f"-{r.avaliacao}")
                print()
    
    elif opcao == "4":

        duplicatas, alteradas = arvore.modoInvestigacao(receitas)

        if len(duplicatas) == 0 and len(alteradas) == 0:
            print("Nenhuma receita recebeu alteração!")

        if len(duplicatas) > 0:
            print("\n--Receitas duplicadas--")
            for r in duplicatas:
                print(f"-{r.nome} (id: {r.id})")

        if len(alteradas) > 0:
            print("\n--Receitas alteradas--")
            for r in alteradas:
                print(f"-{r.nome} (id: {r.id})")

    elif opcao == "5":
        print("Obrigado por usar esse sistema!")
        break
    
    else:
        print("Opção inválida")

        