# T2 - Desafio na Cozinha (Aprimorado)

### Link do repositório
https://github.com/OtavioFinger/AED2---Desafio-na-Cozinha

### Por Arthur Trettin Bast e Otávio Finger

# Introdução

Este trabalho dá continuidade ao sistema desenvolvido no Trabalho 1, reaproveitando toda a base de dados e as estruturas já implementadas (Tabela Hash, Trie e Árvore B). O foco do Trabalho 2 é evoluir o sistema para lidar com problemas de **modelagem de redes** e **otimização de decisões**, introduzindo os seguintes conteúdos, todos novos em relação ao T1:

- Programação Dinâmica
- Grafos (representação e percurso)
- Detecção de Ciclos e Ordenação Topológica
- Caminhos Mínimos (Dijkstra)
- Árvores Geradoras Mínimas (Kruskal + Union-Find)
- Tópicos Avançados em Grafos: Redes, Fluxo Máximo, Comunidades e Heurísticas de Busca Combinatória

Nenhuma das estruturas ou funcionalidades do T1 (Hash, Trie, Árvore B, recomendação gulosa) foi descartada — elas continuam ativas nas opções 1 a 4 do menu. Este documento descreve **apenas** o que foi acrescentado no T2, módulo por módulo.

O restaurante agora oferece, além dos modos antigos:

5. Oficina de Produção
6. Logística de Distribuição
7. Otimização de Cardápio (Menu VIP)
8. Comunidades Gastronômicas
9. Menu Especial Dia dos Namorados
0. Sair

---

# Estruturação dos arquivos 

Abaixo, está descrito toda a árvore de arquivos do projeto, seus usos, bem como relação com cada módulo do código será descrito nas seções de módulos individuais:

```text
AED2 - Desafio na Cozinha/
├── README.md
├── README - T1.md
└── DesafioNaCozinha/
    ├── desafioMain.py
    ├── testarDisco.py
    │
    ├── algorithms/
    │   ├── bottomUp.py
    │   ├── comunidades.py
    │   ├── kahnAlgoritm.py
    │   ├── menuNamorados.py
    │   └── mst.py
    │
    ├── data/
    │   ├── arvore.dat
    │   ├── dependencias.json
    │   ├── logistica.json
    │   └── receita.json
    │
    ├── models/
    │   ├── receita.py
    │   └── recomendacao.py
    │
    └── structs/
        ├── arvoreB.py
        ├── grafo.py
        ├── hash.py
        ├── heap.py
        ├── trie.py
        └── uFind.py
```

# Estrutura Central: `structs/grafo.py`

Todos os módulos novos (5, 6 parcialmente, 7 e 8) dependem de uma estrutura de **Grafo** construída do zero, que serve de base comum para a modelagem de redes do sistema.

## Classe `Grafo`

Implementada como uma **lista de adjacências**, usando um dicionário Python onde cada chave é um vértice e o valor é uma lista de arestas.

- `adicionar_vertice(v)`: garante que o vértice existe no dicionário de adjacências, mesmo sem arestas.
- `adicionar_aresta(u, v, peso=1, dados_extras=None)`: cria a aresta `u → v` com um peso (usado em rotas e no cálculo de MST/Dijkstra) e aceita dados extras arbitrários (por exemplo, `capacidade`, usado no cálculo de fluxo máximo). Se o grafo não for dirigido, a aresta de volta `v → u` é criada automaticamente.
- `obter_vizinhos(u)` / `obter_vertices()`: acesso direto à lista de adjacências, usados por todos os algoritmos de percurso.
- `grau_entrada()`: calcula o grau de entrada de cada vértice, contando quantas arestas apontam para ele — é a base do algoritmo de Kahn usado no Módulo 5.

Essa mesma estrutura é reaproveitada tanto para o grafo de **dependências entre preparos** (Módulo 5) quanto para o grafo de **logística de entrega** (Módulo 7), bastando alternar entre grafo dirigido ou não dirigido e os pesos/atributos das arestas.

O sistema constrói dois grafos a partir de arquivos `.json` próprios:

