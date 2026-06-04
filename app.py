"""Aplicação web da Agência de Viagens (Flask).

HU01 — Visualização pública dos itinerários lidos da folha `Base_viagens`.
HU02 — Acesso privado aos dados do cliente através de palavra-chave.
HU03 — Mapa interativo dos destinos com Folium.
HU04 — Sistema de feedback e listagem de comentários.
HU05 (complemento) — Vista administrativa por chave fixa lida de `secrets/chave.json`.
"""

import os

from flask import Flask, request

import data
import templates
import mapa

app = Flask(__name__)


CSS = """
body { font-family: sans-serif; background: #f0f4f8; color: #2c3e50; padding: 30px; }
header { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
h1 { color: #14507f; margin: 0 0 10px 0; }
h2 { color: #1a6fb5; margin-top: 30px; }

/* Menu em Botões */
p a { text-decoration: none; color: #1a6fb5; font-weight: bold; padding: 6px 12px; border-radius: 6px; }
p a:hover { background: #1a6fb5; color: white; }

/* Tabelas e Formulários Arredondados */
table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
th { background: #14507f; color: #fff; padding: 12px; text-align: left; }
td { padding: 12px; border-bottom: 1px solid #eef2f5; }
tr:hover { background: #f8fafc; }

form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); max-width: 400px; }
input, textarea, button { width: 100%; padding: 8px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
button { background: #14507f; color: white; font-weight: bold; border: none; cursor: pointer; }
button:hover { background: #1a6fb5; }

.aviso { color: #856404; background: #fff3cd; padding: 10px; border-radius: 6px; }
.erro { color: #c0392b; background: #fdeaea; padding: 10px; border-radius: 6px; }
"""

def pagina(titulo, conteudo):
    """Monta uma página HTML completa com cabeçalho institucional e estilo."""
    html = "<!DOCTYPE html><html lang='pt'><head>"
    html += "<meta charset='UTF-8'>"
    html += f"<title>{titulo}</title>"
    html += f"<style>{CSS}</style>"
    html += "</head><body>"
    
    # --- NOVO CABEÇALHO INSTITUCIONAL ---
    # --- NOVO CABEÇALHO INSTITUCIONAL ---
    html += "<header style='border-bottom: 2px solid #14507f; padding-bottom: 10px; margin-bottom: 20px; text-align: center;'>"
    
    # AQUI ENTRA A VOSSA IMAGEM CORPORATIVA
    
    html += "  <h1 style='margin: 5px 0 0 0;'>Agência de Viagens</h1>"
    html += "  <h3 style='margin-top: 0; color: #1a6fb5;'>Projeto 2 - Grupo 3</h3>"
    html += "  <p style='margin: 3px 0;'><strong>Grupo:</strong> Helder Monteiro, Bruna Monteiro, Liliana Gonçalves e Racia Atanásio</p>"
    html += "  <p style='margin: 3px 0;'><strong>Curso:</strong> MADS, TIWM, IPMaia | <em>junho de 2026</em></p>"
    html += "</header>"
    
    # Menu de Navegação
    html += ("<p><a href='/'>Início</a> | "
             "<a href='/cliente'>Área do Cliente</a> | "
             "<a href='/feedback'>Feedback</a> | "
             "<a href='/admin'>Admin</a></p>")
    
    html += conteudo
    
    if data.usar_mock():
        html += "<p class='aviso'>Modo demonstração: a usar dados fictícios.</p>"
        
    # --- NOVO RODAPÉ ---
    html += "<footer style='margin-top: 40px; padding-top: 15px; border-top: 1px solid #ddd; text-align: center; color: #777; font-size: 0.9em;'>"
    html += "  <p>Instituto Politécnico da Maia</p>"
    html += "</footer>"
    
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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """HU05 (complemento) — Vista administrativa por chave fixa (chave.json)."""
    if request.method == 'GET':
        return pagina("Acesso Admin", templates.formulario_admin())

    chave = request.form.get('chave', '').strip()
    if not chave:
        return pagina("Acesso Admin", templates.formulario_admin(
            "Por favor introduza uma chave."))

    chaves = data.get_chaves()
    if chave not in chaves:
        return pagina("Acesso Admin", templates.formulario_admin(
            "Chave de acesso inválida."))

    destino = chaves[chave]
    if destino == "Clientes":
        dados = data.get_clientes()
        conteudo = templates.formulario_admin() + templates.tabela_admin(dados, "Clientes")
    elif destino == "Base_viagens":
        dados = data.get_viagens()
        conteudo = templates.formulario_admin() + templates.tabela_admin(dados, "Base de Viagens (completa)")
    else:
        conteudo = templates.formulario_admin("Destino não reconhecido.")

    return pagina("Acesso Admin", conteudo)


if __name__ == '__main__':
    # Em produção (Render) o debug fica desligado e a porta vem do ambiente.
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=not data.IS_PRODUCTION)
