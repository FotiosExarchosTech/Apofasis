document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-chat');

    // adds the message
    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'ai-message');
        
        msgDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatBox.appendChild(msgDiv);
        
        // Auto-scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ai loading effect
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'ai-message');
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content typing-indicator">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>`;
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) typingDiv.remove();
    }

    // sending the message
    async function handleSend() {
        const text = userInput.value.trim();
        if (text === '') return; 

        // 1. Print the user's prompt
        appendMessage('user', text);
        userInput.value = '';
        // resizing after clearing or sending the message
        function resetInputHeight() {
            userInput.style.height = '24px';
        }

        userInput.style.height = '24px';

        // 2. Show the AI thinking
        showTypingIndicator();

        // 3. Take the data from the site
        try {
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question: text
                })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();

            removeTypingIndicator();
            appendMessage('ai', data.reply);

        } catch (error) {
            removeTypingIndicator();
            appendMessage('ai', 'Σφάλμα: Δεν μπορώ να συνδεθώ με τον Server.');
            console.error('Error:', error);
        }
    }

    // The user can either click the send button or click Enter
    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey)
        { 
            e.preventDefault();
            handleSend();
        }
    });

    // Chat clearing
    clearBtn.addEventListener('click', () => {
        chatBox.innerHTML = `
            <div class="message ai-message">
                <div class="message-content">Γεια σου!👋<br> Πώς μπορώ να βοηθήσω;</div>
            </div>`;
    });

    // autoresize
    userInput.addEventListener('input', function() {
        this.style.height = 'auto'; // Μηδενισμός για σωστό υπολογισμό
        this.style.height = (this.scrollHeight) + 'px'; // Νέο ύψος όσο το κείμενο
        
        // scroll begins after a limit
        if (this.scrollHeight > 120) {
            this.style.overflowY = "auto";
        } else {
            this.style.overflowY = "hidden";
        }
    });
});