# T1 - Desafio na Cozinha

### Link do repositório: https://github.com/OtavioFinger/AED2---Desafio-na-Cozinha
### Por Arthur Trettin Bast e Otávio Finger

# Introdução

    O projeto atual visa explorar todos os conceitos vistos nas aulas de Algoritmos e Estruturas de Dados II, ministrada pela Professora Brenda Salenave Santana.
    
    O objetivo do mesmo é implementar um sistema que use diferentes estruturas de dados como Tries, Tabelas Hash, Árvores B, bem como as versões variadas de cada uma das estruturas citadas. Além disso, deverá ser implementando alguma forma de Algoritmo Guloso em recomendação, busca ou otimização.

    Nesse sistema fictício de um restaurante/cozinha, será possível pelo usuário acessar os modos:

    1- Buscar receita por ingrediente
    2- Buscar receita por nome
    3- Recomendar receita
    4- Modo Investigação
    5- Sair

    Os modos tem por objetivo guiar o usuário (cozinheiro, auxiliar e etc) pelo menu do restaurante, sendo capaz de realizar ações como:

    1- Buscar receita por ingrediente: Utiliza inteiramente os conceitos de Tabelas Hash para buscar pratos que contenham determinado ingrediente na língua inglesa, retornando todas as receitas que contenham o determiando ingrediente.

    2- Buscar receita por nome: Utiliza conceitos de Árvores Trie para buscar receitas por prefixos ou por seus nomes completos, devolvendo uma impressão com os mesmos.

    3- Recomendar receita:

    4- Modo Investigação: Utiliza inteiramente conceitos de Árvore B, armazenando as receitas em RAM e buscando-as. Por ele, é possível buscar e verificar duplicadas de receitas a partir de seu ID

    5- Sair: Encerra o sistema, sendo preciso executar novamente o arquivo main para reacessar o menu.

    As especicações do código de cada um dos módulos será descrito nos seus respectivos tópicos.

# Instruções de Compilação e Execução

    Primeiro, é preciso realizar um checklist com relação á:

    1. Python 3.6+ instalado no sistema operacional?
    2. Tenho baixo o arquivo *AED2 - Desafio na Cozinha*?

    **Obs: A pasta principal que abre o menu proposto pela atividade é "DesafioNaCozinha", que está dentro de "AED2 - Desafio na Cozinha".**

    Com isso, o comando usado, após descompactar a pasta *AED2 - Desafio na Cozinha* é:

    ```
    cd DesafioNaCozinha && python desafioMain.py
    ```

    Com isso, o arquivo principal que contém o menu, o "desafioMain,py" será aberto:

        =======Bem vindo=======
    --Menu--
    1- Buscar receita por ingrediente
    2- Buscar receita por nome
    3- Recomendar receita
    4- Modo Investigação
    5- Sair
    Escolha uma opção: 

## Fonte dos Dados: data

Dentro da pasta  fonte de dados é um arquivo .JSON denominado *receita.json* que contém os dados de 50 receitas (instruções de reparo). 
Abaixo está um exemplo de uma receita:

```{
        "id": 1,
        "nome": "Flan",
        "categoria": "Dessert",
        "ingredientes": [
            "Sugar",
            "Milk",
            "Sugar",
            "vanilla pod",
            "Egg Yolks",
            "Egg",
            "Dulce de leche"
        ],
        "tempo": 41,
        "custo": 26.54,
        "dificuldade": "Média",
        "avaliacao": 4.0,
        "popularidade": 210
    },
```
## models

## structs

# desafioMain.py

# tempCodeRunnerFile.py