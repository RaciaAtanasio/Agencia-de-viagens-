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


def formulario_feedback(mensagem=""):
    """HU04 — Formulário para deixar feedback de uma viagem."""
    html = "<h2>Deixar feedback</h2>"
    if mensagem:
        html += f"<p class='aviso'>{mensagem}</p>"
    html += "<form method='post' action='/feedback'>"
    html += "<label>ID da viagem:</label><br>"
    html += "<input type='text' name='id_viagem'><br>"
    html += "<label>O seu nome:</label><br>"
    html += "<input type='text' name='utilizador'><br>"
    html += "<label>Classificação (1 a 5):</label><br>"
    html += "<input type='number' name='classificacao' min='1' max='5'><br>"
    html += "<label>Comentário:</label><br>"
    html += "<textarea name='comentario'></textarea><br>"
    html += "<button type='submit'>Enviar</button>"
    html += "</form>"
    return html


def formulario_admin(mensagem=""):
    """HU05 — Formulário de acesso administrativo por chave fixa (chave.json)."""
    html = "<h2>Acesso Administrativo</h2>"
    if mensagem:
        cls = "erro" if "inv" in mensagem.lower() else "aviso"
        html += f"<p class='{cls}'>{mensagem}</p>"
    html += "<form method='post' action='/admin'>"
    html += "<label>Chave de acesso:</label><br>"
    html += "<input type='password' name='chave'>"
    html += "<button type='submit'>Aceder</button>"
    html += "</form>"
    return html


def tabela_admin(dados, titulo):
    """HU05 — Tabela administrativa (esconde a coluna Keyword_acesso)."""
    if not dados or len(dados) < 2:
        return "<p>Sem dados para apresentar.</p>"

    headers = dados[0]
    html = f"<h2>{titulo}</h2><table>"
    html += "<tr>"
    for h in headers:
        if "keyword" in h.lower() or "senha" in h.lower():
            continue
        html += f"<th>{h}</th>"
    html += "</tr>"

    for row in dados[1:]:
        html += "<tr>"
        for i, valor in enumerate(row):
            if i < len(headers) and ("keyword" in headers[i].lower() or "senha" in headers[i].lower()):
                continue
            html += f"<td>{valor}</td>"
        html += "</tr>"

    html += "</table>"
    return html


def lista_feedback(dados):
    """HU04 — Lista os feedbacks existentes (um por linha)."""
    if not dados or len(dados) < 2:
        return "<p>Ainda não há feedback.</p>"

    html = "<table>"
    headers = dados[0]
    html += "<tr>"
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr>"

    for row in dados[1:]:
        html += "<tr>"
        for valor in row:
            html += f"<td>{valor}</td>"
        html += "</tr>"

    html += "</table>"
    return html
