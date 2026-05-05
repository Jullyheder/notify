# Notify

Aplicação Django responsável por receber webhooks do SGE (Sistema de Gestão de Estoque), registrar os eventos recebidos e disparar notificações por WhatsApp e e-mail quando uma nova saída de pedido é registrada.

## Funcionalidades

- Recebimento de webhooks via API REST.
- Persistência dos eventos recebidos no banco SQLite.
- Cálculo do valor total da venda, custo total e lucro.
- Envio de mensagem pelo CallMeBot.
- Envio de e-mail HTML para o administrador.
- Visualização dos webhooks recebidos pelo Django Admin.

## Tecnologias

- Python
- Django 6
- Django REST Framework
- SQLite
- python-dotenv
- requests
- CallMeBot API

## Estrutura do projeto

```text
notify/
├── app/                  # Configurações principais do Django
├── services/             # Serviços externos, como integração com CallMeBot
├── webhooks/             # App responsável pelos webhooks
│   ├── templates/        # Templates de e-mail
│   ├── models.py         # Modelo Webhook
│   ├── views.py          # Endpoint de recebimento dos webhooks
│   └── messages.py       # Mensagens enviadas nas notificações
├── manage.py
├── requirements.txt
└── .env.example
```

## Requisitos

- Python 3.12 ou superior
- Conta/configuração do CallMeBot
- Servidor SMTP para envio de e-mails

## Configuração

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Copie o arquivo de exemplo das variáveis de ambiente:

```bash
copy .env.example .env
```

Preencha o arquivo `.env`:

```env
SECRET_KEY=

CALLMEBOT_API_URL=
CALLMEBOT_PHONE_NUMBER=
CALLMEBOT_API_KEY=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_ADMIN_RECEIVER=
```

### Variáveis de ambiente

| Variável | Descrição |
| --- | --- |
| `SECRET_KEY` | Chave secreta usada pelo Django. |
| `CALLMEBOT_API_URL` | URL base da API do CallMeBot. |
| `CALLMEBOT_PHONE_NUMBER` | Número de telefone autorizado no CallMeBot. |
| `CALLMEBOT_API_KEY` | Chave da API do CallMeBot. |
| `EMAIL_HOST` | Host SMTP usado para envio de e-mails. |
| `EMAIL_PORT` | Porta SMTP. |
| `EMAIL_HOST_USER` | Usuário/remetente do SMTP. |
| `EMAIL_HOST_PASSWORD` | Senha do SMTP. |
| `EMAIL_ADMIN_RECEIVER` | E-mail que receberá as notificações. |

## Banco de dados

Execute as migrações:

```bash
python manage.py migrate
```

Opcionalmente, crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

## Execução

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Por padrão, a aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

O painel administrativo fica em:

```text
http://127.0.0.1:8000/admin/
```

## Endpoint

### Receber webhook de saída de pedido

```http
POST /api/v1/webhooks/order/
```

Payload esperado:

```json
{
  "event_type": "outflow.created",
  "product": "Produto exemplo",
  "quantity": 2,
  "product_selling_price": 50.0,
  "product_cost_price": 30.0,
  "timestamp": "2026-05-05 10:30:00"
}
```

Exemplo com `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/webhooks/order/ \
  -H "Content-Type: application/json" \
  -d "{\"event_type\":\"outflow.created\",\"product\":\"Produto exemplo\",\"quantity\":2,\"product_selling_price\":50.0,\"product_cost_price\":30.0,\"timestamp\":\"2026-05-05 10:30:00\"}"
```

Resposta esperada:

```json
{
  "product": "Produto exemplo",
  "quantity": 2,
  "product_selling_price": 50.0,
  "product_cost_price": 30.0,
  "timestamp": "2026-05-05 10:30:00",
  "total_value_selling": "100,00",
  "total_value_cost": "60,00",
  "profit_value": "40,00"
}
```

## Fluxo do webhook

1. A API recebe o payload em `/api/v1/webhooks/order/`.
2. O campo `event_type` é separado do restante dos dados.
3. O evento recebido é salvo na tabela `webhooks`.
4. A aplicação calcula o valor total da venda, o custo total e o lucro.
5. Uma mensagem é enviada via CallMeBot.
6. Um e-mail HTML é enviado para o administrador configurado em `EMAIL_ADMIN_RECEIVER`.
7. A API retorna os dados recebidos com os valores calculados.

## Observações

- O projeto usa SQLite por padrão, por meio do arquivo `db.sqlite3`.
- O arquivo `.env` contém dados sensíveis e não deve ser versionado.
- O endpoint espera que `quantity`, `product_selling_price` e `product_cost_price` sejam valores numéricos.
- Em ambiente de produção, revise `DEBUG`, `ALLOWED_HOSTS` e demais configurações de segurança do Django.
