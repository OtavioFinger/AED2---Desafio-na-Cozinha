#imports para o projeto
import json
import os

#imports das classes
from models.receita import Receita
from models.recomendacao import recomendarReceitas
from structs.hash import HashTable
from structs.trie import Trie
from structs.arvoreB import ArvoreB
from structs.grafo import Grafo
from algorithms.kahnAlgoritm import OficinaProducao
from algorithms.mst import PlanejamentoLogistico
from algorithms.bottomUp import MenuVIP

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
def construirGrafoDependencias(receitas, caminho_json):
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    grafo = Grafo(dirigido=True)

    for r in receitas:
        grafo.adicionar_vertice(r.id)
        
    for preparo in dados["preparos"]:
        grafo.adicionar_vertice(preparo["id"])

    for aresta in dados["arestas"]:
        grafo.adicionar_aresta(aresta["origem"], aresta["destino"])

    return grafo

def construirGrafoLogistica(caminho_json):
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    grafo = Grafo(dirigido=True)

    for regiao in dados["regioes"]:
        grafo.adicionar_vertice(regiao["id"])
        
    for estacao in dados["estacoes"]:
        grafo.adicionar_vertice(estacao["id"])
        
    for ponto in dados["pontos_retirada"]:
        grafo.adicionar_vertice(ponto["id"])

    for rota in dados["rotas"]:
        grafo.adicionar_aresta(
            rota["origem"], rota["destino"],
            peso=rota["tempo_min"],
            dados_extras={"capacidade": rota.get("capacidade", 10)} 
        )

    return grafo

# pega e le o arquivo json
with open("data/receita.json", "r", encoding="utf-8") as doc:

    dados = json.load(doc)

    for item in dados:
        receitas.append(Receita(**item))

tabelaIngredientes = HashTable()
adicionarIngredientes(tabelaIngredientes, receitas)

trie = Trie()
for receita in receitas:
    trie.inserir(receita.nome.lower())

arvore = ArvoreB()

# Se o arquivo .dat já existe, carrega do disco
# Se não, insere todas as receitas e salva
if arvore.carregarDoDisco("DesafioNaCozinhadata/arvore.dat"):
    print("Árvore carregada do disco com sucesso!")
else:
    for receita in receitas:
        arvore.inserir(receita)
    arvore.salvarEmDisco("data/arvore.dat")
    print("Árvore criada e salva em disco!")

grafo_dependencias = construirGrafoDependencias(receitas, "data/dependencias.json")
grafo_logistica = construirGrafoLogistica("data/logistica.json")

