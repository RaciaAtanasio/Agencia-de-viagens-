"""Geração de HTML para as páginas da Agência de Viagens."""


def viagens_publicas(dados):
    """HU01 — Tabela pública de viagens (esconde as coordenadas geográficas)."""
    if not dados:
        return "<p>Sem dados para apresentar.</p>"

    html = "<table>"
    
    # Cabeçalho
    headers = dados[0]
    html += "<tr>"
    for i, header in enumerate(headers):
        # Esconder latitude e longitude
        if "lat" in header.lower() or "lon" in header.lower():
            continue
        html += f"<th>{header}</th>"
    html += "</tr>"
    
    # Linhas de dados
    for row in dados[1:]:
        html += "<tr>"
        for i, valor in enumerate(row):
            # Esconder latitude e longitude
            if i < len(headers) and ("lat" in headers[i].lower() or "lon" in headers[i].lower()):
                continue
            html += f"<td>{valor}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html
