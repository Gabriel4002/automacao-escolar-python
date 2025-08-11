import pandas as pd
import os
import shutil

# Caminho corrigido com raw string
script_dir = os.path.dirname(os.path.realpath(__file__))
caminho_arquivo = os.path.join(script_dir, '..', 'planilha', 'notas_alunos.xlsx')

if not os.path.exists(caminho_arquivo):
    print(f"Arquivo Excel não encontrado: {caminho_arquivo}")
    exit()

# Lê a planilha existente (não cria mais)
df = pd.read_excel(caminho_arquivo)

# Exibe as 5 primeiras linhas no console
print(df.head())
print("\n ...")

# Converte para CSV com mesmo nome
arquivo_csv = os.path.splitext(caminho_arquivo)[0] + '.csv'
df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')

print(f'Arquivo convertido com sucesso para: {arquivo_csv}')

# Caminho da pasta destino (dataset)
pasta_destino = '../analise_dados_pandas/datasets'

# Cria a pasta se não existir
os.makedirs(pasta_destino, exist_ok=True)

# Caminho final do CSV
destino_csv = os.path.join(pasta_destino, os.path.basename(arquivo_csv))

# Move o arquivo para a pasta dataset
shutil.move(arquivo_csv, destino_csv)

print(f'Arquivo movido para: {destino_csv}')
