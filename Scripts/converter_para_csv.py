import pandas as pd
import os

# Caminho corrigido com raw string
arquivo_excel = r'C:\projeto-automacao-email\python-automacao-email\planilha\notas_alunos.xlsx'

# Lê a planilha existente (não cria mais)
df = pd.read_excel(arquivo_excel)

# Exibe as 5 primeiras linhas no console
print(df.head())

# Converte para CSV com mesmo nome
arquivo_csv = os.path.splitext(arquivo_excel)[0] + '.csv'
df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')

print(f'Arquivo convertido com sucesso para: {arquivo_csv}')
