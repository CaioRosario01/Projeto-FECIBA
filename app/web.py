import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


#Puxando os dados
df = pd.read_csv("dados/dados_praias.csv")
df["data"] = pd.to_datetime(df["data"])

st.title("Sistema de Balneabilidade - Ilhéus")


praia = st.selectbox("Escolha a praia", df["praia"].unique())

df_filtrado = df[df["praia"] == praia]

st.dataframe(df_filtrado)

df["score"] = df["classificacao"].apply(lambda x: 1 if x == "impropria" else 0)
risco = df.groupby("praia")["score"].mean().sort_values()

with st.expander("Ver índice de risco por praia"):
    st.bar_chart(risco)
