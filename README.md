# Agencia de viagens
# Enquadramento

O objetivo central é o desenvolvimento de uma interface web 	realizada em Python, distribuível via GitHub e visualização da mesma utilizando a ferramenta Render.  

A interface web deve permitir a visualização dos transportes utilizados e após uso de uma senha mostrar dados de cliente (ID,Nome , NIF, Telemóvel, Morada, Custo Total e senha de detalhes do utilizador e viagens realizadas) 

# Histórias de utilizador

- **HU01 — Visualização Pública de Itinerários:**  
- Consultar as tabela de viagens (passadas e futuras) para conhecer os destinos oferecidos pela agência. 

- **HU02 — Acesso Privado a Detalhes de Reserva:** 
- Introdução de uma palavra-chave para aceder aos dados pessoais e detalhes confidenciais da reserva. 

- **HU03 — Localização Geográfica em Tempo Real:**  
- Ver a localização dos destinos num mapa para facilitar o planeamento de viagem.    

- **HU04 — Sistema de Feedback e Reputação:** 
- Registar críticas sobre experiência de viagem do cliente para ajudar outros viajantes.

- **HU05 — Infraestrutura e Base de Dados:** 
- Configurar a ligação ao Google Sheets e os dados fictícios de fallback para testar localmente.

- **HU06 — Testes de Integração, Segurança e Funcionalidade:** 
- Garantir que o acesso privado é seguro, que o feedback persiste e que o servidor é estável.

- **HU07 — Documentação e Preparação da Defesa:** 
- Documentar a instalação e execução do projeto e preparar o deploy no Render.

# Tecnologias

- **Python 3** com **Flask** (interface web)
- **pygsheets** (ligação ao Google Sheets)
- **Folium** (mapa interativo dos destinos)
- **gunicorn** (servidor de produção no Render)

# Instalação

1. Clonar o repositório e entrar na pasta do projeto.
2. (Opcional) Criar um ambiente virtual.
3. Instalar as dependências:

```bash
pip install -r requirements.txt
```

# Configuração (Google Sheets)

A aplicação funciona em dois modos:

- **Modo demonstração:** sem credenciais, usa dados fictícios. Não é preciso
  configurar nada para testar localmente.
- **Modo real:** coloca o ficheiro de credenciais da conta de serviço Google em
  `secrets/credenciais.json` (esta pasta está no `.gitignore` e nunca é
  versionada). A app passa automaticamente a ler/escrever no Google Sheets.

# Execução local

```bash
python app.py
```

Depois abrir o endereço indicado no terminal (por omissão a porta 5000).

# Testes

```bash
python -m unittest test_app.py -v
```

# Deploy no Render

O ficheiro `render.yaml` já define o serviço. Configuração equivalente no painel
do Render:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Variável de ambiente:** `RENDER=true` (ativa o modo de produção)

Em produção, as credenciais Google devem ser colocadas como *Secret File* em
`/etc/secrets/credenciais.json`. 

