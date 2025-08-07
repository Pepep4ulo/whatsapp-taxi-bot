# 📱 Guia Completo - Como Configurar Twilio WhatsApp

## Passo 1: Criar Conta Twilio (Gratuito)

1. Acesse: **https://www.twilio.com**
2. Clique em "Sign up" (Criar conta)
3. Preencha seus dados
4. Confirme email e telefone

## Passo 2: Encontrar suas Credenciais

### Account SID e Auth Token:

1. **Faça login** no console Twilio
2. Na **tela inicial** (Dashboard), você verá:

```
Account Info
├── Account SID: ACxxxxxxxxxxxxxxxxxxxxx
└── Auth Token: [clique em "show" para ver]
```

**TWILIO_ACCOUNT_SID** = Account SID (começa com "AC")
**TWILIO_AUTH_TOKEN** = Auth Token (string longa)

### WhatsApp Phone Number:

**LOCALIZAÇÃO EXATA:**
1. No menu lateral esquerdo, clique em **"Messaging"**
2. Clique em **"Try it out"** 
3. Clique em **"Send a WhatsApp message"**
4. Na página que abrir, você verá uma caixa com:

```
Your sandbox phone number:
From: whatsapp:+14155238886
```

**COPIE EXATAMENTE ASSIM:**
```
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

**ATENÇÃO:** 
- NÃO remova o "whatsapp:" do início
- NÃO adicione espaços ou caracteres extras
- Copie exatamente como aparece na tela

## Passo 3: Ativar WhatsApp Sandbox

1. Na página do WhatsApp sandbox
2. Você verá instruções tipo:
   ```
   "Para ativar, envie 'join willing-tiger' 
   para +1 415 523 8886"
   ```
3. **Envie essa mensagem** do seu WhatsApp pessoal
4. Você receberá confirmação de ativação

## Passo 4: Configurar Webhook (Importante!)

1. Ainda na página WhatsApp sandbox
2. Procure por **"Webhook Configuration"**
3. Em **"When a message comes in"**, cole:
   ```
   https://SEU-REPLIT.replit.dev/webhook
   ```
4. Clique **"Save Configuration"**

## Exemplo Real de Configuração:

```
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcdef
TWILIO_AUTH_TOKEN=abcdef1234567890abcdef1234567890
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

## 🎯 Resumo dos Locais:

**Dashboard Principal:**
- Account SID ✓
- Auth Token ✓

**Messaging → Try it out → WhatsApp:**
- Phone Number ✓
- Webhook Configuration ✓

## ⚠️ Importante para Produção

O sandbox funciona para **testes**, mas tem limitações:
- Só funciona com números que "joinaram"
- Mensagens têm prefixo automático

Para **produção real** (depois):
- Solicitar número WhatsApp Business dedicado
- Processo de aprovação Facebook/Meta
- Custo adicional

**Para seu projeto freelancer**: O sandbox é perfeito para começar!

## 🔧 Teste Rápido

Depois de configurar, teste:
1. Envie "oi" para seu número sandbox
2. Deve responder com o menu do bot
3. Se não funcionar, verifique webhook e credenciais

## 💰 Custos Twilio

**Sandbox**: Gratuito para testes
**Produção**: ~$0.005 USD por mensagem (~R$ 0,025)

Exatamente o custo que calculamos para o projeto!