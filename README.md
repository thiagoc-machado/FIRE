
# 📊 F.I.R.E. – Controle Inteligente de Investimentos

F.I.R.E. é uma aplicação web responsiva para controle completo de investimentos, desenvolvida com Django REST Framework e Vue.js, com foco em investidores que desejam uma visão técnica e personalizada do seu portfólio.

## ⚙️ Tecnologias principais

- Backend: Django + DRF + JWT + drf-spectacular
- Frontend: Vue 3 + Tailwind (não incluso neste repositório)
- Banco de dados: PostgreSQL
- Autenticação: JWT via Djoser
- Cotações: Integração com Yahoo Finance (via yfinance)
- Testes: Pytest

---

## 🚀 Como usar a API

### 🔐 Autenticação

#### Registrar usuário
```http
POST /api/users/

{
  "username": "usuario123",
  "email": "usuario@email.com",
  "password": "senhaSegura"
}
```

#### Login
```http
POST /api/auth/jwt/create/

{
  "username": "usuario123",
  "password": "senhaSegura"
}
```

Resposta:
```json
{
  "access": "token_jwt",
  "refresh": "token_refresh"
}
```

#### Headers necessários para requisições protegidas:
```
Authorization: Bearer <access_token>
```

---

## 📁 Endpoints principais

### 📂 Categorias

- `GET /api/core/category/` – Listar categorias
- `POST /api/core/category/` – Criar categoria
```json
{
  "nome": "Tecnologia"
}
```

---

### 🏦 Corretoras

- `GET /api/core/broker/` – Listar corretoras
- `POST /api/core/broker/` – Criar corretora
```json
{
  "nome": "XP Investimentos"
}
```

---

### 📈 Ativos

- `GET /api/assets/` – Listar ativos
- `POST /api/assets/` – Criar ativo
```json
{
  "codigo": "AAPL",
  "nome": "Apple Inc.",
  "categoria": 1,
  "moeda": "USD",
  "frequencia_dividendos": "trimestral"
}
```

- `GET /api/assets/atualizar/` – Atualiza cotações automaticamente via Yahoo Finance

---

### 💼 Operações

- `GET /api/core/operation/` – Listar operações do usuário autenticado
- `POST /api/core/operation/` – Criar operação
```json
{
  "tipo": "COMPRA",
  "ativo": 1,
  "quantidade": 10,
  "valor_compra": 150.0,
  "data": "2024-01-01",
  "dividendos": 5.0,
  "categoria": 1,
  "corretora": 1
}
```

---

## 📄 Documentação Swagger

Acesse a documentação interativa em:
```
/api/docs/
```

---

## 🧪 Testes automatizados

Para rodar os testes:
```bash
pytest
```

---

## 📌 Variáveis de ambiente (.env)

Exemplo:
```
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🗂️ Estrutura esperada

```
fire/
├── backend/
│   ├── config/
│   ├── core/
│   ├── users/
│   ├── manage.py
│   └── requirements.txt
```

---

Desenvolvido com ❤️ por [Thiago] – projeto F.I.R.E.
