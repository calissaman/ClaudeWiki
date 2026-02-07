const chatArea = document.getElementById("chat-area");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const samples = document.getElementById("samples");

marked.setOptions({
    breaks: true
});

const renderer = new marked.Renderer();
renderer.link = function ({ href, title, text }) {
    const titleAttr = title ? ` title="${title}"` : "";
    return `<a href="${href}"${titleAttr} target="_blank" rel="noopener noreferrer">${text}</a>`;
};
marked.use({ renderer });

function addMessage(role, content) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    if (role === "assistant") {
        div.innerHTML = DOMPurify.sanitize(marked.parse(content), {
            ALLOWED_TAGS: ['p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'blockquote'],
            ALLOWED_ATTR: ['href', 'target', 'rel', 'title']
        });
    } else {
        div.textContent = content;
    }
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
    return div;
}

function showLoading() {
    const div = document.createElement("div");
    div.className = "message assistant";
    div.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div>';
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
    return div;
}

async function sendMessage(text) {
    if (!text.trim()) return;

    samples.style.display = "none";
    addMessage("user", text);
    chatInput.value = "";
    sendBtn.disabled = true;
    chatInput.disabled = true;

    const loading = showLoading();
    let accumulated = "";
    let messageDiv = null;

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        if (!res.ok) {
            loading.remove();
            let errorMsg = "Sorry, something went wrong. Please try again.";
            try {
                const errorData = await res.json();
                if (errorData.error && res.status === 400) {
                    errorMsg = errorData.error;
                }
            } catch {}
            addMessage("assistant", errorMsg);
            return;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const parts = buffer.split("\n\n");
            buffer = parts.pop();

            for (const part of parts) {
                const line = part.trim();
                if (!line.startsWith("data: ")) continue;

                let payload;
                try {
                    payload = JSON.parse(line.slice(6));
                } catch {
                    continue;
                }

                if (payload.type === "delta") {
                    if (!messageDiv) {
                        loading.remove();
                        messageDiv = document.createElement("div");
                        messageDiv.className = "message assistant";
                        chatArea.appendChild(messageDiv);
                    }
                    accumulated += payload.content;
                    messageDiv.innerHTML = DOMPurify.sanitize(marked.parse(accumulated), {
                        ALLOWED_TAGS: ['p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'blockquote'],
                        ALLOWED_ATTR: ['href', 'target', 'rel', 'title']
                    });
                    chatArea.scrollTop = chatArea.scrollHeight;
                } else if (payload.type === "done") {
                    if (!messageDiv) {
                        loading.remove();
                    }
                } else if (payload.type === "error") {
                    loading.remove();
                    if (messageDiv) messageDiv.remove();
                    addMessage("assistant", payload.content || "Sorry, something went wrong. Please try again.");
                }
            }
        }

        // If no deltas were received at all
        if (!messageDiv) {
            loading.remove();
            addMessage("assistant", "Sorry, no response received. Please try again.");
        }
    } catch {
        loading.remove();
        if (messageDiv) messageDiv.remove();
        addMessage("assistant", "Sorry, could not reach the server. Please try again.");
    } finally {
        sendBtn.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
    }
}

function askSample(button) {
    sendMessage(button.textContent);
}

chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(chatInput.value);
});
