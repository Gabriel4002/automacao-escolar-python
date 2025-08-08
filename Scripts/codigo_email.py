#Este código possui a mesma base do código presente no arquivo "gerar_planilha.py", porem ao inves de cria uma planilha, ele le a planilha ja existente

import pandas as pd
from codigo_envio_email import enviar_email
from datetime import datetime
import os

os.makedirs("../logs", exist_ok=True)

# Caminho da planilha já existente
script_dir = os.path.dirname(os.path.realpath(__file__))
caminho_arquivo = os.path.join(script_dir, '..', 'planilha', 'notas_alunos.xlsx')
#Função que le o arquivo excel
df = pd.read_excel(caminho_arquivo)

# Simulando base de e-mails por nome
emails = {
    #Troque pelo email que você deseja receber a mensagem sobre o boletim
    "Gabriel": "gabriel@email.com",
    "Ana": "ana@email.com",
    "Jorge Willem": "jorgewillem@email.com"
}
#Loop que exibe o corpo da mensagem que sera enviada para o aluno
for _, row in df.iterrows():
    aluno = row["Nome"]
    notas = row.drop("Nome")
    corpo = f"Olá {aluno},\n\nAqui estão suas notas:\n"

    total = 0
    for materia, nota in notas.items():
        corpo += f"{materia}: {nota}\n"
        total += nota
    media = total / len(notas)
    corpo += f"\nMédia: {media:.2f}\n\nAtenciosamente,\nSecretaria Escolar"

    email_destino = emails.get(aluno, None)
    if not email_destino:
        print(f"Email não encontrado para {aluno}. Pulando...")
        continue

    try:
        enviar_email(email_destino, "Boletim Escolar", corpo)
        print(f"E-mail enviado para {aluno}")

        with open("../logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - ENVIADO\n")

    except Exception as e:
        print(f"Erro ao enviar para {aluno}: {e}")
        with open("../logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - FALHA: {e}\n")
