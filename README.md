# 🚗 WhatsApp Taxi Bot - Sistema Inteligente para Motoristas

Sistema completo de atendimento automatizado via WhatsApp para motoristas particulares, com cotação instantânea e gestão de corridas.

## 🎯 Funcionalidades

- **Bot WhatsApp Inteligente**: Atendimento 24h com coleta automática de dados
- **Sistema de Preços**: Cálculo automático baseado em distância e passageiros
- **Dashboard Web**: Painel de controle com estatísticas e histórico
- **Economia Inteligente**: Sistema híbrido que reduz custos de API em 90%
- **Notificações Automáticas**: Motorista recebe corridas confirmadas no WhatsApp

## 💰 Modelo de Custos

- **Custo operacional**: ~R$ 0,025 por corrida
- **100 corridas/mês**: R$ 2,50 total
- **Margem de lucro**: 99,86%

## 🚀 Tecnologias

- **Backend**: Python/Flask
- **Integração**: Twilio WhatsApp API
- **Cálculo de Rotas**: Sistema híbrido (coordenadas locais + Google Maps opcional)
- **Frontend**: Bootstrap 5 com tema dark
- **Armazenamento**: JSON (escalável para banco de dados)

## 📦 Instalação

### Pré-requisitos
- Python 3.11+
- Conta Twilio (WhatsApp API)
- Google Maps API Key (opcional)

### Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/whatsapp-taxi-bot.git
cd whatsapp-taxi-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token  
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
DRIVER_PHONE=whatsapp:+5565999999999
DRIVER_PIX=sua_chave_pix
GOOGLE_MAPS_API_KEY=sua_chave_opcional
```

4. Execute a aplicação:
```bash
python main.py
```

## 📱 Como Usar

### Para Clientes:
1. Enviar "oi" para o número WhatsApp configurado
2. Informar número de passageiros (1-4)
3. Informar endereço de partida
4. Informar destino
5. Receber cotação automática
6. Confirmar ou cancelar a corrida

### Para Motoristas:
- Acesse o dashboard em `/rides` para monitorar corridas
- Receba notificações automáticas no WhatsApp para corridas confirmadas
- Acompanhe estatísticas e receita total

## 🎯 Fluxo de Negócio

```
Cliente → WhatsApp Bot → Coleta Dados → Calcula Preço → 
Cliente Confirma → Notifica Motorista → Corrida Realizada
```

## 📊 Dashboard

- Lista completa de corridas
- Estatísticas de conversão
- Monitoramento de custos
- Receita total calculada
- Uso de APIs em tempo real

## 🔧 Configuração do Webhook

No console Twilio:
1. Vá em Messaging → Try it out → WhatsApp
2. Configure webhook: `https://seu-dominio.com/webhook`
3. Ative o sandbox enviando mensagem de join

## 🏗️ Arquitetura

### Sistema Híbrido Inteligente
- **90% das consultas**: Cálculo local por coordenadas conhecidas
- **10% das consultas**: Google Maps API para locais novos
- **Cache automático**: Reutiliza cálculos anteriores
- **Fallback**: Estimativa segura se APIs falharem

### Estrutura de Arquivos
```
├── main.py              # Entrada da aplicação
├── app.py               # Configuração Flask
├── whatsapp_bot.py      # Lógica do bot
├── distance_calculator.py # Sistema híbrido de cálculo
├── pricing.py           # Lógica de preços
├── models.py            # Modelos de dados
├── data_store.py        # Persistência JSON
├── templates/           # Templates HTML
├── static/              # CSS/JS/Assets
└── docs/                # Documentação
```

## 🎨 Customização

### Preços
Edite `pricing.py` para ajustar:
- Valor por quilômetro
- Preços mínimos por passageiro
- Regras especiais

### Locais Conhecidos  
Adicione novos bairros em `distance_calculator.py`:
```python
known_locations = {
    'novo_bairro': (-15.xxx, -56.xxx),
    # Adicione mais locais...
}
```

### Interface
Modifique templates em `/templates` e estilos em `/static`

## 📈 Monetização

### Para Freelancers/Desenvolvedores:
- **Desenvolvimento**: Valor único por projeto
- **Gerenciamento mensal**: R$ 50/mês por cliente
- **Escalabilidade**: Múltiplos motoristas na mesma base

### Serviços Adicionais:
- Material de marketing
- Relatórios mensais
- Suporte técnico
- Expansão para múltiplos motoristas

## 🔒 Segurança

- Validação de entrada em todas mensagens
- Rate limiting automático
- Logs detalhados para auditoria
- Configuração segura de webhooks

## 📞 Suporte

Para dúvidas sobre implementação ou customização:
- Abra uma issue no GitHub
- Consulte a documentação em `/docs`

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Casos de Uso

- **Motoristas particulares** individuais
- **Empresas de transporte** pequenas/médias
- **Cooperativas** de motoristas
- **Serviços de turismo** local

---

**Desenvolvido para motoristas que querem profissionalizar seu atendimento com tecnologia acessível.**