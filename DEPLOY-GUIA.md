# 🎯 Guia de Deploy Dr. Estevão no Render (Passo a Passo)

## Baseado na Tela "New Web Service" do Render

### Passo 1: Conectar Repositório GitHub

Na tela do Render que você mostrou, preencha:

#### **Source Code**

```
https://github.com/cezicolaseniorsoftwareengineer/advocaciacursi
```

✅ Repositório já está público e atualizado

---

### Passo 2: Configurar Informações Básicas

#### **Name** (Nome do serviço)

```
advocacia-cursi-backend
```

✓ Nome único para identificar no dashboard

#### **Project** (Projeto)

```
Default
```

ou crie um novo projeto chamado `Dr Estevão` se preferir organização

---

### Passo 3: Configurar Linguagem e Branch

#### **Language**

```
Python 3
```

#### **Region**

```
Oregon (US West)
```

Região com melhor custo-benefício no free tier

#### **Branch**

```
main
```

---

### Passo 4: Configurar Root Directory (IMPORTANTE!)

#### **Root Directory**

```
.
```

ou deixe em branco (raiz do repositório)

**CRITICAL**: O backend está em `backend/`, mas o Procfile está na raiz, então não especificar subdiretório.

---

### Passo 5: Build Command

Cole exatamente:

```bash
pip install -r backend/requirements.txt
```

**Explicação**: Instala dependências FastAPI, Uvicorn, Pydantic, etc.

---

### Passo 6: Start Command

Cole exatamente:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

**Explicação**: Inicia servidor FastAPI na porta fornecida pelo Render

---

### Passo 7: Instance Type

#### Para testes iniciais:

```
Free
```

✓ 750 horas/mês
✓ Sleep após 15min inatividade
✓ Wake-up automático

#### Para produção (opcional):

```
Starter - $7/mês
```

✓ Always-on
✓ Sem cold starts
✓ Melhor performance

---

### Passo 8: Environment Variables (Advanced)

**Não é obrigatório** para iniciar, mas recomendado:

Clicar em **+ Add Environment Variable** e adicionar:

| Key              | Value    |
| ---------------- | -------- |
| `PYTHON_VERSION` | `3.13.1` |

O Render já detecta automaticamente via `runtime.txt`, mas isso garante consistência.

---

### Passo 9: Review e Deploy

Antes de clicar **"Create Web Service"**, conferir:

- [x] Source Code: repositório GitHub correto
- [x] Name: `advocacia-cursi-backend`
- [x] Language: Python 3
- [x] Branch: `main`
- [x] Build: `pip install -r backend/requirements.txt`
- [x] Start: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- [x] Instance: Free

**Clicar em "Create Web Service"** ✅

---

## O que acontece após clicar "Create"?

### Fase 1: Build (1-3 minutos)

```
[Render] Cloning repository...
[Render] Installing Python 3.13.1...
[Render] Running: pip install -r backend/requirements.txt
[Render] Collecting fastapi==0.109.2
[Render] Successfully installed fastapi uvicorn pydantic...
[Render] Build completed successfully
```

### Fase 2: Deploy (30 segundos - 1 minuto)

```
[Render] Starting service...
[Render] Running: python -m uvicorn backend.app.main:app...
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on 0.0.0.0:10000
[Render] Service is live 🎉
```

### Fase 3: Health Check

```
[Render] Checking /api/v1/chat/init...
[Render] Health check passed ✓
[Render] Service healthy
```

---

## URLs Resultantes

Após deploy bem-sucedido, você receberá:

### Backend API Base URL:

```
https://advocacia-cursi-backend.onrender.com
```

### Endpoints Testáveis:

**Testar Saudação do Dr. Estevão:**

```bash
curl -X POST https://advocacia-cursi-backend.onrender.com/api/v1/chat/init \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta esperada:**

```json
{
  "session_token": "uuid-here",
  "message": "Olá! Sou o Dr. Estevão, advogado com vasta experiência..."
}
```

---

## Troubleshooting Deploy

### ❌ Erro: "Build failed - requirements not found"

**Causa**: Build command incorreto

**Solução**:

```bash
# Build Command correto:
pip install -r backend/requirements.txt
```

### ❌ Erro: "Service failed to start - port binding"

**Causa**: Start command não usa `$PORT` do Render

**Solução**:

```bash
# Start Command correto (com $PORT):
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

### ❌ Erro: "Module 'backend' not found"

**Causa**: Root directory configurado errado

**Solução**: Root Directory = `.` (raiz)

### ⚠️ Warning: "Service is sleeping"

**Causa**: Free tier dorme após 15min inatividade

**Solução**:

- Normal no free tier
- Wake-up automático em ~30s no primeiro request
- Upgrade para Starter ($7/mês) para always-on

---

## Próximo Passo: Integrar Frontend

Após deploy bem-sucedido, atualizar `js/chatbot.js`:

```javascript
// Substituir:
const backendUrl = "http://localhost:8000/api/v1/chat";

// Por:
const backendUrl = "https://advocacia-cursi-backend.onrender.com/api/v1/chat";
```

Deploy do frontend (GitHub Pages ou Vercel):

```bash
git add js/chatbot.js
git commit -m "feat: integra backend Render em produção"
git push origin main
```

---

## Monitoramento

Acessar dashboard Render:

- **Logs**: Ver requests em tempo real
- **Metrics**: CPU, memória, requests/segundo
- **Events**: Histórico de deploys

**URL Dashboard**: https://dashboard.render.com/

---

## Resumo Executivo

✅ **Configuração Validada**:

- Repositório GitHub atualizado com nova persona Dr. Estevão
- `render.yaml` configurado automaticamente
- `Procfile` na raiz do repositório
- `runtime.txt` especifica Python 3.13.1
- `requirements.txt` em `backend/`

✅ **Ready para Deploy**:
Basta preencher formulário do Render conforme instruções acima e clicar "Create Web Service".

⏱️ **Tempo Estimado**: 5-10 minutos total (preenchimento + build + deploy)

---

**Última atualização**: 5 de março de 2026
**Status**: ✅ Código em produção no GitHub
**Commit**: `304e70e - Dr. Estevão Multidisciplinar`
