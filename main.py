import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#seleção de arquivo
f = input('Digite o nome do arquivo: ')

#finalização forçada
if str.lower(f) == 'sair':
  print('Saindo...')
  sys.exit('O sistema foi finalizado pelo usuario, inicie novamente para outro uso.') #utilizando o import sys

else:
  tabela = pd.read_csv(f, sep=",")
  if tabela.empty:
    print('Arquivo vazio.') #garantir que o arquivo possui dados

match input('Digite o número da questão: '): #seleção da função desejada

  case '0':
    print('Saindo...')
    sys.exit('O sistema foi finalizado pelo usuario, inicie novamente para outro uso.') #finalização forçada

  ###########################
  ######## QUESTÕES ########
  ###########################

  ## -- QUESTÃO 1
  case '1':

    try:
      questao_1 = tabela[['Name', 'Metacritic score', 'Release date']]

      if questao_1['Release date'].duplicated().any():
        questao_1_order = questao_1.sort_values(by= 'Release date' and 'Metacritic score', ascending=True)# Mostra os 10 maiores
        display(questao_1_order.tail(n=10))                                                               #false mostrava os 10 menores

      else:

        questao_1_10 = questao_1.copy()
        top_10_notas = questao_1_10.nlargest(10, 'Metacritic score').sort_values(by='Metacritic score', ascending=False) # mostra os maiores por ter poucos dados
        display(top_10_notas.tail(n=10))

    except FileNotFoundError:
      print('Digite um nome válido')

  ## -- QUESTÃO 2
  case '2':
 
          tabela_copy = tabela.copy() # Para nao perder dados, cria uma copia da tabela
          mask = tabela_copy['Genres'].str.contains('RPG', case=False, na=False) # Procura todos os generos RPG
          RPG = tabela_copy[mask] # Cria uma variavel RPG para facilitar leitura
          RPG = RPG.dropna(subset=['Genres']) # Retira qualquer genero None presente
          print('Neste arquivo, temos:')
          display(RPG)
          # Media e maximo de DLCs no genero
          print()

          #DLCs do Genero RPG
          max_DLC = RPG['DLC count'].max() # Mostra o maior valor de DLCs
          print(f'Para o genero RPG, temos {max_DLC:.2f} DLCs')

          media_DLC = RPG['DLC count'].mean() # Mostra a media de DLCs
          print(f'Em media, temos {media_DLC:.2f} DLCs presentes nesta categoria')

          print()

          #Media e maxima de avaliaçoes positivas
          max_positivas = RPG['Positive'].max() #mostra o maior valor de DLCs
          print(f'Tendo {max_positivas:.2f} avalições positivas')

          media_positivas = RPG['Positive'].mean()
          print(f'Em media, temos {media_positivas:.2f} avalições positivas!!')

          print()

          #Media e maxima de avaliaçoes positivas
          max_negativas = RPG['Negative'].max() #mostra o maior valor de DLCs
          print(f'Porém, temos {max_negativas:.2f} avalições negativas')

          media_negativas = RPG['Negative'].mean()
          print(f'Em media, temos {media_negativas:.2f} avalições negativas para esta categoria!')

          # Procuro por links (como mostra nos dados de cada coluna)
          def contar_links(celula):
            if pd.isnull(celula):
              return 0
            return celula.count('https') + celula.count('http')

          RPG['contador_Screenshots'] = RPG['Screenshots'].apply(contar_links)
          RPG['contador_Movies'] = RPG['Movies'].apply(contar_links)
          RPG['Total_links'] = RPG['contador_Screenshots'] + RPG['contador_Movies']
          print()

          # Calculo a media e maxima a partir da nova coluna
          max_midia = RPG['Total_links'].sum()
          media_total_links = RPG['Total_links'].mean()
          print(f'Para finalizar, temoos {max_midia:.0f} midias presentes!')
          print(f'Isto é em media {media_total_links:.2f} links!!')


  
  ## -- QUESTÃO 3
  case '3':

## 5 empresas com mais publi
    tabela_copy = tabela.copy() #copia de tabela para nao perder dados
    empresas = tabela_copy['Publishers'].value_counts()
    top5_empresas = empresas.head(5)

    top5_empresas_index = empresas.head(5).index

    top5_empresas_pagos = tabela_copy[
        (tabela_copy['Publishers'].isin(top5_empresas_index)) &
        (tabela_copy['Price'] > 0) #quebra de linhas para facilitar leitura
    ]


    media_positivas = top5_empresas_pagos.groupby('Publishers')['Positive'].mean()

    mediana_positivas = top5_empresas_pagos.groupby('Publishers')['Positive'].median()

    display(top5_empresas)
    display(media_positivas)
    display(mediana_positivas)

  ## -- QUESTÃO 4
  case '4':

    tabela_copy = tabela.copy()

    tabela_copy['Release date'] = pd.to_datetime(tabela_copy['Release date'], format='mixed', errors='coerce')


    jogos_2018_2022 = tabela_copy[(tabela_copy['Release date'].dt.year >= 2018) & (tabela_copy['Release date'].dt.year <= 2022)]
    contagem_linux = jogos_2018_2022[jogos_2018_2022['Linux']].groupby(jogos_2018_2022['Release date'].dt.year).size()

    display(contagem_linux)

    crescimento = contagem_linux.diff().dropna()  # Calcula a diferença ano a ano
    cresceu = crescimento > 0  # Verifica se a diferença é positiva


    display(crescimento)


  ###########################
  ######## GRAFICOS #########
  ###########################

  ## -- GRAFICO 1
  case '5':
    sist_op = tabela.copy()

    contagem_sistemas = {
        'Windows': sist_op['Windows'].sum(),
        'Linux': sist_op['Linux'].sum(),
        'Mac': sist_op['Mac'].sum()
    }

    contagem_sistemas_df = pd.DataFrame(list(contagem_sistemas.items()), columns=['Sistema Operacional', 'Quantidade'])

    total_jogos = len(sist_op)
    contagem_sistemas_df['Porcentagem'] = (contagem_sistemas_df['Quantidade'] / total_jogos)

    ## Plot do grafico

    plt.figure(figsize=(10,6))
    contagem_sistemas_df.set_index('Sistema Operacional')['Porcentagem'].plot(kind='bar', color=['blue', 'orange', 'green'])
    plt
    plt.title('Porcentage para sistemas operacionais')
    plt.ylabel('Porcentagem')
    plt.xlabel('Sistema Operacional')
    plt.xticks(rotation=50)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
