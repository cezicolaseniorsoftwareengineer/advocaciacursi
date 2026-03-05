# 🚀 Configuração do Render - Dr. Estevão Backend

## Informações do Web Service

### Configuração Básica

- **Nome do Serviço**: `advocacia-cursi-backend`
- **Ambiente**: Python 3.13.1
- **Região**: Oregon (Free Tier)
- **Branch**: `main`

### Comandos de Build e Start

#### Build Command:

```bash
pip install -r backend/requirements.txt
```

#### Start Command:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

### Variáveis de Ambiente (Environment Variables)

Configurar as seguintes variables no Render Dashboard:

| Chave            | Valor    | Descrição                  |
| ---------------- | -------- | -------------------------- |
| `PYTHON_VERSION` | `3.13.1` | Versão do Python           |
| `PORT`           | `$PORT`  | Porta automática do Render |

### Health Check

- **Path**: `/api/v1/chat/init`
- **Método**: POST
- **Expected Status**: 200

### URLs de acesso

Após deploy:

- **Backend API**: `https://advocacia-cursi-backend.onrender.com`
- **Chat Endpoint**: `https://advocacia-cursi-backend.onrender.com/api/v1/chat`

## Endpoints Disponíveis

### 1. Iniciar Sessão

```http
POST /api/v1/chat/init
Content-Type: application/json

{}
```

**Resposta:**

```json
{
  "session_token": "uuid-v4-token",
  "message": "Saudação do Dr. Estevão"
}
```

### 2. Enviar Mensagem

```http
POST /api/v1/chat/message
Content-Type: application/json

{
  "session_token": "uuid-token",
  "message": "Fui demitido sem justa causa"
}
```

**Resposta:**

```json
{
  "session_token": "uuid-token",
  "response": "Resposta do Dr. Estevão",
  "suggests_contact": false,
  "stage": "investigation",
  "area_identificada": "Direito Trabalhista"
}
```

### 3. Registrar Contato

```http
POST /api/v1/chat/contact
Content-Type: application/json

{
  "session_token": "uuid-token",
  "client_name": "João Silva",
  "client_email": "joao@example.com",
  "client_phone": "+5511987654321",
  "preferencia_consulta": "online"
}
```

**Resposta:**

```json
{
  "success": true,
  "request_id": "uuid-v4",
  "client_name": "João Silva",
  "message": "Confirmação",
  "whatsapp_link": "https://wa.me/5511985773185?text=...",
  "whatsapp_message": "Mensagem formatada"
}
```

## Integração com Frontend

### Atualizar chatbot.js

Substituir URL do backend:

```javascript
// Antes (desenvolvimento local)
const backendUrl = "http://localhost:8000/api/v1/chat";

// Depois (produção Render)
const backendUrl = "https://advocacia-cursi-backend.onrender.com/api/v1/chat";
```

### CORS Configurado

O backend aceita requests de:

- `http://localhost:5500` (desenvolvimento)
- `https://*.onrender.com` (produção)
- Domínios customizados (configurar em chat_routes.py)

## Monitoramento

### Logs

Acessar logs em tempo real:

```bash
# No dashboard do Render, seção "Logs"
```

### Métricas

- Requests por segundo
- Tempo de resposta
- Taxa de erro
- Uso de CPU/memória

## Troubleshooting

### Erro: "Application failed to start"

**Solução:**

1. Verificar `Procfile` existe na raiz
2. Confirmar `requirements.txt` em `backend/requirements.txt`
3. Verificar Python version em `runtime.txt`

### Erro: "Module not found"

**Solução:**

```bash
# No Build Command, adicionar:
pip install -r backend/requirements.txt
```

### Erro: CORS

**Solução:**
Adicionar domínio em `backend/ports/chat_routes.py`:

```python
origins = [
    "http://localhost:5500",
    "https://seu-dominio.com"
]
```

## Custos

### Free Tier

- 750 horas/mês (suficiente para 1 serviço 24/7)
- Sleep após 15 minutos de inatividade
- Wake-up automático em novo request (~30s delay)

### Paid Tier (Opcional)

- $7/mês - Instância always-on
- 400h build time/mês
- Sem sleep automático

## Próximos Passos

1. ✅ Deploy inicial concluído
2. ⏳ Testar endpoints em produção
3. ⏳ Atualizar frontend com URL de produção
4. ⏳ Configurar custom domain (opcional)
5. ⏳ Implementar database PostgreSQL (Neon/Render)
6. ⏳ Analytics e monitoramento

---

**Documentação completa**: https://render.com/docs
**Suporte**: support@render.com
