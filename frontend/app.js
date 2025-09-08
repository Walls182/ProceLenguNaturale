function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;
    addMessage('Tú', message, 'user');
    input.value = '';
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: message })
    })
    .then(res => res.json())
    .then(data => addMessage('ChatBot', data.respuesta, 'bot'));
}

function addMessage(sender, text, cls) {
    const chatlog = document.getElementById('chatlog');
    chatlog.innerHTML += `<div class="${cls}"><b>${sender}:</b> ${text}</div>`;
    chatlog.scrollTop = chatlog.scrollHeight;
}