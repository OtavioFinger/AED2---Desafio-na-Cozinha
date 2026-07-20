# Mapa auxiliar para conseguirmos comparar a dificuldade logística
# (que vem como texto: "Baixa", "Média", "Alta") como se fosse um número.
NIVEL_DIFICULDADE = {
    "Baixa": 1,
    "Média": 2,
    "Alta": 3
}


class MenuNamorados:
    def __init__(self, receitas):

        self.receitas = [
            r for r in receitas
            if getattr(r, "classe", None) and r.valor_venda is not None
        ]

    def _filtrar_por_classe(self, classe):
        return [r for r in self.receitas if r.classe == classe]

    def _gerar_combinacoes(self):

        entradas = self._filtrar_por_classe("Entrada")
        principais = self._filtrar_por_classe("Principal")
        sobremesas = self._filtrar_por_classe("Sobremesa")

        combinacoes = []

        for entrada in entradas:
            for principal in principais:
                for sobremesa in sobremesas:
                    combinacoes.append((entrada, principal, sobremesa))

        return combinacoes

    def _respeita_restricoes(self, combinacao, tempo_max, custo_max, dificuldade_max):
        tempo_total = sum(prato.tempo for prato in combinacao)
        custo_total = sum(prato.custo for prato in combinacao)

        dificuldade_total = max(
            NIVEL_DIFICULDADE.get(prato.dificuldade_logistica, 1)
            for prato in combinacao
        )

        if tempo_total > tempo_max:
            return False
        if custo_total > custo_max:
            return False
        if dificuldade_total > dificuldade_max:
            return False

        return True

    def _calcular_pontuacao(self, combinacao, criterio):
        lucro_total = sum(prato.valor_venda - prato.custo for prato in combinacao)
        avaliacao_media = sum(prato.avaliacao for prato in combinacao) / 3
        popularidade_total = sum(prato.popularidade for prato in combinacao)
        tempo_total = sum(prato.tempo for prato in combinacao)

        if criterio == "lucro":
            return lucro_total
        elif criterio == "avaliacao":
            return avaliacao_media
        elif criterio == "tempo":
            return -tempo_total  # queremos o MENOR tempo, por isso o sinal negativo
        elif criterio == "popularidade":
            return popularidade_total
        elif criterio == "equilibrio":
            # combina lucro, avaliação e tempo numa única pontuação (pesos definidos
            # de forma simples, poderiam ser ajustados conforme o relatório justificar)
            return (lucro_total * 0.5) + (avaliacao_media * 10) - (tempo_total * 0.2)
        else:
            return lucro_total

    def montar_menu(self, tempo_max, custo_max, dificuldade_max, criterio="lucro"):
        
        #Retorna a melhor combinação (entrada, principal, sobremesa) encontrada
        #e a pontuação obtida por ela, ou (None, None) se nenhuma combinação
        #respeitar as restrições informadas.
        
        melhor_combinacao = None
        melhor_pontuacao = float("-inf")

        for combinacao in self._gerar_combinacoes():
            if not self._respeita_restricoes(combinacao, tempo_max, custo_max, dificuldade_max):
                continue

            pontuacao = self._calcular_pontuacao(combinacao, criterio)

            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_combinacao = combinacao

        if melhor_combinacao is None:
            return None, None

        return melhor_combinacao, melhor_pontuacao

    def justificar(self, combinacao, criterio):
        #Monta um textinho simples explicando por que esse menu foi escolhido.
        entrada, principal, sobremesa = combinacao

        tempo_total = entrada.tempo + principal.tempo + sobremesa.tempo
        custo_total = round(entrada.custo + principal.custo + sobremesa.custo, 2)
        venda_total = round(entrada.valor_venda + principal.valor_venda + sobremesa.valor_venda, 2)
        lucro_total = round(venda_total - custo_total, 2)
        avaliacao_media = round((entrada.avaliacao + principal.avaliacao + sobremesa.avaliacao) / 3, 2)

        criterios_texto = {
            "lucro": "maior lucro estimado",
            "avaliacao": "melhor avaliação média",
            "tempo": "menor tempo total de preparo",
            "popularidade": "maior popularidade",
            "equilibrio": "melhor equilíbrio entre lucro, avaliação e tempo",
        }

        texto = (
            f"O menu foi escolhido priorizando {criterios_texto.get(criterio, criterio)}, "
            f"respeitando o tempo, custo e dificuldade logística informados. "
            f"O cardápio resultou em lucro estimado de R${lucro_total:.2f}, "
            f"avaliação média de {avaliacao_media} e tempo total de {tempo_total} minutos."
        )

        return {
            "tempo_total": tempo_total,
            "custo_total": custo_total,
            "venda_total": venda_total,
            "lucro_total": lucro_total,
            "avaliacao_media": avaliacao_media,
            "justificativa": texto,
        }