- `data/dependencias.json`: define os preparos intermediários e as arestas de pré-requisito entre receitas — usado no Módulo 5.
- `data/logistica.json`: define regiões de entrega, estações de preparo e pontos de retirada, além das rotas entre eles com tempo e capacidade — usado no Módulo 7.

---

# Módulo 5 — Oficina de Produção (`algorithms/kahnAlgoritm.py`)

**Conteúdos aplicados:** Grafos, Detecção de Ciclos e Ordenação Topológica.

O restaurante cadastra dependências entre preparações (ex.: molho antes da lasanha, massa antes da sobremesa). O grafo de dependências é dirigido: uma aresta `origem → destino` indica que `origem` precisa estar pronta antes de `destino`.

## Classe `OficinaProducao`

### Método `ordenacao_topologica()`

Implementa o **Algoritmo de Kahn**, baseado em graus de entrada (BFS):

1. Calcula o grau de entrada de todos os vértices com `grafo.grau_entrada()`.
2. Inicializa uma fila apenas com os vértices sem nenhuma dependência (grau de entrada 0).
3. Remove um vértice da fila por vez (usando um ponteiro `i` para simular a remoção sem custo de deslocar a lista), adiciona-o à ordem final e decrementa o grau de entrada de todos os seus vizinhos.
4. Sempre que o grau de entrada de um vizinho chega a zero, ele é liberado para a fila.

Se, ao final, o tamanho da lista `ordem` for menor que o número total de vértices, significa que sobraram vértices que nunca zeraram seu grau de entrada — ou seja, **existe um ciclo** e não há uma ordem de produção válida. É assim que o sistema responde às consultas "Existe algum erro de dependência?" e "Qual a sequência correta para produzir o menu do dia?".

Para validar essa detecção, o arquivo `dependencias.json` inclui propositalmente dois preparos fictícios ("Preparo Cíclico A" e "Preparo Cíclico B") que dependem um do outro.

### Método `buscar_pre_requisitos(receita_alvo)`

Responde à consulta "Quais preparos precisam ser concluídos antes da receita X?". Constrói um **grafo reverso** (invertendo o sentido de todas as arestas) e faz uma busca em largura (BFS) a partir da receita alvo, coletando todos os vértices alcançáveis nesse grafo invertido — ou seja, todos os preparos que, direta ou indiretamente, precisam acontecer antes dela.

**Complexidade:** O(V + E) tanto para a ordenação topológica quanto para a busca de pré-requisitos, onde V é o número de preparos/receitas e E o número de dependências cadastradas.

---

**Porque essa estrutura?** Porque BFS/Kahn e não DFS com pilha de recursão para ordenação topológica? Pq o Kahn detecta ciclo de forma mais natural, sem precisar de cores/estado de visita "em progresso", e evita risco de estouro de pilha em grafos maiores.

# Módulo 6 — Menu Degustação VIP (`algorithms/bottomUp.py`)

**Conteúdo aplicado:** Programação Dinâmica.

O Chef quer montar um cardápio VIP que maximize o lucro respeitando duas restrições simultâneas: tempo total de preparo e limite de ingredientes raros disponíveis. Esse é um problema clássico de **Mochila 0/1 com duas dimensões de restrição**.

## Classe `MenuVIP`

### Método `otimizar_menu(limite_tempo, limite_raros)`

Constrói uma tabela de programação dinâmica **bottom-up**, `tabela[t][r]`, onde cada célula guarda a tupla `(melhor_lucro, lista_de_receitas)` alcançável usando até `t` minutos e `r` ingredientes raros.

Para cada receita, o algoritmo percorre as dimensões de tempo e raros **de trás para frente** (do maior limite até o custo da própria receita). Isso é o que garante que cada receita seja considerada no máximo uma vez por combinação (comportamento 0/1, evitando reaproveitar a mesma receita duas vezes na mesma solução).

Para cada célula, compara o lucro já registrado (`tabela[t][r]`) com o lucro obtido ao incluir a receita atual (lucro da subsolução `tabela[t-tempo][r-raros]` somado ao lucro da própria receita) e mantém o maior dos dois.

Ao final, `tabela[limite_tempo][limite_raros]` contém a melhor combinação de receitas encontrada e o lucro máximo obtido, respondendo a perguntas como "Qual o melhor menu com X minutos e Y ingredientes raros disponíveis?".

