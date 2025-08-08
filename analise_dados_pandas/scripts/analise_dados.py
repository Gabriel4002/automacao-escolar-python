import pandas as pd
import os

os.makedirs("../datasets", exist_ok=True)
def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    caminho_arquivo = os.path.join(script_dir, '..', 'datasets', 'notas_alunos.csv')
    #Checa se o arquivo "notas_alunos.csv" existe
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return

    #Exibe as 5 primeiras linhas da planilha
    print("=== 5 primeiras linhas ===")
    print(df.head(), "\n")

    #Exibe as informações gerais da planilha
    print("=== Informações gerais ===")
    print(df.info(), "\n")

    #Exibe as estatiscas da planilha
    print("=== Estatísticas descritivas ===")
    print(df.describe(), "\n")

    #Calcula a média de cada aluno
    df['Média'] = df[['Matematica', 'Portugues', 'Historia', 'Geografia']].mean(axis=1)
    print("=== Alunos e suas médias ===")
    print(df[['Nome', 'Média']], "\n")

    #Exibe os alunos com média abaixo de 5
    print("=== Alunos com média abaixo de 5 ===")
    print(df[df['Média'] < 5])

    #Exibe a situação do aluno de acordo com a média dele
    df['Situação'] = df['Média'].apply(lambda x: 'Aprovado' if x >= 5 else 'Reprovado')

    #Faz uma contagem de quantos alunos estão aprovados ou reprovados
    print("=== Contagem por situação ===")
    print(df['Situação'].value_counts(), "\n")

    #Cria um arquivo csv que contem esses dados
    df.to_csv('../datasets/notas_analise.csv', index=False, encoding='utf-8-sig')
    print("Análise salva em 'notas_analise.csv'.")




if __name__ == '__main__':
    main()
