import pandas as pd

from codigo_envio_email import enviar_email
from datetime import datetime
from config.config import MEDIA_APROVACAO
import os


os.makedirs("../logs", exist_ok=True)

# Caminho da planilha já existente
script_dir = os.path.dirname(os.path.realpath(__file__))
caminho_arquivo = os.path.join(script_dir, '..', 'planilha', 'notas_alunos.xlsx')
#Função que le o arquivo excel
df = pd.read_excel(caminho_arquivo)

#Loop que exibe o corpo da mensagem que sera enviada para o aluno
def main():
    for _, row in df.iterrows():
        aluno = row["Nome"]
        email_destino = row.get("Email")
        if not email_destino:
            print(f"Email não encontrado para {aluno}. Pulando...")
            continue

        notas = row.drop(["Nome", "Email", "Média"])
        corpo = f"Olá {aluno},\n\nAqui estão suas notas:\n"
        total = 0
        num_materias = 0
        materias_abaixo = []

        for materia, nota in notas.items():
            try:
                nota = float(nota)
                corpo += f"{materia}: {nota}\n"
                total += nota
                num_materias += 1

                if nota < MEDIA_APROVACAO:
                    materias_abaixo.append(materia)
            except ValueError:
                corpo += f"{materia}: [Nota inválida]\n"
                print(f"Atenção: Nota inválida para a matéria {materia} de {aluno}")
                continue

        if num_materias == 0:
            print(f"Nenhuma nota válida encontrada para {aluno}. Pulando...")
            continue

        media = total / num_materias
        corpo += f"\nMédia: {media:.2f}\n"

        # Mensagem personalizada baseada na média
        if media >= 7:
            corpo += "Suas notas estão ótimas! Continue assim.\n"
        elif 5 <= media < 7:
            corpo += "Suas notas estão acima da média mínima. Fique atento!\n"
        else:
            corpo += "Você está abaixo da média mínima. Precisa melhorar!\n"

        # Adiciona matérias abaixo da média
        if materias_abaixo:
            corpo += "\nMatérias que precisam de atenção:\n"
            for mat in materias_abaixo:
                corpo += f"➤ {mat}\n"

        corpo += "\nAtenciosamente,\nSecretaria Escolar"

        try:
            enviar_email(email_destino, "Boletim Escolar", corpo)
            print(f"E-mail enviado para {aluno}")

            with open("../logs/envios_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - ENVIADO\n")
        except Exception as e:
            print(f"Erro ao enviar para {aluno}: {e}")
            with open("../logs/envios_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - FALHA: {e}\n")

if __name__ == '__main__':
    main()