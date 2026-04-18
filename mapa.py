import folium

def criar_mapa(df, coordenadas):
    mapa = folium.Map(location=[-14.79, -39.03], zoom_start=12)

    for praia_nome in df["Praia"].unique():
        df_p = df[df["Praia"] == praia_nome]

        if not df_p.empty:
            ultima = df_p.sort_values("data").iloc[-1]["Classificação"]
            cor = "red" if ultima == "Imprópria" else "green"

            if praia_nome in coordenadas:
                folium.Marker(
                    location=coordenadas[praia_nome],
                    popup=f"{praia_nome} - {ultima}",
                    icon=folium.Icon(color=cor)
                ).add_to(mapa)

    return mapa