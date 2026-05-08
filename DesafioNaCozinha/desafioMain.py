#imports para o projeto
import json
import os

#imports das classes
from models.receita import Receita

os.system('cls')

receitas = []

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
