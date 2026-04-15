import pandas as pd
import os
import matplotlib.pyplot as plt


diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(diretorio_atual, "dados_praias.csv")

df = pd.read_csv(caminho_csv)
df["data"] = pd.to_datetime(df["data"])

print(df.head())
print(df.info())
print(df["classificacao"].value_counts())


df.groupby("data")["classificacao"].value_counts().unstack().plot()

plt.title("Evolução da balneabilidade")
plt.show()

df[df["classificacao"] == "impropria"]["praia"].value_counts().plot(kind="bar")
plt.title("Praias mais impróprias")
plt.show()