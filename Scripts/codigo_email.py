import pandas as pd
from codigo_envio_email import enviar_email
from datetime import datetime
import os

os.makedirs("../logs", exist_ok=True)

# Caminho da planilha já existente
arquivo_excel = r'C:\projeto-automacao-email\python-automacao-email\planilha\notas_alunos.xlsx'
df = pd.read_excel(arquivo_excel)

# Simulando base de e-mails por nome
emails = {
    "Gabriel": "gabriellobato315@gmail.com",
    "Ana": "ana@email.com",
    "Jorge Willem": "jorgewillem@email.com"
}

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
