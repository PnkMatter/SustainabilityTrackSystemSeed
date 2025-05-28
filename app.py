# app.py
import streamlit as st
import pandas as pd
from database import init_db, insert_project, get_all_projects, insert_real_values, get_monthly_real_emissions, get_monthly_project_reductions 
import plotly.express as px
from datetime import date

# Inicializa banco
init_db()

st.title("Painel de Sustentabilidade 🌱")

# Seção: Gráfico de emissões
st.header("Emissões por Escopo (tCO₂e)")

projects_raw = get_all_projects()
columns = ["ID", "Nome", "Tipo", "Escopo 1", "Escopo 2", "Escopo 3", "Data Início", "Data Fim"]
projects = pd.DataFrame(projects_raw, columns=columns)

if not projects.empty:
    emissions = projects[['Data Início', 'Escopo 1', 'Escopo 2', 'Escopo 3']]
    emissions = emissions.groupby('Data Início').sum().reset_index()
    emissions = pd.melt(emissions, id_vars='Data Início', var_name='Escopo', value_name='tCO2e')

    fig = px.line(emissions, x='Data Início', y='tCO2e', color='Escopo',
                  title="Emissões ao Longo do Tempo por Escopo")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum projeto ainda. Adicione abaixo para começar!")

# Seção: Adição de Projeto
st.write("📦 Projetos no banco:")
st.write(get_all_projects())

st.header("Adicionar Projeto")

with st.form(key="form_projeto"):
    nome = st.text_input("Nome do Projeto")
    tipo = st.selectbox("Tipo", ["Redução", "Compensação", "Outros"])
    escopo1 = st.number_input("Impacto Escopo 1 (tCO2e)", value=0.0)
    escopo2 = st.number_input("Impacto Escopo 2 (tCO2e)", value=0.0)
    escopo3 = st.number_input("Impacto Escopo 3 (tCO2e)", value=0.0)
    data_inicio = st.date_input("Data de Início", value=date.today())
    data_fim = st.date_input("Data de Fim", value=date.today())

    submit = st.form_submit_button("Adicionar Projeto")

    if submit:
        insert_project(nome, tipo, escopo1, escopo2, escopo3, data_inicio, data_fim)
        st.success("Projeto adicionado com sucesso! Atualize a página para ver o gráfico.")

# Seção: Upload de CSV
st.header("📁 Importar projetos de um arquivo CSV")

uploaded_file = st.file_uploader("Escolha um arquivo CSV para importar", type=["csv"])

if uploaded_file is not None:
    try:
        df_csv = pd.read_csv(uploaded_file)

        # Verifica se colunas obrigatórias existem
        required_columns = {"sigla", "fabrica", "pais", "regiao", "ano", "mes", "emissao_total", "energia_gerada_local", "energia_verde_comprada", "escopo1", "escopo2", "escopo3"}
        if not required_columns.issubset(df_csv.columns):
            st.error(f"O CSV precisa conter as colunas: {', '.join(required_columns)}")
        else:
            # Construir campos compatíveis com o banco
            df_temp = df_csv.rename(columns={"ano": "year", "mes": "month"})
            df_temp["day"] = 1

            df_import = df_csv[["sigla", "fabrica", "pais", "regiao", "ano", "mes", "emissao_total", "energia_gerada_local", "energia_verde_comprada", "escopo1", "escopo2", "escopo3"]]
            df_import.columns = ["sigla", "fabrica", "pais", "regiao", "ano", "mes", "emissao_total", "energia_gerada_local", "energia_verde_comprada", "escopo1", "escopo2", "escopo3"]

            st.dataframe(df_import)

            if st.button("Importar dados para o banco"):
                for _, row in df_import.iterrows():
                    insert_real_values(
                        row["sigla"],
                        row["fabrica"],
                        row["pais"],
                        row["regiao"],
                        int(row["ano"]),
                        int(row["mes"]),
                        int(row["emissao_total"]),
                        int(row["energia_gerada_local"]),
                        int(row["energia_verde_comprada"]),
                        float(row["escopo1"]),
                        float(row["escopo2"]),
                        float(row["escopo3"])
                    )
                st.success("Dados importados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao ler ou importar o CSV: {e}")

st.header("📉 Emissões Reais vs Reduções dos Projetos")

df_real = get_monthly_real_emissions()
df_proj = get_monthly_project_reductions()

# Junta os dois dataframes
df = pd.merge(df_real, df_proj, on=["ano", "mes"], how="left", suffixes=("_real", "_reduzido"))
df = df.fillna(0)

# Calcula resultado final
df["escopo1_final"] = df["escopo1_real"] - df["escopo1_reduzido"]
df["escopo2_final"] = df["escopo2_real"] - df["escopo2_reduzido"]
df["escopo3_final"] = df["escopo3_real"] - df["escopo3_reduzido"]

# Formata data
df["data"] = pd.to_datetime(df[["ano", "mes"]].assign(day=1))

# Prepara para gráfico
df_melt = pd.melt(df, id_vars="data", value_vars=[
    "escopo1_real", "escopo1_reduzido", "escopo1_final",
    "escopo2_real", "escopo2_reduzido", "escopo2_final",
    "escopo3_real", "escopo3_reduzido", "escopo3_final"
], var_name="Categoria", value_name="tCO2e")

fig = px.line(df_melt, x="data", y="tCO2e", color="Categoria", title="Comparação de Emissões e Reduções")
st.plotly_chart(fig, use_container_width=True)