while True:
    print("=======Bem vindo=======")
    print("--Menu--")
    print("1- Buscar receita por ingrediente")
    print("2- Buscar receita por nome")
    print("3- Recomendar receita")
    print("4- Modo Investigação")
    print("5- Oficina de Produção")
    print("6- Logística de Distribuição")
    print("7- Otimização de Cardápio")
    print("0- Sair")

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
        prefixo = input("Digite o nome da receita: ").lower()
        resultado = trie.buscar(prefixo)
        print()

        if len(resultado) == 0:
            print("Nenhuma receita encontrada!")

        else:
            print("--Receitas--")
            for r in resultado:
                print(f"- {r.title()}")

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
        print("\n=== OFICINA DE PRODUÇÃO ===")
        print("a) Ordem de preparo")
        print("b) Verificar ciclos")
        print("c) Ver pré-requisitos")
        sub_opcao = input("Escolha (a/b/c): ").lower()

        oficina = OficinaProducao(grafo_dependencias)

        mapeamento_nomes = {}
        for r in receitas:
            mapeamento_nomes[r.id] = r.nome
            mapeamento_nomes[str(r.id)] = r.nome
            try:
                mapeamento_nomes[int(r.id)] = r.nome
            except:
                pass

        caminhos_possiveis = [
            "data/dependencias.json",
            "DesafioNaCozinha/data/dependencias.json"
        ]
        dados_dep = {"preparos": []}

        for caminho in caminhos_possiveis:
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados_dep = json.load(f)
                    break
            except FileNotFoundError:
                continue

        for preparo in dados_dep.get("preparos", []):
            p_id = preparo["id"]
            p_nome = preparo.get("nome", f"Preparo {p_id}")
            mapeamento_nomes[p_id] = p_nome
            mapeamento_nomes[str(p_id)] = p_nome
            try:
                mapeamento_nomes[int(p_id)] = p_nome
            except:
                pass

        if sub_opcao == "a":
            ordem, tem_ciclo = oficina.ordenacao_topologica()

            if tem_ciclo:
                print("Há um ciclo nas dependências.")
            else:
                print("\nOrdem de preparo:")

                ordem_nomes = []
                for id_no in ordem:
                    nome_final = mapeamento_nomes.get(
                        id_no,
                        mapeamento_nomes.get(str(id_no), f"Item {id_no}")
                    )
                    ordem_nomes.append(nome_final)

                print("\n→ ".join(ordem_nomes))
                print()

        elif sub_opcao == "b":
            _, tem_ciclo = oficina.ordenacao_topologica()

            if tem_ciclo:
                print("Foi encontrado um ciclo.")
            else:
                print("Nenhum ciclo encontrado.")

        elif sub_opcao == "c":
            id_receita = input("ID da receita: ")

            try:
                id_busca = int(id_receita)
            except:
                id_busca = id_receita

            reqs = oficina.buscar_pre_requisitos(id_busca)

            nomes_reqs = [
                mapeamento_nomes.get(
                    req,
                    mapeamento_nomes.get(str(req), f"Item {req}")
                )
                for req in reqs
            ]

            nome_alvo = mapeamento_nomes.get(
                id_busca,
                mapeamento_nomes.get(str(id_busca), f"Receita {id_receita}")
            )

            print(f"\nPré-requisitos de '{nome_alvo}':")
            print(nomes_reqs)

    elif opcao == "6":
        print("\n=== LOGÍSTICA ===")
        print("a) Rede mínima")
        print("b) Melhor rota")
        print("c) Capacidade máxima")
        sub_opcao = input("Escolha (a/b/c): ").lower()

        logistica = PlanejamentoLogistico(grafo_logistica)

        if sub_opcao == "a":
            print("-----REDE OTIMIZADA-----")

            rotas_otimizadas, custo_total = logistica.otimizar_infraestrutura_kruskal()

            print(f"Custo total: {custo_total} minutos")
            print("\nRotas:")

            for i, rota in enumerate(rotas_otimizadas, start=1):
                origem = rota["origem"]
                destino = rota["destino"]
                custo = rota["custo"]

                print(f"{i}. {origem} -> {destino} ({custo} min)")

            print("\n")

        elif sub_opcao == "b":
            origem = input("Origem: ").upper()
            destino = input("Destino: ").upper()

            rota = logistica.calcular_rota_mais_rapida(origem, destino)

            print(" ------MELHOR ROTA------\n")
            print(f"Origem: {origem}")
            print(f"Destino: {destino}")

            if isinstance(rota, tuple) and len(rota) == 2:
                if isinstance(rota[0], list):
                    caminho, tempo = rota
                else:
                    tempo, caminho = rota
                print(f"Tempo: {tempo} min")
            else:
                caminho = rota

            if caminho:
                if isinstance(caminho, list):
                    print(f"Rota: {' -> '.join(caminho)}")
                else:
                    print(f"Rota: {caminho}")
            else:
                print("Nenhuma rota encontrada.")


        elif sub_opcao == "c":
            origem = input("Origem: ").upper()
            destino = input("Destino: ").upper()

            cap_max = logistica.calcular_capacidade_maxima(origem, destino)

            print("------CAPACIDADE------\n")
            print(f"Origem: {origem}")
            print(f"Destino: {destino}")

            valor_capacidade = 0
            fluxo = []

            if isinstance(cap_max, tuple) and len(cap_max) == 2:
                valor_capacidade, fluxo = cap_max
            else:
                valor_capacidade = cap_max

            print(f"Capacidade: {valor_capacidade}")

            if fluxo:
                print("\nRotas:")
                for conexao in fluxo:
                    print(f"{conexao.get('de', '?')} -> {conexao.get('para', '?')}")

    elif opcao == "7":
        print("\n=== CARDÁPIO VIP ===")
        print("Encontre a melhor combinação de pratos.")

        try:
            tempo_maximo = int(input("Tempo disponível (min): "))
            raros_maximo = int(input("Limite de ingredientes raros: "))
        except ValueError:
            print("Digite apenas números.")
            continue

        # Criando a lista de dicionários passo a passo (Formato Padrão)
        receitas_dicionario = []
        for r in receitas:
            # Transforma o objeto em um dicionário comum
            dados_receita = vars(r).copy()
            
            # Se não tiver a chave de ingredientes raros, define como 0 por segurança
            if "ingredientes_raros" not in dados_receita:
                dados_receita["ingredientes_raros"] = 0
                
            receitas_dicionario.append(dados_receita)

        # Instancia a classe e calcula (Feito em duas linhas claras)
        menu_vip = MenuVIP(receitas_dicionario)
        
        print("\nCalculando...")
        lucro_maximo, pratos_escolhidos = menu_vip.otimizar_menu(tempo_maximo, raros_maximo)

        print("\n==============================")
        print("     CARDÁPIO IDEAL")
        print("==============================")
        print(f"Lucro: R${lucro_maximo:.2f}")
        print(f"Tempo: {sum(p['tempo'] for p in pratos_escolhidos)} min")
        print(f"Ingredientes raros: {sum(p['ingredientes_raros'] for p in pratos_escolhidos)}")
        print("\nPratos:")

        # Loop tradicional para exibir os pratos escolhidos
        for i, prato in enumerate(pratos_escolhidos, start=1):
            lucro_prato = prato["valor_venda"] - prato["custo"]
            print(f"{i}. {prato['nome']} ({prato['tempo']} min, Lucro: R${lucro_prato:.2f})")

        print("==============================\n")
    elif opcao == "0":
        print("Até logo!")
        break

    else:
        print("Opção inválida.")