**Complexidade:** O(N × T × R), onde N é o número de receitas candidatas, T o limite de tempo e R o limite de ingredientes raros — típica de soluções de Programação Dinâmica para o problema da mochila com múltiplas restrições.

---

**Porque essa estrutura?** Escolhemos pois o Alg. Guloso não garante ótimo global com duas restrições simultâneas; força bruta é exponencial; DP bottom-up resolve em tempo pseudo-polinomial e é o padrão para mochila com múltiplas dimensões.


# Módulo 7 — O Pesadelo Logístico (`algorithms/mst.py`, `structs/uFind.py`, `structs/heap.py`)

**Conteúdos aplicados:** Árvores Geradoras Mínimas, Caminhos Mínimos e Tópicos Avançados em Grafos (Fluxo Máximo em Redes).

A rede logística (regiões de entrega, estações de preparo e pontos de retirada) é modelada como um grafo com pesos (tempo em minutos) e capacidades por rota.

## `structs/uFind.py` — Union-Find (Disjoint Set)

Estrutura auxiliar implementada do zero, usada pelo algoritmo de Kruskal para detectar ciclos de forma eficiente.

- `find(v)`: encontra a raiz do conjunto de `v`, aplicando **compressão de caminho** (cada nó visitado passa a apontar diretamente para a raiz), o que acelera buscas futuras.
- `union(u, v)`: une os conjuntos de `u` e `v` usando **união por rank** (o conjunto de menor "altura" é anexado ao de maior), retornando `False` quando os dois já pertencem ao mesmo conjunto (ou seja, uni-los criaria um ciclo).

## `structs/heap.py` — Min-Heap

Fila de prioridade binária implementada manualmente (sem usar `heapq`), usada pelo algoritmo de Dijkstra para sempre extrair o vértice com menor distância acumulada.

- `push(prioridade, item)`: insere o par no final do heap e usa `_subir()` para restaurar a propriedade de heap comparando com o pai.
- `pop()`: remove e retorna o menor elemento (raiz), movendo o último elemento para a raiz e usando `_descer()` para restaurar a propriedade de heap comparando com os filhos.

## Classe `PlanejamentoLogistico`

### Método `otimizar_infraestrutura_kruskal()`

Resolve o problema "menor rede de conexões necessária para interligar todos os pontos operacionais" usando o **Algoritmo de Kruskal**:

1. Coleta todas as arestas únicas do grafo (evitando duplicar arestas em grafos não dirigidos) e as ordena por peso crescente.
2. Percorre as arestas em ordem, usando a estrutura `UnionFind` para verificar se os dois vértices já estão conectados.
3. Se não estiverem (`union()` retorna `True`), a aresta é adicionada à Árvore Geradora Mínima e seu custo é somado ao total.

Isso garante a rede de menor custo total (tempo) que conecta todos os pontos, sem formar ciclos redundantes.

### Método `calcular_rota_mais_rapida(origem, destino)`

Implementa o **Algoritmo de Dijkstra** para caminhos mínimos, usando o `MinHeap` implementado como fila de prioridade:

1. Inicializa as distâncias de todos os vértices como infinito, exceto a origem (0), e insere a origem no heap.
2. A cada iteração, extrai do heap o vértice não visitado de menor distância acumulada.
3. Relaxa as arestas para os vizinhos não visitados: se o caminho pela rota atual for mais curto que o registrado, atualiza a distância e o predecessor daquele vizinho, reinserindo-o no heap.
4. Ao alcançar o destino (ou esvaziar o heap), reconstrói o caminho percorrendo os predecessores de trás para frente.

Responde a consultas como "determinação de rotas" e "estimativas de tempo operacional".

### Método `calcular_capacidade_maxima(origem, destino)`

Implementa o **Algoritmo de Fluxo Máximo (Ford-Fulkerson / Edmonds-Karp)**, usando busca em largura (BFS) para encontrar caminhos aumentantes em um grafo residual:

