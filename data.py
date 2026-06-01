"""Camada de dados da Agência de Viagens.

Lê e escreve dados no Google Sheets através da biblioteca `pygsheets`.
Enquanto o ficheiro de credenciais não estiver disponível, usa dados fictícios
para testar a aplicação localmente.

Estrutura esperada da spreadsheet (3 folhas):
    - Base_viagens:      Id, Destino, Tipo, Data_inicio, Data_fim, Preço_base,
                         Latitude, Longitude, Transporte
    - Clientes:          Id_viagem, Nome_completo, NIF, Telemóvel, Morada, Preco_final, Keyword_acesso
    - Feedback_viagens:  Id_viagem, utilizador, classificacao, comentario
"""

import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IS_PRODUCTION = os.getenv("RENDER") is not None

# Identificador da spreadsheet (key presente no URL do Google Sheets).
SPREADSHEET_KEY = "1oZXOVAyaZZ6ohXhXJ3LxcFeJI0I-RzLVKV5zsl30IIM"

# Nomes das folhas (worksheets).
FOLHA_VIAGENS = "Base_viagens"
FOLHA_CLIENTES = "Clientes"
FOLHA_FEEDBACK = "Feedback_viagens"

# Caminho para o ficheiro de credenciais do Google.
# No Render (produção) os segredos ficam em /etc/secrets; localmente em ./secrets.
if IS_PRODUCTION:
    SERVICE_FILE = Path("/etc/secrets/credenciais.json")
else:
    SERVICE_FILE = BASE_DIR / "secrets" / "credenciais.json"


# --------------------------------------------------------------------------- #
# Ligação ao Google Sheets
# --------------------------------------------------------------------------- #
def conectar_sheets():
    """Autoriza e abre a spreadsheet. Devolve None se não houver credenciais."""
    if not SERVICE_FILE.exists():
        return None

    try:
        import pygsheets
        gc = pygsheets.authorize(service_file=str(SERVICE_FILE))
        sheet = gc.open_by_key(SPREADSHEET_KEY)
        return sheet
    except Exception:
        return None


def usar_mock():
    """True quando a aplicação está a usar dados fictícios (sem credenciais)."""
    return conectar_sheets() is None


# --------------------------------------------------------------------------- #
# Leitura das folhas
# --------------------------------------------------------------------------- #
def get_viagens():
    """Lê a folha `Base_viagens` (cabeçalho + linhas)."""
    sheet = conectar_sheets()
    if sheet is None:
        return list(_MOCK_VIAGENS)

    try:
        wks = sheet.worksheet_by_title(FOLHA_VIAGENS)
        return wks.get_all_values(include_tailing_empty=False,
                                  include_tailing_empty_rows=False)
    except Exception:
        return list(_MOCK_VIAGENS)


def get_clientes():
    """Lê a folha `Clientes` (cabeçalho + linhas)."""
    sheet = conectar_sheets()
    if sheet is None:
        return list(_MOCK_CLIENTES)

    try:
        wks = sheet.worksheet_by_title(FOLHA_CLIENTES)
        return wks.get_all_values(include_tailing_empty=False,
                                  include_tailing_empty_rows=False)
    except Exception:
        return list(_MOCK_CLIENTES)


def get_feedback():
    """Lê a folha `Feedback_viagens` (cabeçalho + linhas)."""
    sheet = conectar_sheets()
    if sheet is None:
        return list(_MOCK_FEEDBACK)

    try:
        wks = sheet.worksheet_by_title(FOLHA_FEEDBACK)
        return wks.get_all_values(include_tailing_empty=False,
                                  include_tailing_empty_rows=False)
    except Exception:
        return list(_MOCK_FEEDBACK)


# --------------------------------------------------------------------------- #
# Escrita
# --------------------------------------------------------------------------- #
def add_feedback(id_viagem, utilizador, classificacao, comentario):
    """Grava uma nova linha de feedback. Devolve (sucesso, mensagem).

    Estrutura: Id_viagem, utilizador, classificacao, comentario.
    """
    nova_linha = [str(id_viagem), str(utilizador), str(classificacao), str(comentario)]

    sheet = conectar_sheets()
    if sheet is None:
        # Modo demonstração: guardar na lista mock para aparecer na listagem
        _MOCK_FEEDBACK.append(nova_linha)
        return True, "Feedback registado (modo demonstração)."

    try:
        wks = sheet.worksheet_by_title(FOLHA_FEEDBACK)
        wks.append_table(values=[nova_linha])
        return True, "Feedback registado com sucesso."
    except Exception:
        return False, "Não foi possível gravar o feedback. Tente novamente."


# --------------------------------------------------------------------------- #
# Dados fictícios (fallback) — usados apenas sem credenciais
# --------------------------------------------------------------------------- #
_MOCK_VIAGENS = [
    ["Id", "Destino", "Tipo", "Data_inicio", "Data_fim", "Preço_base", "Latitude", "Longitude", "Transporte"],
    ["1", "Porto", "Lazer", "2026/01/10", "2026/01/15", "320.00 €", "41.1496", "-8.61099", "Carro (Uber)"],
    ["2", "Madrid", "Negócios", "2026/03/05", "2026/03/08", "210.00 €", "40.4168", "-3.7038", "Avião(TAP), Carro(Europcar)"],
    ["3", "Paris", "Lazer", "2026/07/20", "2026/07/27", "890.00 €", "48.85661", "2.35222", "Avião(TAP), Carro (Uber)"],
    ["4", "Roma", "Histórica", "2026/08/05", "2026/08/12", "720.00 €", "41.9028", "12.4964", "Avião(TAP), Autocarro(FlixBus)"],
    ["5", "Londres", "Negócios", "2026/09/10", "2026/09/13", "550.00 €", "51.5074", "-0.1278", "Avião(TAP), Carro(Europcar)"],
    ["6", "Funchal", "Lazer", "2026/12/20", "2026/12/27", "600.00 €", "32.6500", "-16.9167", "Avião (TAP), Carro(Uber)"],
]

_MOCK_CLIENTES = [
    ["Id_viagem", "Nome_completo", "NIF", "Telemóvel", "Morada", "Preco_final", "Keyword_acesso"],
    ["1", "Ana Silva", "123456789", "912345678", "Rua das Flores 12, Porto",
     "320.00 €", "ana123"],
    ["2", "João Costa", "987654321", "933221144", "Av. da Liberdade 50, Lisboa",
     "210.00 €", "joao456"],
    ["3", "Maria Santos", "456789123", "961122334", "Rua Nova 8, Faro",
     "890.00 €", "maria789"],
    ["4", "Carlos Mendes", "321654987", "910234567", "Praça do Comércio 15, Lisboa",
     "720.00 €", "carlos789"],
    ["5", "Sofia Rodrigues", "654987321", "915678901", "Rua Augusta 42, Lisboa",
     "550.00 €", "sofia123"],
    ["6", "Pedro Alves", "987321654", "919876543", "Avenida da República 88, Lisboa",
     "600.00 €", "pedro456"],
]

_MOCK_FEEDBACK = [
    ["Id_viagem", "utilizador", "classificacao", "comentario"],
    ["1", "Ana Silva", "5", "Viagem muito tranquila e pontual."],
    ["2", "João Costa", "4", "Boa experiência, hotel excelente."],
    ["3", "Maria Santos", "5", "Destino incrível, recomendo vivamente."],
    ["4", "Carlos Mendes", "3", "Bom mas com alguns atrasos no transporte."],
]
