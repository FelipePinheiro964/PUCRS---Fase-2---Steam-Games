
import pandas as pd

#seleção de arquivo
f = input('Digite o nome do arquivo: ')

#finalização forçada
if str.lower(f) == 'sair':
  SystemExit
  print('Saindo...')
else:
  tabela = pd.read_csv(f, sep=",")
  if tabela.empty:
    print('Arquivo vazio.')

match input('Digite o número da questão: '):
  case '0':
    SystemExit
  case '1':
    try: 
      questao_1 = tabela[['Name', 'Metacritic score', 'Release date']]
      if questao_1['Release date'].duplicated().any():  
        questao_1_order = questao_1.sort_values(by= 'Release date' and 'Metacritic score', ascending=True)# Mostra os 10 maiores
        display(questao_1_order.tail(n=10))                                                               #false mostrava os 10 menores
      else:
        questao_1_10 = questao_1.copy()
        top_10_maiores_notas = questao_1_10.nlargest(10, 'Metacritic score').sort_values(by='Metacritic score', ascending=False) # mostra os maiores por ter poucos dados
        display(top_10_maiores_notas.tail(n=10))
    except FileNotFoundError:
      print('Digite um nome válido')
