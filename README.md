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
    │ ├── testarDisco.py
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

Este arquivo implementa toda a lógica da Árvore B utilizada no sistema. A estrutura é responsável principalmente pelo **Modo Investigação**, além de também realizar buscas eficientes por ID das receitas.

A Árvore B foi escolhida por ser uma estrutura de busca balanceada e extremamente eficiente para grandes volumes de dados. Diferente de árvores binárias comuns, cada nó pode armazenar múltiplas chaves e múltiplos filhos, reduzindo a altura da árvore e diminuindo a quantidade de acessos necessários durante buscas.

Nesta implementação, cada nó pode armazenar até 3 chaves e possuir até 4 filhos.

As receitas são organizadas utilizando o atributo `id`, permitindo localizar rapidamente qualquer receita sem percorrer toda a lista carregada do JSON.

Além da implementação tradicional da Árvore B, este arquivo também foi adaptado para a **Opção C da recuperação**, implementando persistência em memória secundária utilizando arquivos binários (`.dat`).

A estrutura foi modificada para simular o funcionamento de sistemas reais de banco de dados e armazenamento em disco, onde cada nó da árvore representa um bloco/página de memória secundária.

---

### Classe NodoB

A classe `NodoB` representa cada nó da Árvore B.

Cada nodo possui:

1. `idBloco`
2. `folha`
3. `chaves`
4. `filhos`

O atributo `idBloco` funciona como um identificador único do bloco no disco. Esse identificador é utilizado para localizar os nós durante as buscas realizadas diretamente no arquivo binário.

O atributo `folha` indica se aquele nodo é um nó folha ou interno.

A lista `chaves` armazena os objetos de receitas organizados de forma ordenada pelo ID.

Já a lista `filhos` armazena as referências para os nós filhos daquele bloco.

A variável estática `contadorIds` é utilizada para gerar IDs únicos automaticamente para cada novo bloco criado na árvore.

---

### Método inserir()

O método `inserir()` é responsável por adicionar novas receitas na Árvore B.

Antes de inserir, o sistema verifica se já existe uma receita com o mesmo ID utilizando a busca em memória:

```python
if self.buscarMemoria(self.raiz, receita.id) is not None:
    return
```

Isso impede duplicações dentro da estrutura.

Caso a raiz esteja cheia, ocorre o processo de divisão (`split`) do nó raiz, criando uma nova raiz e reorganizando os filhos da árvore.

Essa divisão mantém a Árvore B balanceada durante toda a execução.

---

### Método inserirNaoCheio()

Este método realiza a inserção propriamente dita em nós que ainda possuem espaço disponível.

Se o nodo for folha, a receita é inserida diretamente na posição correta, mantendo as chaves ordenadas pelo ID.

Caso o nodo não seja folha, o algoritmo determina qual filho deve receber a inserção.

Se o filho estiver cheio, ocorre um `split` antes de continuar a inserção.

Esse processo garante que a árvore continue balanceada mesmo após múltiplas inserções.

---

### Método dividirFilho()

O método `dividirFilho()` implementa o processo de divisão de nós da Árvore B.

Quando um nodo atinge o limite máximo de chaves, ele é dividido em dois blocos menores.

O elemento central sobe para o nó pai, enquanto as demais chaves são separadas entre os dois filhos.

Esse mecanismo é o principal responsável pelo balanceamento automático da Árvore B.

---

### Método buscarMemoria()

O método `buscarMemoria()` realiza buscas tradicionais diretamente na estrutura carregada na RAM.

A busca percorre os nós comparando o ID desejado com as chaves armazenadas até localizar a receita correta ou determinar que ela não existe.

Esse método é utilizado principalmente durante inserções e no Modo Investigação.

---

### Persistência em Disco

A principal modificação realizada na recuperação foi a implementação da persistência em memória secundária.

Anteriormente, toda a árvore era serializada diretamente utilizando:

```python
pickle.dump(self.raiz, arquivo)
```

Essa abordagem salvava toda a estrutura de memória RAM de uma única vez, não representando corretamente o funcionamento de uma Árvore B em sistemas reais.

Na nova implementação, cada nodo passou a ser tratado como um bloco/página de disco independente.

Cada bloco armazena:

- identificador do bloco;
- informação de folha;
- chaves armazenadas;
- IDs dos filhos.

Esses dados são serializados individualmente no arquivo `.dat`.

---

### Método salvarNodo()

O método `salvarNodo()` salva cada bloco da árvore individualmente no arquivo binário.

Os filhos não são armazenados diretamente como objetos, mas apenas pelos seus IDs de bloco.

Isso permite simular referências de páginas em memória secundária.

Após salvar o bloco atual, o método continua recursivamente salvando todos os filhos da árvore.

---

### Método salvarEmDisco()

O método `salvarEmDisco()` é responsável por persistir toda a estrutura da Árvore B no arquivo `.dat`.

Além dos blocos, o sistema salva também os metadados da árvore, principalmente o ID do bloco raiz.

Essas informações permitem reconstruir a navegação da árvore posteriormente sem necessidade de reinserir todas as receitas.

---

### Método carregarBlocos()

Este método lê o arquivo binário e reconstrói os blocos armazenados.

Primeiramente, os metadados são carregados para recuperar o ID da raiz.

Em seguida, todos os blocos persistidos são carregados para um dicionário interno.

Cada bloco é indexado pelo seu `idBloco`, permitindo acesso rápido durante as buscas.

