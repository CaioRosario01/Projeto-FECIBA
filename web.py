# Importa as bibliotecas necessárias
import streamlit as st          # Interface web
import pandas as pd            # Manipulação de dados
from mapa import criar_mapa
from streamlit_folium import st_folium

# -----------------------------
# Leitura e preparação dos dados
# -----------------------------

# Lê o arquivo CSV com os dados das praias
df = pd.read_csv("dados/dados_praias.csv")

df = df.replace('propria', 'Própria')
df = df.replace('impropria', 'Imprópria')

# Converte a coluna "data" para o tipo datetime (facilita análises temporais)
df["data"] = pd.to_datetime(df["data"])


# -----------------------------
# Configuração da página
# -----------------------------

# Define título da aba e layout (wide = tela mais larga)
st.set_page_config(page_title="Balneabilidade Ilhéus", layout="wide")

# Título principal do sistema
st.title("PraiaCheck: Sistema de Balneabilidade - Ilhéus")

# Pequena descrição
st.markdown("Divulgação da qualidade da água nas praias de Ilhéus")
st.info("ℹ️ Veja mais informações sobre o Projeto PraiaCheck na barra lateral")


# -----------------------------
# Filtro por praia
# -----------------------------

# Cria um seletor com os nomes das praias (ordenados)
praia = st.selectbox(
    "Escolha a praia:",
    sorted(df["Praia"].unique())
)

# Filtra o dataframe apenas para a praia selecionada
df_filtrado = df[df["Praia"] == praia]


# -----------------------------
# Cálculo do índice de risco
# -----------------------------

# Cria uma coluna "score":
# 1 = imprópria
# 0 = própria
df["score"] = df["Classificação"].apply(lambda x: 1 if x == "Imprópria" else 0)

# Agrupa por praia e calcula a média do score
# Isso representa a frequência de vezes que a praia esteve imprópria
risco = df.groupby("Praia")["score"].mean().sort_values()


# -----------------------------
# Estilização da tabela
# -----------------------------

# Função para colorir a classificação
def cor_classificacao(val):
    if val == "Imprópria":
        return "color: red"    # Vermelho para imprópria
    else:
        return "color: green"  # Verde para própria

# Exibe a tabela filtrada com cores na coluna "Classificação"
st.dataframe(
    df_filtrado.style.map(cor_classificacao, subset=["Classificação"]),
    column_config={
        "data": st.column_config.DateColumn(
            "Data da Coleta",
            format="DD/MM/YYYY",  # Formato brasileiro
        ),
    },
    use_container_width=True
)

# -----------------------------
# Métricas (resumo dos dados)
# -----------------------------

# Total de registros da praia selecionada
total = len(df_filtrado)

# Quantidade de análises próprias
proprias = (df_filtrado["Classificação"] == "Própria").sum()

# Quantidade de análises impróprias
improprias = (df_filtrado["Classificação"] == "Imprópria").sum()

# Cria 3 colunas para exibir os indicadores
col1, col2, col3 = st.columns(3)

# Exibe os indicadores
col1.metric("Total de análises", total)
col2.metric("Próprias", proprias)
col3.metric("Impróprias", improprias)


# -----------------------------
# Indicador de qualidade da praia
# -----------------------------

st.divider()

st.subheader("Situação atual da praia")

col1, col2 = st.columns([2, 1])

with col1:
    ultima_classificacao = df_filtrado.sort_values("data").iloc[-1]["Classificação"]
    ultima_data = df_filtrado["data"].max()

    if ultima_classificacao == "Imprópria":
        st.error("⚠️ Água imprópria para banho")
    else:
        st.success("✅ Água própria para banho")

    st.caption(f"Última análise: {ultima_data.date()}")

with col2:
    st.metric(
        "Total de análises",
        len(df_filtrado)
    )

coordenadas = {
    "Avenida": [-14.801595691198887, -39.02990331527904],
    "Barra de São Miguel": [-14.762791385731225, -39.05797959772375],
    "Cururupe": [-14.842979615212979, -39.02524773896752],
    "Malhado": [-14.784720528977816, -39.03777837660922],
    "Sul": [-14.820624696328307, -39.02495731039769],
    "Cristo": [-14.803696351173011, -39.03333352575771],
    "Opaba": [-14.817495059038803, -39.02451011494049],
    "Marciano": [-14.779071139334897, -39.04774124329706],
    "Ceplus Montante": [-14.838957830650179, -39.02485467661454],
    "Ceplus Jusante": [-14.840597153780113, -39.02471812572864],
    "Milionários": [-14.864563935948906, -39.024144443154846],
    "Olivença": [-14.93016272245089, -39.01641369689538],

}

if not df_filtrado.empty:
    ultima_classificacao = df_filtrado.sort_values("data").iloc[-1]["Classificação"]
    # ... resto do código
else:
    st.warning("Não há dados disponíveis para esta praia.")

st.subheader("Mapa das praias: ")

mapa = criar_mapa(df, coordenadas)

#Centralizando o mapa
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st_folium(mapa, width=800, height=500)

st.sidebar.title("Sobre")

st.sidebar.markdown("""
**Projeto:** Deu Praia  

Sistema de divulgação da qualidade da água nas praias de Ilhéus.
Este sistema foi desenvolvido por estudantes da 3ªB do Colégio da Polícia Militar Rômulo Galvão, 
com o objetivo de apresentar dados sobre a qualidade da água das praias de Ilhéus.

O projeto utiliza dados públicos de balneabilidade, organizados e analisados por meio de Python, 
com o intuito de facilitar o acesso à informação pela população ilheense.
                    


**Equipe:**
- Adriel de Jesus
- Caio Rosário
- Thiago Adão
- Lara Cryssa
""")