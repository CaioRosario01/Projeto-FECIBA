# =================================================================
# BIBLIOTECAS E IMPORTAÇÕES
# =================================================================
import streamlit as st          # Framework para interface web
import pandas as pd             # Manipulação e análise de dados
from mapa import criar_mapa      # Função customizada para o mapa
from streamlit_folium import st_folium  # Integração Folium/Streamlit

# =================================================================
# CONFIGURAÇÃO DA PÁGINA
# =================================================================
st.set_page_config(page_title="Balneabilidade Ilhéus", layout="wide")

# =================================================================
# LEITURA E TRATAMENTO DOS DADOS
# =================================================================
# Carrega a base de dados
df = pd.read_csv("dados/dados_praias.csv")

# Padronização de nomes (Case sensitive)
df = df.replace('propria', 'Própria')
df = df.replace('impropria', 'Imprópria')

# Conversão de tipos: string para data
df["data"] = pd.to_datetime(df["data"])

# Cálculo do índice de risco global (Score: 1 para Imprópria, 0 para Própria)
df["score"] = df["Classificação"].apply(lambda x: 1 if x == "Imprópria" else 0)
risco = df.groupby("Praia")["score"].mean().sort_values()

# =================================================================
# CABEÇALHO DA INTERFACE
# =================================================================
st.title("PraiaCheck: Sistema de Balneabilidade - Ilhéus")
st.markdown("Divulgação da qualidade da água nas praias de Ilhéus")
st.info("ℹ️ Veja mais informações sobre o Projeto PraiaCheck na barra lateral")

# =================================================================
# FILTROS E LÓGICA DE SELEÇÃO
# =================================================================
# Seletor de praias disponível na base
praia = st.selectbox(
    "Escolha a praia:",
    sorted(df["Praia"].unique())
)

# Filtra dados específicos da praia escolhida e ordena pela data mais recente
df_filtrado = df[df["Praia"] == praia]
df_filtrado = df_filtrado.sort_values("data", ascending=False)

# =================================================================
# EXIBIÇÃO DA TABELA (COM LÓGICA DE EXPANSÃO)
# =================================================================
# Estilização condicional (Cores: Verde para Própria, Vermelho para Imprópria)
def cor_classificacao(val):
    if val == "Imprópria":
        return "color: red"
    else:
        return "color: green"

# Controle de estado para o botão "Ver Mais"
if 'ver_tudo' not in st.session_state:
    st.session_state.ver_tudo = False

# Define se exibe apenas as 4 últimas ou o histórico completo
if st.session_state.ver_tudo:
    df_exibicao = df_filtrado
    texto_botao = "Ver menos"
else:
    df_exibicao = df_filtrado.head(4)
    texto_botao = "Ver mais"

# Renderização do DataFrame
st.dataframe(
    df_exibicao.style.map(cor_classificacao, subset=["Classificação"]),
    column_config={
        "data": st.column_config.DateColumn(
            "Data da Coleta",
            format="DD/MM/YYYY",
            width="150px"
        ),
        "score": None  # Esconde a coluna de score
    },
    use_container_width=True,
    hide_index=True  # Remove a coluna de índices numéricos
)

# Botão de alternância (Toggle)
if st.button(texto_botao):
    st.session_state.ver_tudo = not st.session_state.ver_tudo
    st.rerun()

# =================================================================
# MÉTRICAS GERAIS DA PRAIA SELECIONADA
# =================================================================
total = len(df_filtrado)
proprias = (df_filtrado["Classificação"] == "Própria").sum()
improprias = (df_filtrado["Classificação"] == "Imprópria").sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total de análises", total)
col2.metric("Próprias", proprias)
col3.metric("Impróprias", improprias)

# =================================================================
# STATUS ATUAL E ALERTAS
# =================================================================
st.divider()
st.subheader("Situação atual da praia")

col_status, col_metric_total = st.columns([2, 1])

if not df_filtrado.empty:
    with col_status:
        # Pega a análise mais recente cronologicamente
        ultima_classificacao = df_filtrado.sort_values("data").iloc[-1]["Classificação"]
        ultima_data = df_filtrado["data"].max()

        if ultima_classificacao == "Imprópria":
            st.error("⚠️ Água imprópria para banho")
        else:
            st.success("✅ Água própria para banho")
        
        st.caption(f"Última análise: {ultima_data.date()}")

    with col_metric_total:
        st.metric("Total de análises", len(df_filtrado))
else:
    st.warning("Não há dados disponíveis para esta praia.")

# =================================================================
# MAPA GEOGRÁFICO
# =================================================================
st.subheader("Mapa das praias: ")

# Dicionário de Coordenadas (Latitude, Longitude)
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

# Centralização e exibição do mapa via Folium
mapa = criar_mapa(df, coordenadas)
c1, c2, c3 = st.columns([1, 3, 1])
with c2:
    st_folium(mapa, width=800, height=500)


# =================================================================
# BARRA LATERAL (SIDEBAR) - SOBRE O PROJETO
# =================================================================
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


#Fonte dos dados
st.sidebar.markdown("**Fonte dos dados:** INEMA - Boletins de Balneabilidade")