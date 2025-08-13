import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from config.config import *

def registrar_erro(mensagem):
    log_dir = os.path.join( '..', DIRETORIO_LOGS)
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, 'erros.log')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")


def carregar_dados(caminho):
    try:
        df = pd.read_csv(caminho)
        if df.empty:
            msg = "Erro: Arquivo CSV está vazio"
            registrar_erro(msg)
            return None, msg
        return df, "Dados carregados com sucesso"
    except FileNotFoundError:
        msg = f"Erro: Arquivo não encontrado - {caminho}"
        registrar_erro(msg)
        return None, msg
    except Exception as e:
        msg = f"Erro inesperado: {str(e)}"
        registrar_erro(msg)
        return None, msg


def validar_dados(df):
    erros = []

    # Verifica nomes vazios
    if df['Nome'].isnull().any():
        erros.append("Existem alunos sem nome no registro")

    # Verifica nomes duplicados
    if df['Nome'].duplicated().any():
        erros.append("Existem nomes duplicados")

    # Verifica notas negativas
    notas_negativas = df[COLUNAS_NOTA].lt(0).any().any()
    if notas_negativas:
        erros.append("Existem notas negativas")

    if erros:
        msg = (" | ".join(erros))
        registrar_erro(msg)
        raise ValueError(msg)

def calcular_medias(df):
    # Verifica se as colunas necessárias existem
    missing_cols = [col for col in COLUNAS_NOTA if col not in df.columns]

    if missing_cols:
        msg = f"[ERRO] Colunas ausentes: {missing_cols}"
        registrar_erro(msg)
        print(msg)
        return None, msg  # Retorna None para interromper o fluxo

    colunas_nao_numericas = [col for col in COLUNAS_NOTA if not pd.api.types.is_numeric_dtype(df[col])]
    if colunas_nao_numericas:
        msg = f"[ERRO] Colunas não numéricas: {colunas_nao_numericas}"
        registrar_erro(msg)
        print(msg)
        return None, msg


    # Cálculo das médias (código existente)
    df['Média'] = df[COLUNAS_NOTA].mean(axis=1).round(2)
    df['Situação'] = df['Média'].apply(lambda x: 'Aprovado' if x >= MEDIA_APROVACAO else 'Reprovado')
    return df, "Médias calculadas com sucesso"


def gerar_visualizacoes(df, output_dir):
    """Gera gráficos profissionais"""
    try:
        # Gráfico de distribuição
        plt.figure(figsize=(10, 6))
        df['Situação'].value_counts().plot(
            kind='pie',
            autopct='%1.1f%%',
            colors=['#4CAF50', '#F44336'],
            title='Distribuição de Aprovação'
        )
        plt.savefig(os.path.join(output_dir, 'distribuicao.png'), bbox_inches='tight')
        plt.close()

        # Gráfico de desempenho individual
        plt.figure(figsize=(12, 6))
        df.sort_values('Média').plot(
            x='Nome',
            y='Média',
            kind='barh',
            color=df['Situação'].map({'Aprovado': '#4CAF50', 'Reprovado': '#F44336'}),
            title='Desempenho Individual'
        )
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(output_dir, 'desempenho.png'), bbox_inches='tight')
        plt.close()

    except Exception as e:
        registrar_erro(f"Erro na geração de gráficos: {str(e)}")


def exportar_resultados(df, output_path):
    try:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return f"Resultados exportados para {output_path}"
    except Exception as e:
        msg = f"Erro ao exportar resultados: {str(e)}"
        registrar_erro(msg)
        return msg


'''def gerar_feedback_ia(nome: str, notas: dict, media: float) -> str:
    cache = carregar_cache()
    cache_key = f"{nome}_{hash(frozenset(notas.items()))}"

    if cache_key in cache:
        return cache[cache_key]

    prompt = f"""
    Como especialista em educação, forneça um feedback para {nome}:
    - Matérias: {', '.join(f'{k}: {v:.1f}' for k, v in notas.items())}
    - Média: {media:.1f}
    Diretrizes:
    1. Identifique 1 ponto forte
    2. Sugira 1 área de melhoria
    3. Máximo 2 frases
    """

    try:
        # Mensagens com tipos específicos
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content="Você é um tutor educacional especializado."
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,  # Agora com tipos corretos
            max_tokens=15
        )

        feedback = response.choices[0].message.content
        cache[cache_key] = feedback
        salvar_cache(cache)
        return feedback

    except Exception as e:
        registrar_erro(f"Erro na API: {str(e)}")
        return f"[Feedback temporariamente indisponível - {datetime.now().strftime('%H:%M')}]"
'''

def mostrar_analise(df):
    print("\n" + "=" * 50)
    print("📊 ANÁLISE COMPLETA")
    print("=" * 50)

    print("\n🔍 Visão Geral:")
    print(df.to_string())

    print("\n📝 Estatísticas Descritivas:")
    print(df.describe())

    print(f"\n📌 Alunos em Recuperação (Média entre {RECUPERACAO_MIN} e {RECUPERACAO_MAX}):")
    recuperacao = df[df['Média'].between(RECUPERACAO_MIN, RECUPERACAO_MAX)].sort_values('Média')

    if not recuperacao.empty:
        for idx, row in recuperacao.iterrows():
            print(
                f"- {row['Nome']}: {row['Média']:.1f} ({'➤ Precisa melhorar ' + ', '.join(col for col in COLUNAS_NOTA if row[col] < MEDIA_APROVACAO)})")
    else:
        print("Nenhum aluno em recuperação")

    print("\n🎯 Top 3 Melhores Alunos:")
    print(df.nlargest(3, 'Média')[['Nome', 'Média']])

def main():
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        input_path = os.path.join(script_dir, '..', 'datasets', 'notas_alunos.csv')
        output_dir = os.path.join(script_dir, '..', DIRETORIO_SAIDA)
        os.makedirs(output_dir, exist_ok=True)

        df, msg = carregar_dados(input_path)
        if df is None:
            print(msg)
            return
        try:
            validar_dados(df)
        except ValueError as e:
            registrar_erro(f"Dados inválidos: {e}")
            print(f"Erro: {e}")
            return

        df, msg = calcular_medias(df)
        if df is None:  # <- Nova verificação
            return

        mostrar_analise(df)
        print("\nCriando gráficos para melhor vizualização 📊\n")
        gerar_visualizacoes(df, output_dir)
        print(f"Gráficos gerados, eles podem ser acessados em: {output_dir} como 'desempenho.png' e 'distribuicao.png'")

        output_path = os.path.join(output_dir, 'analise_completa.csv')
        print("\n" + exportar_resultados(df, output_path))
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        registrar_erro(f"Falha crítica: {str(e)}")

if __name__ == '__main__':
    main()