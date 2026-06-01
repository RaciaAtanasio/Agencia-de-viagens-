"""Aplicação web da Agência de Viagens (Flask).

HU01 — Visualização pública dos itinerários lidos da folha `Base_viagens`.
"""

from flask import Flask

import data
import templates

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
"""


@app.route('/')
def index():
    """HU01 — Página pública com a tabela de viagens."""
    try:
        viagens = data.get_viagens()
    except Exception:
        viagens = []

    if not viagens:
        return "<h1>Erro ao carregar dados</h1><p>Não foi possível ligar à base de dados.</p>"

    html = "<!DOCTYPE html><html lang='pt'><head>"
    html += "<meta charset='UTF-8'>"
    html += "<title>Agência de Viagens</title>"
    html += f"<style>{CSS}</style>"
    html += "</head><body>"
    html += "<h1>Agência de Viagens - Grupo 3</h1>"
    html += "<h2>Itinerários disponíveis</h2>"
    html += templates.viagens_publicas(viagens)

    if data.usar_mock():
        html += "<p class='aviso'>Modo demonstração: a usar dados fictícios.</p>"

    html += "</body></html>"
    return html


if __name__ == '__main__':
    app.run(debug=True)
