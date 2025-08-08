from openpyxl import Workbook
from codigo_envio_email import enviar_email
from datetime import datetime
import os

#Checa se o diretório existe
os.makedirs("../logs", exist_ok=True)
os.makedirs("../planilha", exist_ok=True)

#Dados que serão adicionados na planilha
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

#Funções referentes ao openpyxl. WB cria uma pasta de trabalho; WS infoma que será usada a planilha ativa desta pasta de trabalho e WS.title insere o titulo desta planilha
wb = Workbook()
ws = wb.active
ws.title = "Notas dos Alunos"

#Define que 'headings' sera as informações que existem após estas referencias
headings = ["Nome"] + list(data["Gabriel"]["Notas"].keys())
ws.append(headings)

#Cria um loop que primeiramente imprime na planilha as informações do aluno
for aluno, dados in data.items():
    notas = dados["Notas"]
    linha_planilha = [aluno] + list(notas.values())
    ws.append(linha_planilha)
#Cria o corpo da mensagem que será enviada por email para o aluno e calcula a média dele
    corpo = f"Olá {aluno},\n\nAqui estão suas notas:\n"
    total = 0
    for materia, nota in notas.items():
        corpo += f"{materia}: {nota}\n"
        total += nota
    media = total / len(notas)
    corpo += f"\nMédia: {media:.2f}\n\nAtenciosamente,\nSecretaria Escolar"

    email_destino = dados["Email"]
#Envia o email para o aluno e cria um log que exibe quando a mensagem foi enviada e se ela foi realmente enviada ou não
    try:
        enviar_email(email_destino, "Boletim Escolar", corpo)
        print(f"E-mail enviado para {aluno}")

        with open("../logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - ENVIADO\n")

    except Exception as e:
        print(f"Erro ao enviar para {aluno}: {e}")
        with open("logs/envios_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {aluno} - {email_destino} - FALHA: {e}\n")
#Salva a planilha na pasta de destino com o seguinte nome
wb.save("../planilha/notas_alunos.xlsx")
