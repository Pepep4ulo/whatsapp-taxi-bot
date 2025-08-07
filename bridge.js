const { Client, LocalAuth, Buttons } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// Dados do motorista
const MOTORISTA_NUMERO = '5566984338952@c.us'; // WhatsApp com DDI + DDD + número + "@c.us"
const MOTORISTA_CARRO = 'Sandero Branco (QBI9I82)';
const MOTORISTA_PIX = '609.950.773-63';

// Chave da API do OpenRouteService
const ORS_API_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE2ZDAwYWFjYzE1MTRkZWFiY2QxNzVmNjJhMjhkNTgwIiwiaCI6Im11cm11cjY0In0='; 

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('📱 Escaneie o QR Code com o número do BOT (atendimento automático).');
});

client.on('ready', () => {
    console.log('✅ Bot conectado ao WhatsApp com sucesso!');
});

const corridasPendentes = {}; // Armazena corridas em aberto

client.on('message', async msg => {
    const texto = msg.body.trim();
    const remetente = msg.from;

    if (msg.from.includes('-')) return; // Ignora grupos

    const partes = texto.split(',');
    if (partes.length !== 3) {
        await msg.reply('❗ Formato inválido.\nEnvie assim:\n\n`Partida, Destino, Nº de pessoas`\n\nExemplo:\n📍Centro, 🏠Bairro Primavera, 2');
        return;
    }

    const [partida, destino, numPessoasStr] = partes.map(p => p.trim());
    const numPessoas = parseInt(numPessoasStr);

    if (isNaN(numPessoas) || numPessoas <= 0) {
        await msg.reply('❗ Número de pessoas inválido. Tente novamente.');
        return;
    }

    try {
        // Função para obter coordenadas via ORS
        const geocodeUrl = `https://api.openrouteservice.org/geocode/search?api_key=${ORS_API_KEY}&text=`;

        const getCoordenadas = async (endereco) => {
            const res = await axios.get(geocodeUrl + encodeURIComponent(endereco));
            if (!res.data.features.length) throw new Error('Endereço não encontrado');
            return res.data.features[0].geometry.coordinates; // [lng, lat]
        };

        const origemCoords = await getCoordenadas(partida);
        const destinoCoords = await getCoordenadas(destino);

        const matrixURL = `https://api.openrouteservice.org/v2/matrix/driving-car`;
        const matrixBody = {
            locations: [origemCoords, destinoCoords],
            metrics: ['distance', 'duration']
        };

        const matrixRes = await axios.post(matrixURL, matrixBody, {
            headers: {
                Authorization: ORS_API_KEY,
                'Content-Type': 'application/json'
            }
        });

        const distanciaMetros = matrixRes.data.distances[0][1];
        const duracaoSegundos = matrixRes.data.durations[0][1];

        const distanciaKm = distanciaMetros / 1000;
        const tempoEstimado = `${Math.floor(duracaoSegundos / 60)} min`;

        // Calcula valor
        let valorCorrida;
        if (numPessoas === 1) {
            valorCorrida = Math.max(15, distanciaKm * 1.5);
        } else {
            valorCorrida = 18;
        }

        const valorFormatado = valorCorrida.toFixed(2).replace('.', ',');

        const resposta = `🛻 *Cotação de Corrida*\n\n📍 *Partida:* ${partida}\n🏁 *Destino:* ${destino}\n👥 *Pessoas:* ${numPessoas}\n🕐 *Tempo estimado:* ${tempoEstimado}\n📏 *Distância:* ${distanciaKm.toFixed(1)} km\n💰 *Valor:* R$ ${valorFormatado}\n\nDeseja confirmar?`;

        const botoes = new Buttons(resposta, ['CONFIRMAR', 'CANCELAR'], '🚕 Corrida Particular com Ismael');

        await msg.reply(botoes);

        corridasPendentes[remetente] = {
            partida,
            destino,
            numPessoas,
            tempoEstimado,
            distanciaKm,
            valor: valorFormatado
        };

    } catch (err) {
        console.error('❌ Erro:', err.message);
        await msg.reply('❗ Erro ao calcular rota. Verifique os endereços e tente novamente.');
    }
});

// Quando o usuário clicar CONFIRMAR ou CANCELAR
client.on('message_create', async msg => {
    const remetente = msg.from;
    const texto = msg.body.trim().toUpperCase();

    if (!corridasPendentes[remetente]) return;

    if (texto === 'CONFIRMAR') {
        const dados = corridasPendentes[remetente];
        delete corridasPendentes[remetente];

        const mensagemMotorista = `🚖 *Nova Corrida Solicitada!*\n\n📍 *Partida:* ${dados.partida}\n🏁 *Destino:* ${dados.destino}\n👥 *Pessoas:* ${dados.numPessoas}\n🕐 *Tempo estimado:* ${dados.tempoEstimado}\n📏 *Distância:* ${dados.distanciaKm.toFixed(1)} km\n💰 *Valor:* R$ ${dados.valor}\n\n🚗 ${MOTORISTA_CARRO}`;

        await client.sendMessage(MOTORISTA_NUMERO, mensagemMotorista);

        await msg.reply(`✅ Corrida confirmada! O motorista foi notificado.\n\nPara pagamento via PIX:\n🔢 *Chave PIX:* ${MOTORISTA_PIX}`);
    } else if (texto === 'CANCELAR') {
        delete corridasPendentes[remetente];
        await msg.reply('❌ Corrida cancelada.');
    }
});

client.initialize();
