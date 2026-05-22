# T1 - Desafio na Cozinha

### Link do repositório: https://github.com/OtavioFinger/AED2---Desafio-na-Cozinha
### Por Arthur Trettin Bast e Otávio Finger

Cada receita deverá ter:
- nome
- categoria
- ingredientes
- ou (tempo de preparo, custo, avaliação ou popularidade).

*MÓDULOS DE SISTEMA:*

1. Livro de Receitas: carrega e faz a listagem das receitas (core)

2. Buscas Eficientes por nome ou ID, ou categoria ou prefixo da receita

3. Consulta por ingrediente.

*MÓDULO DE INTERAÇÃO (podem usar funções de outros módulos)*

MODOS DE INTERAÇÃO:

MODO INVESTIGAÇÃO (ver receitas corrompidas):

1. Permite encontrar inconsistências nas receitas armazenadas
(foi alterado desde o início da inserção)

2. (receitas com conteúdos errados ou duplicados)
(detectar conflitos com uma mesma receita)

3. (validar a integridade de dados a partir de aquivos ou API'S?????)

MODO CHEF (recomendar pratos sobre restrição)

1. Auxiliar na escolha de receitas ou composição dos menus.

2. Selecionar receitas com base em restrições

3. Obter sugestões de pratos considerando múltiplos critérios?????

4. Selecionar por popularidade (de boa)

5. Gerar combinações de receitas que sejam de menu econômico, menu rápido,...

MODO CONSULTA RÁPIDA (recuperação eficiente de receitas):

1. Usuário busca por noem (total ou parcial)

2. Filtrar receitas por categoria

3. Consultar receitas a partir de ingredientes específicos

4. Localizar receitas com base em "identificadores únicos?"



## Fonte dos Dados

A fonte de dados é um arquivo .JSON que contém os dados de 50 receitas (instruções de reparo). 
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