1. Constrói o grafo residual a partir das capacidades cadastradas em cada rota (`dados_extras["capacidade"]`).
2. Repetidamente busca, via BFS (`bfs_caminho_aumentante`), um caminho da origem até o destino com capacidade residual positiva.
3. Para cada caminho encontrado, calcula o gargalo (a menor capacidade residual ao longo do caminho) e atualiza o grafo residual, somando esse valor ao fluxo total.
4. Repete até que não existam mais caminhos aumentantes — nesse ponto, o fluxo acumulado é o **fluxo máximo** entre origem e destino.
5. Identifica os **gargalos operacionais**: após a última busca, os vértices ainda alcançáveis no grafo residual formam um lado do corte mínimo; toda aresta que sai desse conjunto para o restante da rede é reportada como gargalo, respondendo diretamente a "Existe gargalo operacional?".

**Complexidade:** O(E log V) para Kruskal (dominado pela ordenação das arestas), O((V + E) log V) para Dijkstra com heap binário, e O(V × E²) no pior caso para o fluxo máximo via Edmonds-Karp (BFS como estratégia de busca de caminho aumentante).

---

**Por que essa estrutura?** Por que Kruskal e não Prim? Mais simples de implementar com lista de arestas ordenadas, funciona bem com grafos esparsos como o de logística. 
Por que Dijkstra e não Bellman-Ford? Pesos não-negativos, então Dijkstra é mais eficiente. Por que BFS (Edmonds-Karp) e não DFS puro no Ford-Fulkerson? (garante caminhos aumentantes mais curtos, evitando piores casos de convergência lenta).

# Módulo 8 / Laboratório de Inovação — Comunidades Gastronômicas (`algorithms/comunidades.py`)

**Conteúdo aplicado:** Tópicos Avançados em Grafos — detecção de comunidades/componentes conectados via busca em profundidade (técnica não exigida nos módulos anteriores).

## Classe `ComunidadesGastronomicas`

### Método `construir_grafo()`

Constrói um grafo não dirigido implícito (via `defaultdict`) ligando duas receitas sempre que elas compartilham pelo menos um ingrediente em comum (comparação case-insensitive).

### Método `dfs(vertice, visitados, componente)`

Busca em profundidade (DFS) recursiva clássica: marca o vértice como visitado, adiciona-o ao componente atual e chama-se recursivamente para cada vizinho ainda não visitado.

### Método `encontrar_comunidades()`

Percorre todas as receitas; para cada uma ainda não visitada, dispara uma nova DFS, descobrindo um **componente conexo** completo (uma "comunidade gastronômica" de receitas interligadas por ingredientes compartilhados). Cada chamada de DFS a partir de uma receita não visitada revela uma família culinária distinta.

Esse módulo foi o desafio avançado escolhido pelo grupo dentre as sugestões do Laboratório de Inovação do Chef ("Comunidades Gastronômicas"), utilizando uma técnica de análise de redes (componentes conexos via DFS) não exigida nos demais módulos.

**Complexidade:** O(N²) para a construção do grafo de similaridade (comparação de ingredientes entre todos os pares de receitas) e O(V + E) para a busca de componentes via DFS.

---

**Por que essa estrutura?** Por que DFS e não BFS para achar comunidades? Resultado equivalente para componentes conexos, mas DFS recursiva é mais simples de implementar aqui.

# Desafio Extra — Menu Especial Dia dos Namorados (`algorithms/menuNamorados.py`)

**Conteúdo aplicado:** Heurísticas e busca combinatória de otimização sob restrições, reaproveitando a base de receitas do sistema.

## Classe `MenuNamorados`

Trabalha apenas com receitas que possuem `classe` definida (Entrada, Principal ou Sobremesa) e `valor_venda` cadastrado.

### Método `_gerar_combinacoes()`

Filtra as receitas por classe e gera todas as combinações possíveis de (entrada, prato principal, sobremesa) — uma busca combinatória exaustiva sobre o espaço de menus viáveis.

### Método `_respeita_restricoes(combinacao, tempo_max, custo_max, dificuldade_max)`

Descarta combinações que ultrapassem o tempo total de preparo, o custo total ou a dificuldade logística máxima aceita (a dificuldade logística textual — Baixa/Média/Alta — é convertida para valor numérico via o dicionário `NIVEL_DIFICULDADE` para permitir a comparação).

