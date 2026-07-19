class MenuVIP:
    def __init__(self, receitas):
        self.receitas = receitas

    def otimizar_menu(self, limite_tempo, limite_raros):
        tabela = [[(0.0, []) for _ in range(limite_raros + 1)] 
                  for _ in range(limite_tempo + 1)]
        
        for receita in self.receitas:
            tempo = receita['tempo']
            raros = receita['ingredientes_raros']
            lucro = receita['valor_venda'] - receita['custo']
            
            # Percorremos os limites de trás para frente para garantir que não vai receber a mesma receita duas vezes
            for t in range(limite_tempo, tempo - 1, -1):
                for r in range(limite_raros, raros - 1, -1):
                    
                    lucro_atual, menu_atual = tabela[t][r]
                    lucro_base, menu_base = tabela[t - tempo][r - raros]
                    
                    novo_lucro = lucro_base + lucro
                    
                    if novo_lucro > lucro_atual:
                        tabela[t][r] = (novo_lucro, menu_base + [receita])
                        
        return tabela[limite_tempo][limite_raros]