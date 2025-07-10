/*
* Description: 
* Enables a chat interface where user messages are 
* displayed in a chat box, and AI responses are  
* fetched via the SiteSense API. Includes functions to handle 
* form submission, append messages, and type out AI responses.
*
* Version: v2.0
* Author: Alexander Powell
* Dependencies: N/A
*/


const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-input");

function addMessage(text, isUser = false) {
const msg = document.createElement("div");
msg.classList.add("chat-message");
if (isUser) msg.classList.add("user");

// Render HTML if it's from the bot
if (isUser) {
    msg.textContent = text;
} else {
    msg.innerHTML = text;  // <-- this allows links, <p>, <code>, etc.
}

chatBody.appendChild(msg);
chatBody.scrollTop = chatBody.scrollHeight;
}


async function sendToFlaskAPI(message) {
try {
    const response = await fetch(sitesenseAI.apiUrl, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ question: message })
    });

    if (!response.ok) {
    throw new Error("API error");
    }

    const data = await response.json();
    return data.ai_response || "No response received.";
} catch (error) {
    console.error(error);
    return "There was an error connecting to the Site Sense.";
}
}

async function submitMessage() {
const inputText = chatInput.value.trim();
if (!inputText) return;

addMessage("You: " + inputText, true);
chatInput.value = "";

addMessage("Emily is typing...");

const botResponse = await sendToFlaskAPI(inputText);

// Remove the "typing..." message
const lastMessage = chatBody.lastElementChild;
if (lastMessage && lastMessage.textContent === "Emily is typing...") {
    chatBody.removeChild(lastMessage);
}

addMessage("Bot: " + botResponse);
}

chatInput.addEventListener("keypress", function (e) {
if (e.key === "Enter") {
    submitMessage();
}
});
