from openpyxl import Workbook
from codigo_envio_email import enviar_email
from datetime import datetime
import os


os.makedirs("../logs", exist_ok=True)

data = {
    "Gabriel": {
        #adicione o email que irá receber a mensagem sobre as notas
        "Email": "gabriel@email.com",
        "Notas": {
            "Matematica": 10,
            "Portugues": 8,
            "Historia": 6,
            "Geografia": 1
        }
    },
    "Ana": {
        "Email": "ana@email.com",
        "Notas": {
            "Matematica": 4,
            "Portugues": 3,
            "Historia": 7,
            "Geografia": 3
        }
    },
    "Jorge Willem": {
        "Email": "jorgewillem@email.com",
        "Notas": {
            "Matematica": 9,
            "Portugues": 4,
            "Historia": 2,
            "Geografia": 10
        }
    }
}

wb = Workbook()
ws = wb.active
ws.title = "Notas dos Alunos"

headings = ["Nome"] + list(data["Gabriel"]["Notas"].keys())
ws.append(headings)

for aluno, dados in data.items():
    notas = dados["Notas"]
    linha_planilha = [aluno] + list(notas.values())
    ws.append(linha_planilha)

    corpo = f"Olá {aluno},\n\nAqui estão suas notas:\n"
    total = 0
    for materia, nota in notas.items():
        corpo += f"{materia}: {nota}\n"
        total += nota
    media = total / len(notas)
    corpo += f"\nMédia: {media:.2f}\n\nAtenciosamente,\nSecretaria Escolar"

    email_destino = dados["Email"]

    try:
        enviar_email(email_destino, "Boletim Escolar", corpo)
        print(f"E-mail enviado para {aluno}")

        with open("logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - ENVIADO\n")

    except Exception as e:
        print(f"Erro ao enviar para {aluno}: {e}")
        with open("logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - FALHA: {e}\n")

wb.save("planilha/notas_alunos.xlsx")
