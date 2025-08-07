# 🗺️ Guia Completo - Como Conseguir Google Maps API Key

## Passo 1: Acessar Google Cloud Console

1. Acesse: **https://console.cloud.google.com**
2. Faça login com sua conta Google
3. Se for a primeira vez, aceite os termos

## Passo 2: Criar um Projeto

1. No topo da página, clique no **seletor de projeto**
2. Clique em **"NEW PROJECT"** (Novo Projeto)
3. Digite um nome: **"Bot WhatsApp Taxi"**
4. Clique **"CREATE"** (Criar)
5. Aguarde alguns segundos e selecione o projeto criado

## Passo 3: Ativar a API Distance Matrix

1. No menu lateral esquerdo, clique em **"APIs & Services"**
2. Clique em **"Library"** (Biblioteca)
3. Na caixa de pesquisa, digite: **"Distance Matrix API"**
4. Clique na API que aparecer
5. Clique no botão **"ENABLE"** (Ativar)

## Passo 4: Criar Credenciais (API Key)

1. Ainda em **"APIs & Services"**, clique em **"Credentials"**
2. Clique em **"+ CREATE CREDENTIALS"**
3. Selecione **"API key"**
4. Uma janela mostra sua chave:

```
Your API key
AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**COPIE ESSA CHAVE!**

## Passo 5: Configurar a Chave (Importante para Segurança)

1. Clique em **"RESTRICT KEY"** na janela da chave
2. Em **"Application restrictions"**:
   - Selecione **"HTTP referrers (web sites)"**
   - Adicione: `*.replit.dev/*`
   - Adicione: `https://seu-projeto.replit.dev/*`

3. Em **"API restrictions"**:
   - Selecione **"Restrict key"**
   - Marque apenas: ☑️ **Distance Matrix API**

4. Clique **"SAVE"**

## Passo 6: Configurar Cobrança (Obrigatório)

⚠️ **Google exige cartão cadastrado, MAS você não pagará nada no início:**

1. Menu lateral → **"Billing"**
2. **"Link a billing account"**
3. Cadastre cartão de crédito
4. **Você tem $200 USD gratuitos** para começar
5. **40.000 cálculos grátis por mês** (suficiente para 1.300+ corridas)

## Resultado Final:

```
GOOGLE_MAPS_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 💰 Custos Reais:

**Gratuito:**
- Primeiros $200 USD (Google oferece)
- Primeiras 40.000 consultas/mês

**Após esgotar grátis:**
- $5 USD por 1.000 consultas extras
- ~R$ 0,025 por consulta individual

**Para seu negócio:**
- 100 corridas/mês = GRATUITO
- 1.000 corridas/mês = GRATUITO  
- 1.500 corridas/mês = ~R$ 25/mês

## 🔧 Teste Rápido:

Após configurar, teste no navegador:
```
https://maps.googleapis.com/maps/api/distancematrix/json?origins=Cuiabá&destinations=Arsenal&key=SUA_CHAVE_AQUI
```

Deve retornar dados JSON com distâncias.

## ⚠️ Problemas Comuns:

**"This API project is not authorized"**
- Certifique-se que a API está ativada
- Aguarde alguns minutos após ativar

**"REQUEST_DENIED"**  
- Verifique as restrições da chave
- Confirme que o dominio está liberado

**"OVER_QUERY_LIMIT"**
- Você esgotou sua cota gratuita
- Verifique cobrança no console

## 🎯 Resumo dos Locais:

**console.cloud.google.com:**
- Criar projeto ✓
- APIs & Services → Library → Ativar Distance Matrix ✓  
- APIs & Services → Credentials → Criar API Key ✓
- Billing → Cadastrar cartão ✓

## 📋 Checklist Final:

- ✅ Projeto criado
- ✅ Distance Matrix API ativada  
- ✅ API Key gerada
- ✅ Restrições configuradas
- ✅ Cobrança habilitada
- ✅ Testado no navegador

**Sua chave Google Maps está pronta para usar!**