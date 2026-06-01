"""Testes da aplicação da Agência de Viagens (HU06).

Testes de integração, segurança e funcionalidade:
    - O servidor responde (estabilidade).
    - Dados privados não aparecem sem a palavra-chave correta.
    - Com a palavra-chave correta, os dados privados aparecem.
    - O feedback enviado reflete-se na listagem (persistência).
    - O formulário de feedback valida os campos obrigatórios.

Como correr:
    python -m unittest test_app.py
"""

import unittest

import app
import data


class TestAgenciaViagens(unittest.TestCase):

    def setUp(self):
        """Cria um cliente de teste antes de cada teste."""
        self.cliente = app.app.test_client()

    # --- Estabilidade ------------------------------------------------------ #
    def test_pagina_inicial_responde(self):
        """A página inicial deve responder com sucesso (estabilidade)."""
        resposta = self.cliente.get("/")
        self.assertEqual(resposta.status_code, 200)

    # --- Segurança --------------------------------------------------------- #
    def test_dados_privados_escondidos_sem_senha(self):
        """Sem palavra-chave, a página do cliente não mostra dados privados."""
        resposta = self.cliente.get("/cliente")
        texto = resposta.get_data(as_text=True)
        # O NIF de um cliente não deve aparecer só por abrir a página
        self.assertNotIn("123456789", texto)

    def test_palavra_chave_errada_nao_mostra_dados(self):
        """Com palavra-chave errada, mostra erro e não revela dados."""
        resposta = self.cliente.post("/cliente", data={"keyword": "errada"})
        texto = resposta.get_data(as_text=True)
        self.assertIn("inválida", texto)
        self.assertNotIn("123456789", texto)

    def test_palavra_chave_certa_mostra_dados(self):
        """Com palavra-chave correta, mostra os dados privados do cliente."""
        resposta = self.cliente.post("/cliente", data={"keyword": "ana123"})
        texto = resposta.get_data(as_text=True)
        self.assertIn("Ana Silva", texto)

    # --- Persistência / Funcionalidade ------------------------------------ #
    def test_feedback_aparece_na_listagem(self):
        """Um feedback enviado deve aparecer na listagem (persistência)."""
        self.cliente.post("/feedback", data={
            "id_viagem": "1",
            "utilizador": "Teste Unitario",
            "classificacao": "5",
            "comentario": "Comentario de teste.",
        })
        resposta = self.cliente.get("/feedback")
        texto = resposta.get_data(as_text=True)
        self.assertIn("Teste Unitario", texto)

    def test_feedback_valida_campos_obrigatorios(self):
        """Enviar feedback com campos vazios deve mostrar aviso de validação."""
        resposta = self.cliente.post("/feedback", data={
            "id_viagem": "",
            "utilizador": "",
            "classificacao": "",
            "comentario": "",
        })
        texto = resposta.get_data(as_text=True)
        self.assertIn("preencha todos os campos", texto)


if __name__ == "__main__":
    unittest.main()
