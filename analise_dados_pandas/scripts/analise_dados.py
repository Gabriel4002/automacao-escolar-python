import pandas as pd
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from config.config import *

#Função que registra erros em um log
def registrar_erro(mensagem):
    log_dir = os.path.join( '..', DIRETORIO_LOGS)
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, 'erros.log')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")

#Carrega os dados do arquivo csv gerado após converter a planilha em csv
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

#Função que valida os dados presentes no arquivo csv, se há algum campo vazio, etc.
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

#Função que cacula as medias dos alunos além de analisar se há algum erro como se há alguma string onde deveria haver numeros, se todas as colunas estão presentes, etc.
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

#Função que gera os graficos sobre a quantidade de alunos aprovados e um que exibe a média dos alunos
def gerar_visualizacoes(df, output_dir):
    """Gera gráficos"""
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

#Função que determina onde os resultados serão exportados ao fim do código, onde o arquivo csv com as analises serão salvos
def exportar_resultados(df, output_path):
    try:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return f"Resultados exportados para {output_path}"
    except Exception as e:
        msg = f"Erro ao exportar resultados: {str(e)}"
        registrar_erro(msg)
        return msg

#Função que gera um pdf com o relatório dos alunos, médias, situação, nomes
def gerar_relatorio_pdf(df, output_path, graficos_paths=[]):
    """Gera um relatório PDF com base nos dados"""
    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        largura, altura = A4

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, altura - 50, "Relatório de Desempenho dos Alunos")
        c.setFont("Helvetica", 12)
        c.drawString(50, altura - 70, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, altura - 82, f"Você pode ver os gráficos na segunda página")
        c.setFont("Helvetica", 12)


        # Estatísticas
        total_alunos = len(df)
        aprovados = df['Situação'].value_counts().get('Aprovado', 0)
        reprovados = df['Situação'].value_counts().get('Reprovado', 0)

        c.drawString(50, altura - 100, f"Total de alunos: {total_alunos}")
        c.drawString(50, altura - 120, f"Aprovados: {aprovados}")
        c.drawString(50, altura - 140, f"Reprovados: {reprovados}")


        # Tabela simples
        y = altura - 180
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Nome")
        c.drawString(250, y, "Média")
        c.drawString(350, y, "Situação")
        c.setFont("Helvetica", 10)

        y -= 20
        for _, row in df.iterrows():
            c.drawString(50, y, str(row['Nome']))
            c.drawString(250, y, f"{row['Média']:.2f}")
            c.drawString(350, y, row['Situação'])
            y -= 15
            if y < 50:  # quebra de página
                c.showPage()
                y = altura - 50


        if graficos_paths:
            c.showPage()  # inicia nova página para os gráficos
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 50, "Gráficos de Análise")

            y_position = altura - 100

            for grafico in graficos_paths:
                if os.path.exists(grafico):
                    img_width, img_height = ImageReader(grafico).getSize()

                    # Ajusta a largura para no máximo 500px e altura proporcional
                    max_width = 500
                    max_height = 350
                    scale = min(max_width / img_width, max_height / img_height)

                    new_width = img_width * scale
                    new_height = img_height * scale

                    # Desenha imagem centralizada
                    x_position = (largura - new_width) / 2
                    c.drawImage(grafico, x_position, y_position - new_height, width=new_width, height=new_height)

                    y_position -= new_height + 30  # espaçamento

                    # Se não couber mais na página, cria nova
                    if y_position < 100:
                        c.showPage()
                        y_position = altura - 100

        # Salva o PDF
        c.save()
        print(f"✅ Relatório PDF gerado em: {output_path}")

    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")


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

        resposta = input("Você deseja gerar um PDF com o relatório dos alunos? (Sim/Não): ").strip().lower()
        if resposta == 'sim' or resposta == 'Sim' or resposta == 's' or resposta == 'S':
            caminho_pdf = os.path.join(output_dir, 'relatorio_alunos.pdf')
            graficos = [
                os.path.join(output_dir, 'distribuicao.png'),
                os.path.join(output_dir, 'desempenho.png')
            ]
            gerar_relatorio_pdf(df, caminho_pdf, graficos_paths=graficos)

    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        registrar_erro(f"Falha crítica: {str(e)}")

if __name__ == '__main__':
    main()