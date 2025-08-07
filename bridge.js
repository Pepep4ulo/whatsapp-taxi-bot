const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('📱 Escaneie o QR Code com o WhatsApp do motorista...');
});

client.on('ready', () => {
    console.log('✅ Bot conectado ao WhatsApp com sucesso!');
});

client.on('message', async msg => {
    const userMessage = msg.body;
    const senderNumber = msg.from;

    try {
        // Envia a mensagem para o backend Flask
        const response = await axios.post('http://localhost:5000/webhook', {
            From: senderNumber,
            Body: userMessage
        });

        const resposta = response.data?.message || '✅ Mensagem recebida com sucesso.';

        // Responde no WhatsApp
        await msg.reply(resposta);
        console.log('📨 Resposta enviada para o usuário.');
    } catch (err) {
        console.error('❌ Erro ao enviar mensagem para Flask:', err.message);
        await msg.reply('❗ Ocorreu um erro ao processar sua solicitação.');
    }
});

client.initialize();