---

### Método carregarDoDisco()

O método `carregarDoDisco()` realiza a recuperação da árvore diretamente do arquivo binário.

Se o arquivo não existir, o sistema informa que a árvore ainda não foi persistida.

Caso exista, os blocos são carregados e a árvore passa a funcionar utilizando os dados armazenados em disco.

Esse método permite inicializar o sistema sem reconstruir toda a árvore na RAM.

---

### Método carregarNodo()

O método `carregarNodo()` reconstrói um nodo específico a partir dos dados persistidos.

A partir do `idBloco`, o sistema recupera as informações do bloco correspondente e recria o nodo dinamicamente.

Esse comportamento simula operações reais de leitura de páginas de disco.

---

### Método buscar()

O método `buscar()` inicia o processo de busca diretamente no disco.

A busca começa a partir do bloco raiz carregado nos metadados da árvore.

---

### Método buscarDisco()

O método `buscarDisco()` implementa a navegação da Árvore B utilizando os blocos persistidos.

A cada etapa da busca:

1. um bloco é carregado;
2. as chaves são verificadas;
3. o próximo filho é determinado;
4. um novo bloco é acessado.

Durante a execução, mensagens como:

```text
[DISCO] Bloco X acessado
```

são exibidas para demonstrar os acessos simulados à memória secundária.

Esse processo representa o funcionamento de Árvores B utilizadas em bancos de dados e sistemas de arquivos reais.

---

### Método modoInvestigacao()

O método `modoInvestigacao()` é utilizado para verificar inconsistências nas receitas carregadas no sistema.

Ele identifica:

- receitas duplicadas;
- receitas alteradas após a inserção na árvore.

Para isso, o sistema percorre todas as receitas e compara o estado atual dos dados com o estado originalmente armazenado na Árvore B.

A comparação é feita utilizando o método `resumoReceita()`, que gera uma representação textual dos dados da receita.

Caso existam diferenças entre os dados atuais e os dados armazenados originalmente, a receita é marcada como alterada.

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

## [RECUPERAÇÃO P1]

### Questão Escolhida

A dupla escolheu recuperar a:

```text
Opção C: Árvores B e Simulação de Memória Secundária (I/O)
```

O objetivo da recuperação foi adaptar a implementação da Árvore B para funcionar com persistência em disco utilizando arquivos binários (`.dat`), simulando o comportamento de páginas/blocos de memória secundária utilizados em bancos de dados e sistemas de arquivos reais.

---

### Explicação Teórica e Arquitetural

Inicialmente, a Árvore B estava sendo salva utilizando serialização completa da estrutura em memória RAM:

```python
pickle.dump(self.raiz, arquivo)
```

Apesar de funcional, essa abordagem não simulava corretamente o funcionamento de uma Árvore B em memória secundária, pois toda a árvore era carregada de uma única vez.

Após a recuperação, a implementação foi reformulada para:

- salvar cada nó individualmente como um bloco de disco;
- utilizar identificadores de blocos (`idBloco`);
- armazenar referências lógicas entre os nós;
- carregar os nós sob demanda durante a busca;
- permitir buscas diretamente no arquivo binário sem reinserção das receitas.

Cada nó passou a representar uma página/bloco de disco contendo:

- informações da folha;
- chaves armazenadas;
- referências para os filhos.

Durante as buscas, o sistema carrega apenas os blocos necessários, simulando operações reais de I/O.

A busca passou a funcionar da seguinte forma:

```text
buscar(id)
    ↓
carregar bloco do disco
    ↓
verificar chaves
    ↓
navegar para próximo bloco
```

Durante a execução, o sistema exibe mensagens como:

```text
[DISCO] Bloco X acessado
```

demonstrando os acessos simulados à memória secundária.

Essa recuperação permitiu compreender melhor:

- o motivo do uso de Árvores B em bancos de dados;
- a relação entre Árvores B e hardware;
- o conceito de páginas/blocos;
- a importância da redução de operações de I/O.

---

### Passo a Passo para Execução

### 1. Remover o arquivo antigo

Excluir:

```text
DesafioNaCozinha/data/arvore.dat
```

Isso garante que a árvore seja recriada no novo formato baseado em blocos.

---

### 2. Executar o sistema principal

Comando:

```bash
python desafioMain.py
```

Na primeira execução, o sistema irá:

- carregar o JSON;
- construir a Árvore B;
- salvar os blocos no arquivo `arvore.dat`.

Saída esperada:

```text
Árvore criada e salva em disco!
```

---

### 3. Executar novamente

Executar novamente:

```bash
python desafioMain.py
```

Agora a árvore será carregada diretamente do disco.

Saída esperada:

```text
Árvore carregada do disco com sucesso!
```

---

### 4. Testar a memória secundária

Executar:

```bash
python testarDisco.py
```

O sistema iniciará com a RAM limpa e utilizará apenas os blocos persistidos no arquivo binário.

Saída esperada:

```text
RAM iniciada limpa. Árvore carregada apenas do disco.
```

---

### 5. Realizar buscas

Inserir um ID de receita válido.

Exemplo:

```text
Digite o ID da receita que deseja buscar: 10
```

Durante a busca, o sistema exibirá mensagens indicando os acessos aos blocos:

```text
[DISCO] Bloco X acessado
[DISCO] Navegando para bloco filho
```

Ao final, os dados da receita serão retornados diretamente da estrutura persistida em disco.