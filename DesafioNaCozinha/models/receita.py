class Receita:
    def __init__(self, id, nome, categoria, ingredientes, tempo, custo, dificuldade, avaliacao, popularidade,
                 classe="Principal", ingredientes_raros=0, dificuldade_logistica="Baixa",
                 valor_venda=None, dependencias=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.tempo = tempo
        self.custo = custo
        self.dificuldade = dificuldade
        self.avaliacao = avaliacao
        self.popularidade = popularidade
        self.classe = classe
        self.ingredientes_raros = ingredientes_raros
        self.dificuldade_logistica = dificuldade_logistica
        self.valor_venda = valor_venda
        self.dependencias = dependencias if dependencias is not None else []

    def lucro(self):
        if self.valor_venda is None:
            return None
        return round(self.valor_venda - self.custo, 2)