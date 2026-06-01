"""Aplicação web da Agência de Viagens (Flask).

HU01 — Visualização pública dos itinerários lidos da folha `Base_viagens`.
HU02 — Acesso privado aos dados do cliente através de palavra-chave.
HU03 — Mapa interativo dos destinos com Folium.
HU04 — Sistema de feedback e listagem de comentários.
"""

import os

from flask import Flask, request

import data
import templates
import mapa

app = Flask(__name__)


# Estilo simples para a página
CSS = """
body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f8; color: #333; }
h1 { color: #14507f; }
h2 { color: #1a6fb5; }
table { width: 100%; border-collapse: collapse; background: #fff; margin-top: 20px; }
th { background: #14507f; color: #fff; padding: 10px; text-align: left; }
td { padding: 10px; border-bottom: 1px solid #ddd; }
tr:nth-child(even) { background: #f8fafb; }
.aviso { color: #856404; background: #fff3cd; padding: 10px; margin-top: 20px; }
.erro { color: #c0392b; background: #fdeaea; padding: 10px; margin-top: 10px; }
form { margin-top: 20px; }
input, button, textarea { padding: 8px; margin-top: 5px; }
textarea { width: 300px; height: 80px; }
a { color: #1a6fb5; }
"""


def pagina(titulo, conteudo):
    """Monta uma página HTML completa com cabeçalho e estilo."""
    html = "<!DOCTYPE html><html lang='pt'><head>"
    html += "<meta charset='UTF-8'>"
    html += f"<title>{titulo}</title>"
    html += f"<style>{CSS}</style>"
    html += "</head><body>"
    html += "<h1>Agência de Viagens - Grupo 3</h1>"
    html += ("<p><a href='/'>Início</a> | "
             "<a href='/cliente'>Área do Cliente</a> | "
             "<a href='/feedback'>Feedback</a></p>")
    html += conteudo
    if data.usar_mock():
        html += "<p class='aviso'>Modo demonstração: a usar dados fictícios.</p>"
    html += "</body></html>"
    return html


@app.route('/')
def index():
    """HU01 — Página pública com a tabela de viagens."""
    try:
        viagens = data.get_viagens()
    except Exception:
        viagens = []

    if not viagens:
        return pagina("Erro", "<h2>Erro ao carregar dados</h2>"
                      "<p>Não foi possível ligar à base de dados.</p>")

    conteudo = "<h2>Itinerários disponíveis</h2>"
    conteudo += templates.viagens_publicas(viagens)
    conteudo += "<h2>Mapa dos destinos</h2>"
    conteudo += mapa.criar_mapa(viagens)
    conteudo += "<h2>Feedback dos clientes</h2>"
    conteudo += templates.lista_feedback(data.get_feedback())
    return pagina("Agência de Viagens", conteudo)


@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    """HU02 — Acesso privado aos dados do cliente por palavra-chave."""
    # GET: mostrar o formulário de login
    if request.method == 'GET':
        return pagina("Área do Cliente", templates.formulario_login())

    # POST: verificar a palavra-chave introduzida
    keyword = request.form.get('keyword', '').strip()

    clientes = data.get_clientes()
    headers = clientes[0]
    # A palavra-chave está na última coluna (Keyword_acesso)
    coluna_keyword = len(headers) - 1

    for cliente_linha in clientes[1:]:
        if cliente_linha[coluna_keyword] == keyword and keyword != "":
            conteudo = templates.dados_cliente(cliente_linha, headers)
            return pagina("Área do Cliente", conteudo)

    # Palavra-chave inválida
    erro = "Palavra-chave inválida. Tente novamente."
    return pagina("Área do Cliente", templates.formulario_login(erro))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """HU04 — Formulário de feedback e listagem dos comentários."""
    # GET: mostrar o formulário + lista de feedbacks
    if request.method == 'GET':
        conteudo = templates.formulario_feedback()
        conteudo += "<h2>Feedback dos clientes</h2>"
        conteudo += templates.lista_feedback(data.get_feedback())
        return pagina("Feedback", conteudo)

    # POST: validar e gravar o feedback
    id_viagem = request.form.get('id_viagem', '').strip()
    utilizador = request.form.get('utilizador', '').strip()
    classificacao = request.form.get('classificacao', '').strip()
    comentario = request.form.get('comentario', '').strip()

    # Validar campos obrigatórios
    if not id_viagem or not utilizador or not classificacao or not comentario:
        mensagem = "Por favor preencha todos os campos."
        return pagina("Feedback", templates.formulario_feedback(mensagem))

    sucesso, mensagem = data.add_feedback(id_viagem, utilizador,
                                          classificacao, comentario)
    conteudo = templates.formulario_feedback(mensagem)
    conteudo += "<h2>Feedback dos clientes</h2>"
    conteudo += templates.lista_feedback(data.get_feedback())
    return pagina("Feedback", conteudo)


if __name__ == '__main__':
    # Em produção (Render) o debug fica desligado e a porta vem do ambiente.
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=not data.IS_PRODUCTION)
