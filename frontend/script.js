const API_URL = "http://127.0.0.1:8000";

const CUSTOMER_ID = "CUS-001";

let sessionId = "session-" + Date.now();


const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");


// ============================================================
// RESTAURANT LOGO
// ============================================================

function restaurantLogo() {

    return `
        <svg viewBox="0 0 64 64" aria-hidden="true">

            <path
                d="M14 35h36"
                fill="none"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
            />

            <path
                d="M18 35c0-11 6-18 14-18s14 7 14 18"
                fill="none"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
            />

            <path
                d="M29 12h6"
                fill="none"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
            />

            <path
                d="M11 40h42"
                fill="none"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
            />

            <path
                d="M17 47h30"
                fill="none"
                stroke="currentColor"
                stroke-width="4"
                stroke-linecap="round"
            />

        </svg>
    `;
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (!message) {
        return;
    }


    addMessage(
        "user",
        message
    );


    messageInput.value = "";

    autoResize();


    sendButton.disabled = true;

    sendButton.innerHTML = `
        <span>Thinking...</span>
    `;


    const loadingId =
        addLoadingMessage();


    try {

        const controller =
            new AbortController();


        const timeout =
            setTimeout(
                () => controller.abort(),
                20000
            );


        const response =
            await fetch(
                `${API_URL}/api/agent/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        session_id:
                            sessionId,

                        customer_id:
                            CUSTOMER_ID,

                        message:
                            message
                    }),

                    signal:
                        controller.signal
                }
            );


        clearTimeout(timeout);


        removeMessage(
            loadingId
        );


        if (!response.ok) {

            throw new Error(
                `Backend returned HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Agent response:",
            data
        );


        handleAgentResponse(
            data
        );


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        removeMessage(
            loadingId
        );


        let errorMessage =
            "⚠️ I couldn't connect to the support server.";


        if (
            error.name ===
            "AbortError"
        ) {

            errorMessage =
                "⏳ The backend took too long to respond.";
        }


        addMessage(
            "assistant",
            errorMessage
        );


    } finally {

        sendButton.disabled =
            false;


        sendButton.innerHTML = `
            <span>Send</span>
            <span class="send-icon">➤</span>
        `;


        messageInput.focus();
    }
}


// ============================================================
// RESPONSE HANDLER
// ============================================================

function handleAgentResponse(data) {

    if (!data) {

        addMessage(
            "assistant",
            "I received an empty response from the agent."
        );

        return;
    }


    if (
        data.type ===
        "security_block"
    ) {

        addMessage(
            "assistant",
            "🛡️ " + data.message
        );

        return;
    }


    if (
        data.type ===
        "authorization_error"
    ) {

        addMessage(
            "assistant",
            "🔐 " + data.message
        );

        return;
    }


    if (
        data.type ===
        "escalation"
    ) {

        addMessage(
            "assistant",
            data.message
        );

        return;
    }


    if (data.message) {

        addMessage(
            "assistant",
            data.message
        );

        return;
    }


    addMessage(
        "assistant",
        "The agent completed your request."
    );
}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    role,
    message
) {

    const wrapper =
        document.createElement("div");


    wrapper.className =
        role === "user"
            ? "message user-message"
            : "message assistant-message";


    // Avatar

    const avatar =
        document.createElement("div");


    avatar.className =
        role === "user"
            ? "avatar user-avatar"
            : "avatar ai-avatar restaurant-message-logo";


    if (role === "user") {

        avatar.textContent =
            "YOU";

    } else {

        avatar.innerHTML =
            restaurantLogo();
    }


    // Content

    const content =
        document.createElement("div");


    content.className =
        "message-content";


    // Name

    const name =
        document.createElement("div");


    name.className =
        "message-name";


    name.textContent =
        role === "user"
            ? "You"
            : "Restaurant AI";


    // Bubble

    const bubble =
        document.createElement("div");


    bubble.className =
        "message-bubble";


    bubble.innerHTML =
        formatResponse(
            message
        );


    content.appendChild(
        name
    );

    content.appendChild(
        bubble
    );


    wrapper.appendChild(
        avatar
    );

    wrapper.appendChild(
        content
    );


    chatMessages.appendChild(
        wrapper
    );


    scrollChatToBottom();
}


// ============================================================
// FORMAT RESPONSE
// ============================================================

function formatResponse(
    message
) {

    if (!message) {
        return "";
    }


    let safeMessage =
        escapeHtml(
            String(message)
        );


    safeMessage =
        safeMessage.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    safeMessage =
        safeMessage.replace(
            /\bORD-\d+\b/g,
            "<strong>$&</strong>"
        );


    safeMessage =
        safeMessage.replace(
            /\bTKT-\d+\b/g,
            "<strong>$&</strong>"
        );


    safeMessage =
        safeMessage.replace(
            /\n/g,
            "<br>"
        );


    return safeMessage;
}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;
}


// ============================================================
// LOADING
// ============================================================

function addLoadingMessage() {

    const id =
        "loading-" +
        Date.now();


    const wrapper =
        document.createElement(
            "div"
        );


    wrapper.className =
        "message assistant-message";


    wrapper.id =
        id;


    const avatar =
        document.createElement(
            "div"
        );


    avatar.className =
        "avatar ai-avatar restaurant-message-logo";


    avatar.innerHTML =
        restaurantLogo();


    const content =
        document.createElement(
            "div"
        );


    content.className =
        "message-content";


    const name =
        document.createElement(
            "div"
        );


    name.className =
        "message-name";


    name.textContent =
        "Restaurant AI";


    const bubble =
        document.createElement(
            "div"
        );


    bubble.className =
        "message-bubble";


    bubble.innerHTML = `
        <div class="loading-dots">

            <span></span>
            <span></span>
            <span></span>

        </div>
    `;


    content.appendChild(
        name
    );

    content.appendChild(
        bubble
    );


    wrapper.appendChild(
        avatar
    );

    wrapper.appendChild(
        content
    );


    chatMessages.appendChild(
        wrapper
    );


    scrollChatToBottom();


    return id;
}


// ============================================================
// REMOVE MESSAGE
// ============================================================

function removeMessage(id) {

    const element =
        document.getElementById(
            id
        );


    if (element) {
        element.remove();
    }
}


// ============================================================
// QUICK ACTION
// ============================================================

function quickMessage(
    message
) {

    messageInput.value =
        message;

    autoResize();

    sendMessage();
}


// ============================================================
// SCROLL
// ============================================================

function scrollChatToBottom() {

    requestAnimationFrame(
        () => {

            chatMessages.scrollTop =
                chatMessages.scrollHeight;

        }
    );
}


// ============================================================
// AUTO RESIZE
// ============================================================

function autoResize() {

    messageInput.style.height =
        "auto";


    messageInput.style.height =
        Math.min(
            messageInput.scrollHeight,
            100
        ) + "px";
}


// ============================================================
// ENTER TO SEND
// ============================================================

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


messageInput.addEventListener(
    "input",
    autoResize
);


// ============================================================
// BACKEND CHECK
// ============================================================

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${API_URL}/health`
            );


        if (response.ok) {

            console.log(
                "Backend connected successfully."
            );
        }

    } catch (error) {

        console.warn(
            "Backend health check failed.",
            error
        );
    }
}


checkBackend();