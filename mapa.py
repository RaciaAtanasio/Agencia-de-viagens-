"""Geração do mapa interativo dos destinos (HU03).

Usa a biblioteca Folium para criar um mapa com um marcador por destino,
a partir das colunas Latitude e Longitude da folha `Base_viagens`.
"""

import folium


def criar_mapa(viagens):
    """HU03 — Cria um mapa Folium com um marcador por destino.

    `viagens` é uma lista-de-listas (primeira linha = cabeçalho).
    Devolve o HTML do mapa pronto a embeber na página.
    """
    if not viagens:
        return "<p>Sem dados para mostrar no mapa.</p>"

    headers = viagens[0]

    # Descobrir em que coluna estão o destino, a latitude e a longitude
    col_destino = None
    col_lat = None
    col_lon = None
    for i, header in enumerate(headers):
        nome = header.lower()
        if "destino" in nome:
            col_destino = i
        elif "lat" in nome:
            col_lat = i
        elif "lon" in nome:
            col_lon = i

    # Se não houver coordenadas, não dá para fazer o mapa
    if col_lat is None or col_lon is None:
        return "<p>Não há coordenadas para mostrar no mapa.</p>"

    # Mapa centrado mais ou menos na Europa
    mapa = folium.Map(location=[45.0, 5.0], zoom_start=4)

    for row in viagens[1:]:
        try:
            lat = float(row[col_lat])
            lon = float(row[col_lon])
        except (ValueError, IndexError):
            # Coordenadas inválidas: ignorar este destino
            continue

        destino = row[col_destino] if col_destino is not None else "Destino"
        folium.Marker(location=[lat, lon], popup=destino).add_to(mapa)

    # Devolver apenas o HTML do mapa (sem <html>/<body>)
    return mapa._repr_html_()
