import pandas as pd
import re
import unicodedata
import sqlite3

# Ler a aba CMVCol taco3 do arquivo Excel
table = pd.read_excel('taco.xlsx', sheet_name='CMVCol taco3', header=[0, 1, 2])

# Combinar as três primeiras linhas do cabeçalho em uma única linha
table.columns = [' '.join(map(str, col)).strip()
                 for col in table.columns.values]

# Remove a string "Unnamed: \n_level_\n" em que \n corresponde a um número
table.columns = [re.sub(r'Unnamed:\s\d+_level_\d+\s', '', col)
                 for col in table.columns]

# Renomear a coluna 'Número do Descrição dos alimentos' para 'Descrição do Alimento'
table.rename(columns={
             'Número do Descrição dos alimentos': 'Descrição do Alimento'}, inplace=True)

# Remover linhas com valores nulos
table.dropna(subset=['Número do Alimento'], inplace=True)
table['Número do Alimento'] = table['Número do Alimento'].astype(
    str)  # Converte a coluna 'Número do Alimento' para string
# Remove linhas que contém a string 'Número do'
table = table[~table['Número do Alimento'].str.contains('Número do')]
# Remove linhas que contém a string 'Alimento'
table = table[~table['Número do Alimento'].str.contains('Alimento')]

# Se a coluna 'Descrição do Alimento' for nula, então a coluna 'Tipo do alimento' recebe o valor da coluna 'Número do Alimento', caso contrário, recebe NA
table['Tipo do alimento'] = table.apply(
    lambda row: row['Número do Alimento'] if pd.isna(row['Descrição do Alimento']) else pd.NA, axis=1
).ffill()

# Remove linhas com valores nulos na coluna 'Descrição do Alimento'
table.dropna(subset=['Descrição do Alimento'], inplace=True)
# Remove linhas com valores nulos na coluna 'Número do Alimento'
table.dropna(subset=['Número do Alimento'], inplace=True)


# Ler o arquivo Excel na aba AGtaco3
fats = pd.read_excel('./taco.xlsx', sheet_name='AGtaco3', header=[0, 1, 2])

# Combinar as três primeiras linhas do cabeçalho em uma única linha
fats.columns = [' '.join(map(str, col)).strip() for col in fats.columns.values]

# Remove a string "Unnamed: \n_level_\n" em que \n corresponde a um número
fats.columns = [re.sub(r'Unnamed:\s\d+_level_\d+\s', '', col)
                for col in fats.columns]
# Renomear a coluna 'Número do Descrição dos alimentos' para 'Descrição do Alimento'
fats.rename(columns={
            'Número do Descrição dos alimentos': 'Descrição do Alimento'}, inplace=True)

fats.dropna(subset=['Número do Alimento'], inplace=True)

fats['Número do Alimento'] = fats['Número do Alimento'].astype(str)
fats = fats[~fats['Número do Alimento'].str.contains('Número do')]
fats = fats[~fats['Número do Alimento'].str.contains('Alimento')]

fats = fats.iloc[:, :5]

fats.drop(fats.columns[1], axis=1, inplace=True)

fats.dropna(inplace=True)

table = table.merge(fats, on="Número do Alimento", how="left")
table = table[table['Tipo do alimento'] != 'Legenda']
table.rename(columns={'Número do Alimento': 'ID Alimento'}, inplace=True)
table.columns = table.columns.str.lower()
table.columns = table.columns.str.replace("- ", "")
table.columns = [unicodedata.normalize('NFKD', col).encode(
    'ASCII', 'ignore').decode('utf-8') for col in table.columns]
table.drop(columns=['fibra numero do alimento'], inplace=True)

table = table[['id alimento', 'tipo do alimento', 'descricao do alimento', 'umidade (%)', 'energia (kcal)', 'energia (kj)', 'proteina (g)', 'lipideos (g)', 'saturados (g)', 'monoinsaturados (g)', 'poliinsaturados (g)', 'colesterol (mg)', 'carboidrato (g)', 'fibra alimentar (g)', 'fibra cinzas (g)', 'fibra calcio (mg)', 'fibra magnesio (mg)', 'fibra manganes (mg)', 'fibra fosforo (mg)',
               'fibra ferro (mg)', 'fibra sodio (mg)', 'fibra potassio (mg)', 'fibra cobre (mg)', 'fibra zinco (mg)', 'fibra retinol (mcg)', 'fibra re (mcg)', 'fibra rae  (mcg)', 'fibra tiamina (mg)', 'fibra riboflavina (mg)', 'fibra piridoxina (mg)', 'fibra niacina (mg)', 'vitamina c (mg)',]]

table.rename(columns={'saturados (g)': 'lipideos saturados (g)', 'monoinsaturados (g)': 'lipideos monoinsaturados (g)',
             'poliinsaturados (g)': ' lipideos poliinsaturados (g)'}, inplace=True)

pd.set_option('future.no_silent_downcasting', True)
table.iloc[:, 3:] = table.iloc[:, 3:].replace('*', 0)
table.iloc[:, 3:] = table.iloc[:, 3:].replace(' Tr', 0)
table.iloc[:, 3:] = table.iloc[:, 3:].replace('Tr', 0)
table.iloc[:, 3:] = table.iloc[:, 3:].replace(' ', 0)
table.iloc[:, 3:] = table.iloc[:, 3:].replace(",", "")

table.iloc[:, 3:] = table.iloc[:, 3:].replace(',0,02', '0.02')

table.iloc[:, 3:] = table.iloc[:, 3:].astype(float)

conn = sqlite3.connect('dados.db')
table.to_sql('tabela', conn, if_exists='replace', index=False)
conn.close()