### Método `_calcular_pontuacao(combinacao, criterio)`

Calcula a pontuação de cada combinação válida conforme o critério de otimização escolhido pelo usuário: maior lucro, melhor avaliação média, menor tempo de preparo, maior popularidade ou um critério de equilíbrio que combina lucro, avaliação e tempo em uma única fórmula ponderada.

### Método `montar_menu(...)`

Percorre todas as combinações geradas, descarta as que violam restrições e mantém a de maior pontuação segundo o critério escolhido — uma heurística de busca gulosa sobre o espaço de soluções viáveis, retornando o melhor menu encontrado (ou `None` caso nenhuma combinação seja viável).

### Método `justificar(combinacao, criterio)`

Monta a justificativa textual final, recalculando tempo total, custo total, valor de venda, lucro e avaliação média do menu escolhido, e gerando uma frase explicando por que aquele menu foi selecionado — exatamente no formato de saída pedido no enunciado.

**Complexidade:** O(E × P × S), onde E, P e S são, respectivamente, o número de entradas, pratos principais e sobremesas cadastrados — já que o algoritmo avalia exaustivamente todas as combinações possíveis entre as três classes.

---

**Por que essa estrutura?** Por que busca exaustiva de combinações e não uma heurística gulosa? O espaço de combinações é pequeno — poucas dezenas de entradas/principais/sobremesas, então força bruta garante o ótimo sem custo proibitivo; um guloso poderia perder combinações melhores.

# Integração com o `desafioMain.py`

O arquivo principal foi expandido (sem remover nada do T1) para:

- Carregar os arquivos `data/dependencias.json` e `data/logistica.json` e construir os respectivos grafos (`construirGrafoDependencias` e `construirGrafoLogistica`) logo na inicialização, junto com a Hash, a Trie e a Árvore B já existentes.
- Exibir três novas opções de menu ligadas aos grafos (5 - Oficina de Produção, 6 - Logística de Distribuição, 7 - Otimização de Cardápio) e duas ligadas aos demais algoritmos (8 - Comunidades Gastronômicas, 9 - Menu Especial Dia dos Namorados).
- Cada opção nova instancia a classe correspondente (`OficinaProducao`, `PlanejamentoLogistico`, `MenuVIP`, `ComunidadesGastronomicas`, `MenuNamorados`) e traduz a entrada/saída do usuário para os métodos descritos acima.

# Dimensão das estruturas utilizadas

- Grafo de dependências entre preparos (`dependencias.json`): 10 preparos intermediários + as receitas do sistema como vértices, com 60 arestas de pré-requisito (incluindo um ciclo proposital para validar a detecção de inconsistências).
- Grafo de logística (`logistica.json`): 8 regiões de entrega, 3 estações de preparo e 5 pontos de retirada como vértices (16 vértices), interligados por 66 rotas com peso (tempo) e capacidade.
- Base de receitas (`receita.json`): 56 receitas, reaproveitadas em todos os módulos novos (dependências, menu VIP, comunidades e menu dos namorados).

Ambas as redes atendem ao requisito mínimo de 30 vértices e 50 arestas somando o total de estruturas de grafo utilizadas no trabalho.

### Observações Requisitadas

6. Dimensões das Redes Utilizadas
O enunciado exige que as redes utilizadas tenham tamanho suficiente para demonstrar de forma consistente o funcionamento dos algoritmos (no mínimo 30 vértices e 50 arestas). A tabela a seguir resume as dimensões efetivamente usadas em cada módulo:
Rede
Vértices
Arestas
Observação
Grafo de dependências (Módulo 5)
65
60
55 receitas + 10 preparos-base
Grafo de logística (Módulo 7)
16
66
8 regiões + 3 estações + 5 pontos de retirada
Somadas, as duas redes totalizam 81 vértices e 126 arestas. Consideradas isoladamente, o grafo de dependências já ultrapassa o mínimo exigido em ambas as dimensões; o grafo de logística ultrapassa o mínimo de arestas, mas ainda está abaixo do mínimo de vértices — ponto registrado como melhoria futura na seção 8.
