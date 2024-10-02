function ativarMicrofone() {
    // Verifica se o navegador suporta a API de reconhecimento de voz
    if ('webkitSpeechRecognition' in window) {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = 'pt-BR'; // Define o idioma
        recognition.interimResults = false;

        recognition.onresult = function(event) {
            // Obtém o resultado da gravação
            var resultado = event.results[0][0].transcript;
            // Adiciona o resultado no campo de observações
            document.getElementById('observacoes').value += resultado + ' ';
        };

        recognition.onerror = function(event) {
            console.error('Erro ao reconhecer a fala: ' + event.error);
        };

        recognition.start();
    } else {
        alert('Seu navegador não suporta reconhecimento de voz.');
    }
}

function desativarMicrofone() {
    if (recognition) {
        recognition.stop();
    }
}