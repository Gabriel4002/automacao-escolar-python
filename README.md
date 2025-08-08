# 📨 Automação Escolar com Python

Automação simples e funcional para envio de boletins escolares via e-mail, com geração, conversão e análise de planilhas usando Python.

## 🔧 Funcionalidades
- Geração de planilha com dados fictícios de alunos (`.xlsx`)
- Leitura de planilhas existentes
- Conversão automática para `.csv` e organização na pasta `dataset`
- Envio de e-mails com os boletins individuais
- Registro de logs de envio

## 📊 Análise de Dados  
- Gera estatísticas descritivas (média, desvio padrão).  
- Classifica alunos em **Aprovados/Reprovados**.  
- Exporta resultados para `notas_analise.csv`.  
- **Técnicas usadas**: Pandas, lambda functions, filtros.  

## 📁 Estrutura do Projeto
```
automacao-escolar-python/
├── planilha/   
├── analise_dados/
│ └── dataset/             # Arquivo com os dados dos alunos
│ └── scripts/             # Arquivo com os códigos de analise de dados
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

4️. Configurar as variáveis de ambiente
- Copie o arquivo `.env.example` para `.env` (caso exista) ou crie um novo `.env`.
- Preencha com seu e‑mail e senha de aplicativo (ou outra conta SMTP válida):

```env
EMAIL=seuemail@gmail.com
SENHA=sua_senha_de_app
```
> ⚠️ Importante: use senha de aplicativo no Gmail ou configuração equivalente em outros provedores.

5. Execute os scripts:
```bash
# Gerar planilha
python Scripts/gerar_planilha.py

# Enviar e-mails
python Scripts/codigo_email.py

# Converter para CSV
python Scripts/converter_para_csv.py

# Analisar os dados do CSV
python analise_dados_pandas/scripts/analise_dados.py
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
- Caso use Gmail, ative a autenticação em dois fatores e gere uma senha de app.

## ✍️ Autor

Gabriel Lobato  
[LinkedIn](https://www.linkedin.com/in/gabriel-lobato-314096371)

---

> Projeto criado como parte do meu aprendizado em automação com Python, envio de e-mails e análise de dados.
