#imports para o projeto
import json
import os

#imports das classes
from models.receita import Receita
from structs.hash import HashTable
from structs.trie import Trie

os.system('cls')

receitas = []

#função para inserir as receitas na hashtable
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

