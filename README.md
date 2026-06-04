# Agencia de viagens
# Enquadramento

O objetivo central é o desenvolvimento de uma interface web realizada em Python, distribuível via GitHub e disponibilizada publicamente através da ferramenta Render.

A aplicação lê os dados de uma Google Spreadsheet com três folhas (`Base_viagens`, `Clientes` e `Feedback_viagens`) e oferece:

- Uma **vista pública** com a tabela de itinerários (Id, Destino, Tipo, datas, Preço base e Transporte) e um mapa interativo dos destinos.
- Uma **área privada** onde, após introduzir uma palavra-chave, o cliente vê os seus dados de reserva (Nome, NIF, Telemóvel, Morada e Preço final).
- Um **sistema de feedback** onde os clientes deixam uma classificação (1 a 5) e um comentário sobre a viagem.

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

## Criar as credenciais Google Cloud

Para ligar a app a um Google Sheet real:

1. Aceder ao [Google Cloud Console](https://console.cloud.google.com).
2. Criar um projeto (ou usar um existente).
3. Ativar a API **Google Sheets API**.
4. Ir a `IAM & Admin > Service Accounts` e criar uma conta de serviço.
5. Dentro da conta de serviço, criar uma chave do tipo **JSON**.
6. Descarregar o ficheiro `.json` e colocá-lo em `secrets/credenciais.json` (local) ou como *Secret File* no Render (produção).
7. Copiar o email da conta de serviço e partilhar o Google Sheet com esse email (como leitor e editor).

# Execução local

```bash
python app.py
```

Depois abrir o endereço indicado no terminal (por omissão a porta 5000).

## Mapa interativo

O mapa (HU03) é gerado pela biblioteca **Folium** a partir das colunas `Latitude` e `Longitude` da folha `Base_viagens`. A aplicação cria um marcador para cada destino; se as coordenadas estiverem em falta ou num formato inválido, o marcador é ignorado sem interromper o mapa.

# Testes

```bash
python -m unittest test_app.py -v
```

## O que os testes verificam

A suite de 6 testes cobre os seguintes cenários:

1. **Estabilidade** — a página inicial responde com HTTP 200.
2. **Segurança (acesso sem senha)** — ao aceder a `/cliente` sem POST, o NIF de um cliente não aparece.
3. **Segurança (senha errada)** — com palavra-chave errada, a página mostra "inválida" e continua a não revelar dados privados.
4. **Segurança (senha correta)** — com a palavra-chave correta, os dados privados (ex: "Ana Silva") são apresentados.
5. **Persistência de feedback** — um comentário submetido aparece na listagem.
6. **Validação de campos** — enviar o formulário com campos vazios mostra a mensagem "preencha todos os campos".

# Deploy no Render

O ficheiro `render.yaml` já define o serviço. Configuração equivalente no painel
do Render:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Variável de ambiente:** `RENDER=true` (ativa o modo de produção)

Em produção, as credenciais Google devem ser colocadas como *Secret File* em
`/etc/secrets/credenciais.json`. 

