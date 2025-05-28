## 📘 Documentação - Painel de Sustentabilidade em Python
## 📌 Visão Geral
Este projeto tem como objetivo criar um painel interativo de sustentabilidade utilizando Python, Streamlit e SQLite. Ele permite:

Adicionar projetos que impactam as emissões de GEE (Escopos 1, 2 e 3).

Visualizar os dados em gráficos interativos.

Registrar os impactos por tipo de projeto (Redução, Compensação, etc.).

## 🗂 Estrutura do Projeto

sustentabilidade_projeto/
├── app.py                # App principal com Streamlit
├── database.py           # Operações com o banco de dados
├── data/
│   └── projetos.db       # Banco SQLite com os projetos
├── requirements.txt      # Bibliotecas necessárias
└── README.md             # (opcional) versão simplificada dessa documentação

## 🚀 Instalação e Execução
1. Clone ou baixe o projeto

  git clone https://github.com/seu-usuario/sustentabilidade_projeto.git
  cd sustentabilidade_projeto

2. (Opcional) Crie um ambiente virtual

  python -m venv venv
  venv\Scripts\activate     # Windows
  source venv/bin/activate  # Mac/Linux

3. Instale as dependências

  pip install -r requirements.txt

4. Execute o projeto

  streamlit run app.py

## 📊 Funcionalidades
Visualização de Gráficos
Gráfico de linha com a evolução de emissões por escopo (1, 2 e 3).

Atualizado automaticamente com os projetos adicionados.

Adição de Projetos
Formulário com os campos:

Nome do projeto

Tipo (Redução, Compensação, Outros)

Impacto estimado (tCO₂e) nos escopos 1, 2 e 3

Data de início e fim

Ao submeter, os dados são salvos no banco de dados SQLite (data/projetos.db).

## 🛠 Tecnologias Utilizadas
Tecnologia	Função
Streamlit	Interface Web interativa
Plotly	Gráficos interativos
Pandas	Manipulação de dados
SQLite	Banco de dados leve (local)
Python	Lógica do sistema

## 📁 Banco de Dados
O banco SQLite possui uma tabela chamada projetos com os seguintes campos:

id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT,
tipo TEXT,
escopo1 REAL,
escopo2 REAL,
escopo3 REAL,
data_inicio DATE,
data_fim DATE

## 🔄 Próximos Passos (Evoluções Sugeridas)

 Filtros por tipo, data ou escopo nos gráficos

 Exportação para Excel ou CSV

 Dashboard com KPIs totais

 Simulador de cenários

 Upload de projetos em lote (CSV/Excel)

 Autenticação (login)

 Deploy na web (Streamlit Cloud, Heroku, etc.)

 Capturas de Tela 

## 🤝 Contribuição
Sinta-se à vontade para sugerir melhorias ou abrir issues. É um projeto inicial e qualquer colaboração é bem-vinda!

## 📃 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](./LICENSE) para detalhes.
