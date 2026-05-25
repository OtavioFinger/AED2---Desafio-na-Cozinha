def recomendarReceitas(receitas, orçamento):

    receitasOrdenadas = sorted(receitas, key = lambda receita:(receita.avaliacao/receita.custo), reverse= True)

    receitasEscolhidas = []
    custoTotal = 0

    for receita in receitasOrdenadas:
        if custoTotal + receita.custo <= orçamento:
            receitasEscolhidas.append(receita)
            custoTotal += receita.custo
    
    return receitasEscolhidas  

# O algoritmo guloso foi escolhido para solucionar o problema das recomendações, usando ele para definir o melhor custo benefício entre receitas, tendo seu custo como O(n Logn)