# 📱 Tutorial: Configurar Webhook Twilio

## 🎯 URL do Seu Sistema

**Sua URL completa para webhook:**
```
https://bff91910-990c-4b15-a778-08908ffb9209-00-3n5646a9tthz6.worf.replit.dev/webhook
```

## 📋 Passo a Passo Visual

### 1. Acessar Console Twilio
- Login em: `console.twilio.com`
- Vá para: **Develop → Messaging → Try it out**

### 2. Configurar WhatsApp Sandbox
- Clique em: **"Send a WhatsApp message"**
- Você verá a página do WhatsApp Sandbox

### 3. Encontrar a Seção Webhook
Na página do Sandbox, procure:
```
┌─────────────────────────────────────┐
│ Sandbox Configuration               │
├─────────────────────────────────────┤
│ When a message comes in:            │
│ [_____________________________]    │ ← AQUI!
│                                     │
│ HTTP POST ▼                        │
└─────────────────────────────────────┘
```

### 4. Colar sua URL
No campo "When a message comes in", cole:
```
https://bff91910-990c-4b15-a778-08908ffb9209-00-3n5646a9tthz6.worf.replit.dev/webhook
```

### 5. Salvar Configuração
- Clique em **"Save Configuration"**
- Aguarde confirmação verde

## 📱 Ativar Sandbox no seu WhatsApp

Na mesma página, você verá:
```
┌─────────────────────────────────────┐
│ To start using your sandbox:        │
├─────────────────────────────────────┤
│ Send "join [código]" to:            │
│ +1 (415) 523-8886                  │
│                                     │
│ Example: join purple-elephant       │
└─────────────────────────────────────┘
```

**Do seu WhatsApp pessoal:**
1. Adicione contato: `+1 (415) 523-8886`
2. Envie a mensagem com o código que aparecer
3. Exemplo: `join purple-elephant`

## ✅ Teste Final

**Após configurar tudo:**
1. Envie "oi" para +1 (415) 523-8886
2. O bot deve responder com menu de corridas
3. Siga o fluxo completo

## 🔧 Verificação

**Se não funcionar:**
- Confira se URL está correta (com /webhook no final)
- Verifique se enviou mensagem de ativação
- Aguarde alguns minutos para propagação

**URL sempre atualizada:**
Sua URL pode mudar no Replit. Para verificar a atual:
```bash
echo "https://$REPLIT_DEV_DOMAIN/webhook"
```

## 🎯 Resultado Esperado

Quando configurado, o fluxo será:
```
Cliente → WhatsApp Twilio → Webhook → Seu Sistema → Resposta → Cliente
```

**Tudo automático e em tempo real!**