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


def formulario_login(erro=""):
    """HU02 — Formulário para o cliente introduzir a palavra-chave."""
    html = "<h2>Área do Cliente</h2>"
    if erro:
        html += f"<p class='erro'>{erro}</p>"
    html += "<form method='post' action='/cliente'>"
    html += "<label>Palavra-chave de acesso:</label><br>"
    html += "<input type='password' name='keyword'>"
    html += "<button type='submit'>Entrar</button>"
    html += "</form>"
    return html


def dados_cliente(cliente, headers):
    """HU02 — Mostra os dados privados de um cliente (esconde a palavra-chave)."""
    html = "<h2>Os seus dados</h2>"
    html += "<table>"
    for i, valor in enumerate(cliente):
        nome_coluna = headers[i]
        # Não mostrar a palavra-chave de acesso
        if "keyword" in nome_coluna.lower() or "senha" in nome_coluna.lower():
            continue
        html += f"<tr><th>{nome_coluna}</th><td>{valor}</td></tr>"
    html += "</table>"
    html += "<p><a href='/cliente'>Sair</a></p>"
    return html
