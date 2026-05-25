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
    2. Tenho baixado o arquivo *AED2 - Desafio na Cozinha*?

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

# Estruturação e Função dos Arquivos

Nesta seção, cada arquivo principal do projeto será explicado individualmente, detalhando sua responsabilidade, funcionamento interno, principais funções e relação com o restante do sistema.

    AED2 - Desafio na Cozinha/
    │
    ├── README.md
    ├── DesafioNaCozinha/
    │ ├── desafioMain.py
    │ ├── data/
    │ │ └── receita.json
    │ ├── models/
    │ │ ├── receita.py
    │ │ └── recomendacao.py
    │ └── structs/
    │ ├── hash.py
    │ ├── trie.py
    │ └── arvoreB.py

## Fonte dos Dados: data

Dentro da pasta  fonte de dados é um arquivo .JSON denominado *receita.json* que contém os dados de 50 receitas (instruções de reparo). 

Essa pasta está localizada em: 
```
DesafioNaCozinha/data/receita.json
```

Cada receita possui os seguintes campos:
- id
- nome
- categoria
- ingredientes
- tempo
- custo
- dificuldade
- avaliacao
- popularidade

Abaixo está um exemplo de uma receita:

```
{
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

## models/receita.py

    Esse arquivo serve para definir a classe da receita, a entidade principal do sistema. A classe criada como Receita somente possui seus atributos, sem métodos. 

    ```
    class Receita:
    def __init__(self, id, nome, categoria, ingredientes, tempo, custo, dificuldade, avaliacao, popularidade):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.tempo = tempo
        self.custo = custo
        self.dificuldade = dificuldade
        self.avaliacao = avaliacao
        self.popularidade = popularidade
    ```  

    Ela é compartilhada com *recomendacao.py* e os arquivos das outras estruturas de dados que veremos  a seguir.

## models/recomendacao.py

    A função é ser um "Modo de Recomendação", responsável por sugerir receitas com base em critérios de melhor custo-benefício. O algoritmo faz isso utilizando conceitos de Algoritmos Gulosos.

    *Obs: Sendo uma implementação de um algoritmo guloso para recomendar receitas, ele não garante a solução perfeita global.

    Isso ocorre ao perguntar qual o orçamento máximo do usuário, sendo assim, o algoritmo calcula:

    ```
    key = lambda receita:(receita.avaliacao/receita.custo)
    ```

    Recebe a lista completa de receitas e um valor de orçamento máximo definido pelo usuário, e retorna quais receitas devem ser escolhidas para maximizar a qualidade dentro daquele
orçamento.

## structs/hash.py

    Este arquivo implementa a Tabela Hash do zero, responsável pelo Módulo 3 — Organização dos
    Ingredientes. A Tabela Hash permite associar ingredientes às receitas e recuperar essa associação
de forma muito rápida, independente de quantas receitas estejam cadastradas.

Cria uma tabela com 103 posições. Cada posição pode guardar vários ingredientes sem
perder nenhum, mesmo que dois ingredientes diferentes acabem no mesmo índice, o arquivo resolve o problema com tratamento de *Colisão por Encadeamento*.

### Método: hash(self, chave):
    O método é quem calcula o índice onde vai aquele ingrediente. 
    Ele faz isso somando os valores numéricos de cada letra e aplica o resto da divisão por 103. Assim, cada ingrediente sempre vai pro mesmo índice,

## Método: inserir(self, ingrediente, receita):

Essa função serve para *associar um ingrediente com determinada receita dentro da tabela*.

Calcula a posição do ingrediente usando hash(). Vai até essa posição na tabela e
verifica se o ingrediente já existe ali. Se já existir, apenas adiciona a nova receita à lista que já está
associada a ele. Se não existir, cria uma nova entrada com o ingrediente e uma lista contendo a
receita. Isso garante que o mesmo ingrediente nunca seja duplicado na tabela e que todas as
receitas que o usam fiquem agrupadas.

### Método buscar(self, ingrediente):

Retorna todas as receitas que contêm um ingrediente específico. *É chamado quando o
usuário escolhe a opção 1 no menu*.

Calcula a posição do ingrediente com hash(), vai diretamente para aquela posição na
tabela e procura o ingrediente. Se encontrar, retorna a lista de receitas associadas associadas ao índice daquela receita. Se não encontrar, retorna uma lista vazia. Por ir direto à posição correta sem precisar percorrer toda a tabela, a busca é extremamente rápida.

## structs/trie.py

Este arquivo implementa a estrutura Trie, responsável pelo *Módulo 2 — Busca Rápida no
Cardápio.* A Trie é uma árvore onde cada nó representa uma letra, e o caminho percorrido da raiz
até um nó final forma o nome completo de uma receita. Isso permite encontrar todas as receitas
que começam com um determinado prefixo de forma muito eficiente.

### Método inserir(self, palavra):

Tem por função inserir Insere o nome de uma receita na Trie letra por letra.

Começa na raiz e percorre cada letra do nome. Se a letra ainda não existe como filho do
nó atual, cria um novo espaço para ela. Ao chegar na última letra, marca aquele nó como final
para indicar que ali termina um nome de receita completo.

### Método buscar(self, prefixo):

Recebe o texto digitado pelo usuário e retorna todos os nomes de receitas que
começam com aquele texto. **É chamado quando o usuário escolhe a opção 2 no menu.**

Navega pela Trie seguindo as letras do prefixo digitado. Se em algum ponto uma letra
não existe na árvore, retorna lista vazia pois nenhuma receita começa com aquele prefixo. Se
chegar ao fim do prefixo com sucesso, chama a próxima função, autocomplete() para coletar todos os nomes que
continuam a partir daquele ponto.

### Método autocomplete autocomplete(self, nodo, prefixo, palavras):

Percorre todos os filhos do nó recebido. Sempre que encontra um nó
com final igual a verdadeiro, adiciona o nome formado até ali na lista de palavras. Dessa forma,
todos os nomes que começam com o prefixo digitado são coletados automaticamente.

## structs/arvoreB.py

Este arquivo implementa a Árvore B do zero, responsável pelo Modo Investigação. **A Árvore B é
uma estrutura de busca ordenada onde cada nó pode guardar até 3 chaves e ter até 4 filhos**. As
receitas são indexadas pelo ID, o que permite localizar qualquer receita de forma eficiente sem
percorrer a lista inteira. Além de armazenar cada receita, a árvore guarda também um resumo do
conteúdo dela no momento da inserção, que é usado posteriormente para detectar alterações.

### Classe NodoB:

Cada nó possui dois atributos. 

1. O primeiro é chaves, uma lista de tuplas onde cada tupla
guarda três coisas: 

1.1 O ID da receita, 
1.2 O objeto receita completo 
1.3 O resumo do conteúdo dela no momento da inserção. 

2. O segundo é filhos, uma lista com os nós filhos daquele nó. 

## desafioMain.py

Este é o arquivo principal do sistema. Ele une todos os outros módulos, carrega os dados, inicializa
as estruturas e exibe o menu de interação para o usuário. **É o único arquivo que precisa ser
executado para rodar o sistema.**

### Bloco de carregamento do JSON

Lê o arquivo receita.json e transforma cada entrada em um objeto Receita, populando a
lista receitas que é o repositório central do sistema.

### Bloco de Inicialização de Estruturas

Esse bloco tem por objetivo ler o arquivo receita.json e transformar cada entrada em u objeto Receita de uma lista, que depois será utilizado por:

[] Hash: Criada vazia e populada chamando adicionarIngredientes() com a lista receitas.

[] Trie: Criada vazia e populada com um laço que chama trie.inserir() para cada nome de receita.

[] Árvore B: Criada vazia e populada com um laço que chama arvore.inserir() para cada receita.

### Opção 1: Buscar por Ingrediente

Converte o texto digitado para minúsculas e chama tabelaIngredientes.buscar(). Se a
lista retornada estiver vazia, exibe mensagem de não encontrado. Caso contrário, exibe os nomes
de cada receita retornada, que estava na lista associada por aquele ingrediente na Hash.

### Opção 2: Buscar por nome

Converte o texto digitado pelo usuário para minúsculas e chama trie.buscar(). Se a lista retornada estiver
vazia, exibe mensagem de não encontrado. Caso contrário, exibe os nomes encontrados.

### Opção 3: Recomendar receita

Pede ao usuário um valor de orçamento máximo e exibe as receitas recomendadas
dentro daquele limite.
Em seguida, converte o valor digitado para número decimal e chama recomendarReceitas()
passando a lista receitas e o orçamento. Para cada receita retornada exibe o nome, o custo e a
avaliação.

### Opção 4: Modo Investigação

O Modo Investigação é implementado somente por Árvore B. Ele verifica a integridade das receitas cadastradas, identificando duplicatas e receitas que
foram alteradas após a inserção no sistema.

 Chama arvore.modoInvestigacao() passando a lista receitas. Recebe de volta duas
listas — duplicatas e alteradas. Se ambas estiverem vazias, exibe que nenhuma inconsistência foi
encontrada. Se houver duplicatas, lista os nomes e IDs das receitas duplicadas. Se houver
alteradas, lista os nomes e IDs das receitas que tiveram seu conteúdo mudado.

### Opção 5: Sair 

Encerra o programa exibindo uma mensagem de despedida e interrompendo o laço
principal do menu com break.