from openpyxl import Workbook
from datetime import datetime
import os

# Checa se os diretórios existem
os.makedirs("../logs", exist_ok=True)
os.makedirs("../planilha", exist_ok=True)

# Dados dos alunos
data = {
    "Gabriel": {
        "Email": "gabriel@email.com",
        "Notas": {
            "Matematica": 5,
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
            "Matematica": 1,
            "Portugues": 4,
            "Historia": 2,
            "Geografia": 8
        }
    },
    "Mariana Souza": {
        "Email": "mariana.souza@email.com",
        "Notas": {
            "Matematica": 7,
            "Portugues": 9,
            "Historia": 6,
            "Geografia": 8
        }
    },
    "Lucas Ferreira": {
        "Email": "lucas.ferreira@email.com",
        "Notas": {
            "Matematica": 3,
            "Portugues": 5,
            "Historia": 4,
            "Geografia": 2
        }
    },
    "Beatriz Lima": {
        "Email": "beatriz.lima@email.com",
        "Notas": {
            "Matematica": 9,
            "Portugues": 7,
            "Historia": 8,
            "Geografia": 9
        }
    },
    "Ricardo Alves": {
        "Email": "ricardo.alves@email.com",
        "Notas": {
            "Matematica": 6,
            "Portugues": 6,
            "Historia": 5,
            "Geografia": 6
        }
    },
    "Larissa Martins": {
        "Email": "larissa.martins@email.com",
        "Notas": {
            "Matematica": 2,
            "Portugues": 3,
            "Historia": 1,
            "Geografia": 4
        }
    },
    "Fernando Costa": {
        "Email": "fernando.costa@email.com",
        "Notas": {
            "Matematica": 10,
            "Portugues": 9,
            "Historia": 9,
            "Geografia": 10
        }
    },
    "Juliana Rocha": {
        "Email": "juliana.rocha@email.com",
        "Notas": {
            "Matematica": 4,
            "Portugues": 6,
            "Historia": 5,
            "Geografia": 7
        }
    }
}

# Criação da planilha
wb = Workbook()
ws = wb.active
ws.title = "Notas dos Alunos"

# Cabeçalhos (colunas)
headings = ["Nome"] + list(data["Gabriel"]["Notas"].keys()) + ["Média"]
ws.append(headings)

# Processa e adiciona os dados de cada aluno na planilha
for aluno, dados in data.items():
    notas = dados["Notas"]
    valores_notas = list(notas.values())
    media = sum(valores_notas) / len(valores_notas)

    linha_planilha = [aluno] + valores_notas + [round(media, 2)]
    ws.append(linha_planilha)

    # Apenas printa no terminal que foi processado
    print(f"Notas do aluno {aluno} processadas.")

# Salva a planilha
wb.save("planilha/notas_alunos.xlsx")
print("\nPlanilha salva com sucesso em '../planilha/notas_alunos.xlsx'")
