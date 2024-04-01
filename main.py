import random

# Definição dos dados do problema
analises = {
    'Análise 1': ['Espectrofotômetro UV-VIS', 'Cromatógrafo Gasoso'],
    'Análise 2': ['Cromatógrafo Líquido', 'Espectrômetro Infravermelho'],
    'Análise 3': ['Microscópio', 'Balança Analítica'],
    'Análise 4': ['Espectrômetro de Massa'],
    'Análise 5': ['Agitador Magnético', 'Espectrômetro Infravermelho'],
    'Análise 6': ['Cromatógrafo Líquido', 'Espectrofotômetro UV-VIS'],
    'Análise 7': ['Espectrofotômetro UV-VIS', 'Microscópio'],
    'Análise 8': ['Cromatógrafo Gasoso'],
    'Análise 9': ['Espectrômetro Infravermelho', 'Balança Analítica'],
    'Análise 10': ['Espectrômetro de Massa', 'Cromatógrafo Gasoso']
}

equipamentos = {
    'Balança Analítica': 6,
    'Agitador Magnético': 4,
    'Cromatógrafo Líquido': 8,
    'Cromatógrafo Gasoso': 6,
    'Espectrofotômetro UV-VIS': 4,
    'Espectrômetro Infravermelho': 6,
    'Espectrômetro de Massa': 4,
    'Microscópio': 6
}

horas_dia = 8
dias_semana = 6
dias = [
    'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
    'Sexta-feira', 'Sábado', 'Domingo'
]


# Função de geração de indivíduos (plano de uso dos equipamentos na semana)
def gerar_individuo():
  plano_semana = []
  for dia in range(dias_semana):
    plano_dia = {}
    for hora in range(horas_dia):
      if hora != 2:  # Hora de almoço, das 12h às 13h, sem análises
        analises_hora = random.sample(list(
            analises.keys()), random.randint(1, len(
                analises)))  # Agora pode ter mais de duas análises por hora
        plano_dia[hora] = analises_hora
    plano_semana.append(plano_dia)
  return plano_semana


# Função de avaliação de aptidão (fitness) - número de análises simultâneas em cada hora
def calcular_fitness(individuo):
  uso_equipamento = {
      equipamento: {
          dia: 0
          for dia in range(dias_semana)
      }
      for equipamento in equipamentos
  }
  for dia in range(dias_semana):
    for hora in range(horas_dia):
      if hora in individuo[
          dia]:  # Se houver análises programadas para esta hora
        analises_hora = individuo[dia][hora]
        for analise in analises_hora:
          for equipamento in analises[analise]:
            if uso_equipamento[equipamento][dia] < equipamentos[
                equipamento]:  # Verifica se o equipamento ainda pode ser usado
              uso_equipamento[equipamento][dia] += 1
            else:
              break
  num_analises_simultaneas = [
      max(values.values()) for values in uso_equipamento.values()
  ]
  return sum(num_analises_simultaneas)


# Funções de crossover e mutação
def crossover(individuo1, individuo2):
  ponto_corte = random.randint(1, dias_semana - 1)
  filho1 = individuo1[:ponto_corte] + individuo2[ponto_corte:]
  filho2 = individuo2[:ponto_corte] + individuo1[ponto_corte:]
  return filho1, filho2


def mutacao(individuo):
  dia = random.randint(0, dias_semana - 1)
  hora = random.randint(0, horas_dia - 1)
  if hora != 2:  # Não mutar a hora do almoço
    individuo[dia][hora] = random.sample(
        list(analises.keys()),
        random.randint(1, len(analises)))  # No máximo duas análises por hora
  return individuo


# Algoritmo genético
def algoritmo_genetico(tamanho_populacao, taxa_mutacao, num_geracoes):
  populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
  for _ in range(num_geracoes):
    populacao = sorted(populacao, key=lambda x: calcular_fitness(x))
    melhores_pais = populacao[:tamanho_populacao // 2]
    nova_geracao = melhores_pais.copy()

    while len(nova_geracao) < tamanho_populacao:
      pai1, pai2 = random.choices(melhores_pais, k=2)
      filho1, filho2 = crossover(pai1, pai2)
      if random.random() < taxa_mutacao:
        filho1 = mutacao(filho1)
      if random.random() < taxa_mutacao:
        filho2 = mutacao(filho2)
      nova_geracao.append(filho1)
      nova_geracao.append(filho2)

    populacao = nova_geracao

  melhor_solucao = min(populacao, key=calcular_fitness)
  return melhor_solucao


# Função para calcular o uso de cada equipamento em cada dia
def calcular_uso_equipamento(individuo):
  uso_equipamento = {
      equipamento: {
          dia: 0
          for dia in range(dias_semana)
      }
      for equipamento in equipamentos
  }
  for dia in range(dias_semana):
    for hora in range(horas_dia):
      if hora in individuo[
          dia]:  # Se houver análises programadas para esta hora
        analises_hora = individuo[dia][hora]
        for analise in analises_hora:
          for equipamento in analises[analise]:
            if uso_equipamento[equipamento][dia] < equipamentos[
                equipamento]:  # Verifica se o equipamento ainda pode ser usado
              uso_equipamento[equipamento][dia] += 1
  return uso_equipamento


# Execução do algoritmo genético
if __name__ == "__main__":
  tamanho_populacao = 50
  taxa_mutacao = 0.1
  num_geracoes = 100

  melhor_solucao = algoritmo_genetico(tamanho_populacao, taxa_mutacao,
                                      num_geracoes)
  melhor_fitness = calcular_fitness(melhor_solucao)
  uso_equipamento = calcular_uso_equipamento(melhor_solucao)

  print("Melhor plano de uso dos equipamentos na semana:")
  for dia, plano_dia in enumerate(melhor_solucao, start=1):
    print(f"\n{dias[dia - 1]}:")
    for hora in range(horas_dia):
      if hora in plano_dia:
        analises_hora = plano_dia[hora]
        print(
            f"  Hora {hora + 10 if hora < 2 else hora + 11}:00 - {', '.join(analises_hora)}"
        )

    print("\nUso de cada equipamento no dia:")
    for equipamento, uso_dias in uso_equipamento.items():
      uso = uso_dias[dia - 1]
      horas_uso = [
          hora for hora in range(horas_dia)
          if hora in plano_dia and any(equipamento in analises[analise]
                                       for analise in plano_dia[hora])
      ]
      print(
          f"  {equipamento}: {uso} horas (disponível: {equipamentos[equipamento]} horas, sobra: {equipamentos[equipamento] - uso} horas, horas de uso: {', '.join(str(hora + 10 if hora < 2 else hora + 11) for hora in horas_uso)})"
      )

  print("\nFitness da melhor solução:", melhor_fitness)
