# Arquivo separado para testar a persistência em disco da Árvore B
# Rodar este arquivo de forma independente do desafioMain.py
# Ele carrega a árvore do arquivo .dat sem reconstruir nada na ram
# e realiza uma busca por id diretamente da estrutura carregada.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structs.arvoreB import ArvoreB

caminho = "DesafioNaCozinha/data/arvore.dat"

print("!!! Opção C: Árvores B e Simulação de Memória Secundária (I/O) !!!\n")

# Cria uma árvore vazia, sem nenhuma receita na ram
arvore = ArvoreB()

# Tenta carregar do disco
carregou = arvore.carregarDoDisco(caminho)

if not carregou:
    print("Arquivo arvore.dat não encontrado.")
    print("Execute o desafioMain.py primeiro para gerar o arquivo.")

else:
    print("RAM iniciada limpa. Árvore carregada apenas do disco.")
    print("\n")

    idBusca = int(input("Digite o ID da receita que deseja buscar: "))

    resultado = arvore.buscar(idBusca)

    print("\n")

    if resultado is None:
        print(f"Nenhuma receita encontrada com ID {idBusca}.")

    else:
        print("Receita encontrada diretamente do disco:")
        print(f"  ID:           {resultado.id}")
        print(f"  Nome:         {resultado.nome}")
        print(f"  Categoria:    {resultado.categoria}")
        print(f"  Tempo:        {resultado.tempo} min")
        print(f"  Custo:        R${resultado.custo}")
        print(f"  Dificuldade:  {resultado.dificuldade}")
        print(f"  Avaliação:    {resultado.avaliacao}")
        print(f"  Popularidade: {resultado.popularidade}")