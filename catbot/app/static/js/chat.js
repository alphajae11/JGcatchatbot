document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const statusElement = document.getElementById('status');
    const catImageContainer = document.getElementById('cat-image-container');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            addMessage('user', message);
            userInput.value = '';
            await sendMessageStream(message);
        }
    });

    async function sendMessageStream(message) {
        const response = await fetch('/chat_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const token = line.slice(6);
                    if (token.startsWith('Status: ')) {
                        updateStatus(token);
                    } else if (token.startsWith('Fetched cat images: ')) {
                        displayCatImages(token.slice(20).split(', '));
                    } else {
                        botResponse += token;
                        updateBotMessage(botResponse);
                    }
                }
            }
        }

        return botResponse;
    }

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateStatus(status) {
        statusElement.textContent = status;
    }

    function updateBotMessage(message) {
        const lastMessage = chatMessages.lastElementChild;
        if (lastMessage && lastMessage.classList.contains('bot')) {
            lastMessage.textContent = message;
        } else {
            addMessage('bot', message);
        }
    }

    function displayCatImages(imageUrls) {
        catImageContainer.innerHTML = '';
        imageUrls.forEach(url => {
            const img = document.createElement('img');
            img.src = url;
            img.alt = 'Cat';
            catImageContainer.appendChild(img);
        });
    }
});