# 📨 Automação Escolar com Python

Automação simples e funcional para envio de boletins escolares via e-mail, com geração, conversão e análise de planilhas usando Python.

## 🔧 Funcionalidades
- Geração de planilha com dados fictícios de alunos (`.xlsx`)
- Leitura de planilhas existentes
- Conversão automática para `.csv`
- Envio de e-mails com os boletins individuais
- Registro de logs de envio
- (Em breve) Análise de dados com Pandas

## 📁 Estrutura do Projeto
```
automacao-escolar-python/
├── planilha/              # Arquivo com os dados dos alunos
├── logs/                  # Logs de envio
├── Scripts/               # Scripts principais
├── README.md              # Este arquivo
├── requirements.txt       # Bibliotecas necessárias
└── .gitignore             # Ignorar arquivos temporários
```

## ▶️ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/Gabriel4002/automacao-escolar-python.git
cd automacao-escolar-python
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4.Edite o arquivo `.env.example` colocando o seu email e a sua senha de acesso e renomeie o arquivo para `.env`

5. Execute os scripts:
```bash
# Gerar planilha
python Scripts/gerar_planilha.py

# Enviar e-mails
python Scripts/codigo_email.py

# Converter para CSV
python Scripts/converter_para_csv.py
```

## 💼 Tecnologias utilizadas

- Python 3.13+
- `pandas`
- `openpyxl`
- `smtplib` e `email`
- `os`, `datetime`

## 📌 Requisitos

- Conta de e-mail (Gmail, Outlook, etc.)
- Planilha `.xlsx` formatada corretamente

## ✍️ Autor

Gabriel Lobato  
[LinkedIn](https://www.linkedin.com/in/gabriel-lobato-314096371)

---

> Projeto criado como parte do meu aprendizado em automação com Python, envio de e-mails e análise de dados.
