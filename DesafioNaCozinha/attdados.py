import json
import random

def gerar_dependencias():
    # Módulo 5: Grafo Dirigido (DAG) de Produção
    # Vamos criar alguns "preparos base" (IDs 100 a 110) que servem de pré-requisito para as receitas (IDs 1 a 55)
    arestas = []
    
    preparos_base = [
        {"id": 100, "nome": "Caldo de Carne Base"},
        {"id": 101, "nome": "Massa de Torta Pré-assada"},
        {"id": 102, "nome": "Molho de Tomate Rústico"},
        {"id": 103, "nome": "Mirepoix (Cebola, Cenoura, Salsão)"},
        {"id": 104, "nome": "Caldo de Legumes"}
    ]
    
    # Adicionando arestas: um preparo aponta para várias receitas aleatórias
    for prep in preparos_base:
        # Cada preparo base será usado por 3 a 6 receitas diferentes
        receitas_destino = random.sample(range(1, 56), random.randint(3, 6))
        for rec_id in receitas_destino:
            arestas.append({
                "origem": prep["id"],
                "destino": rec_id,
                "descricao": f"Requer {prep['nome']}"
            })
            
    # Garantindo algumas dependências entre as próprias receitas (ex: Receita A precisa da Receita B)
    # Criando algumas poucas arestas seguras para não gerar ciclos acidentais agora
    arestas.append({"origem": 12, "destino": 21}) # Hummus (12) como base pro Falafel (21)
    arestas.append({"origem": 42, "destino": 6})  # Miso Soup (42) como entrada pro Sushi (6)

    dados_dependencias = {
        "preparos": preparos_base,
        "arestas": arestas
    }
    
    with open('dependencias.json', 'w', encoding='utf-8') as f:
        json.dump(dados_dependencias, f, indent=4, ensure_ascii=False)
    
    print(f"-> dependencias.json criado! ({len(preparos_base)} vértices de preparo, {len(arestas)} arestas)")
    return len(preparos_base), len(arestas)

def gerar_logistica():
    # Módulo 7: Rede Logística (Regiões, Pontos de Retirada, Estações)
    regioes = [{"id": f"R{i}", "nome": f"Região {i}"} for i in range(1, 9)] # 8 vértices
    estacoes = [{"id": f"E{i}", "nome": f"Cozinha {i}", "capacidade": random.randint(20, 50)} for i in range(1, 4)] # 3 vértices
    pontos = [{"id": f"P{i}", "nome": f"Ponto {i}", "regiao": f"R{random.randint(1, 8)}"} for i in range(1, 6)] # 5 vértices
    
    arestas = []
    todos_nos = [n["id"] for n in regioes + estacoes + pontos]
    
    # Conectando nós aleatoriamente para simular ruas/rotas
    for i in range(len(todos_nos)):
        # Cada nó se conecta a 2 ou 3 outros nós
        conexoes = random.sample(todos_nos, random.randint(2, 3))
        for destino in conexoes:
            if todos_nos[i] != destino:
                # Evita duplicatas exatas na mesma direção
                if not any(a["origem"] == todos_nos[i] and a["destino"] == destino for a in arestas):
                    arestas.append({
                        "origem": todos_nos[i],
                        "destino": destino,
                        "distancia_km": round(random.uniform(1.5, 12.0), 1),
                        "tempo_min": random.randint(5, 30)
                    })

    dados_logistica = {
        "regioes": regioes,
        "estacoes": estacoes,
        "pontos_retirada": pontos,
        "rotas": arestas
    }
    
    with open('logistica.json', 'w', encoding='utf-8') as f:
        json.dump(dados_logistica, f, indent=4, ensure_ascii=False)
        
    total_vertices = len(regioes) + len(estacoes) + len(pontos)
    print(f"-> logistica.json criado! ({total_vertices} vértices logísticos, {len(arestas)} arestas/rotas)")
    return total_vertices, len(arestas)

if __name__ == "__main__":
    random.seed(17) # Garantir os mesmos resultados
    
    print("Gerando dados de grafos para o T2...")
    v_dep, e_dep = gerar_dependencias()
    v_log, e_log = gerar_logistica()
    
    total_v = v_dep + v_log + 55 # 55 receitas já existentes
    total_e = e_dep + e_log
    
    print("-" * 30)
    print(f"RESUMO PARA O RELATÓRIO:")
    print(f"Total de Vértices: {total_v} (Mínimo exigido: 30)")
    print(f"Total de Arestas: {total_e} (Mínimo exigido: 50)")
    
    if total_v >= 30 and total_e >= 50:
        print("✅ Requisito de tamanho do grafo atingido com sucesso!")