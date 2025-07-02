/*
* Description: 
* Enables a chat interface where user messages are 
* displayed in a chat box, and AI responses are  
* fetched via the SiteSense API. Includes functions to handle 
* form submission, append messages, and type out AI responses.
*
* Version: v1.6
* Author: Alexander Powell
* Dependencies: N/A
*/


/**
 * Handles the form submission, processes the user's message, and retrieves an AI response.
 * 
 * This function prevents the default form submission behavior, retrieves the message input,
 * disables the submit button to prevent multiple submissions, and sends the message to the AI 
 * for processing. Once the AI response is received, it is appended to the chat window. The 
 * form is then reset, and the submit button is re-enabled.
 * 
 * @param {Event} event - The submit event triggered when the form is submitted.
 * 
 * @returns {void} - This function does not return any value. It handles the form submission
 * and updates the chat box with the user and AI messages.
 */
async function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form submission

    // Get message text from input
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const humanMessage = data.message;

    // Clear the input field
    event.target.reset();

    // Reset the textarea height after submission
    const textarea = document.querySelector('.emily_chat');
    textarea.style.height = 'auto'; // Reset height to auto
    textarea.style.height = '50px'; // Set it to the default size

    // Disable button to prevent errors
    const submitButton = document.getElementById("ai-submitButton");
    submitButton.disabled = true;

    if (!humanMessage.trim()) return; // Ignore empty messages

    // Append the user's message
    appendMessage(humanMessage, 'user');

    // Append a temporary AI message bubble with "Thinking..."
    const chatBox = document.getElementById('ai-chat-box');
    const thinkingMessage = document.createElement('div');
    thinkingMessage.classList.add('ai-message', 'ai');
    thinkingMessage.textContent = "Thinking...";
    chatBox.appendChild(thinkingMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Get an AI response
    const aiResponse = await generateAIResponse(humanMessage);

    // Replace the "Thinking..." text with the typed AI response
    thinkingMessage.innerHTML = ""; // Clear the thinking message
    typeMessage(thinkingMessage, aiResponse); // Type out the response

    submitButton.disabled = false;
}


/**
 * Appends a new message bubble to the chat box.
 * 
 * This function creates a new message bubble (a `div` element), adds the specified text
 * to it, and appends it to the chat box. It also ensures the chat box scrolls to the 
 * bottom to display the latest message.
 * 
 * @param {string} text - The text content to be displayed in the message bubble.
 * @param {string} type - The type of message ('ai' or 'user') to style the message bubble accordingly.
 * 
 * @returns {void} - This function does not return any value.
 */
function appendMessage(text, type) {
    const messageBubble = document.createElement('div');
    messageBubble.classList.add('ai-message', type);

    const chatBox = document.getElementById('ai-chat-box');
    chatBox.appendChild(messageBubble);

    // Set the sanitized HTML to the message bubble
    if (type === 'ai') {
        typeMessage(messageBubble, text); // Type the message with a typing effect
    } else {
        messageBubble.innerHTML = text; // User messages appear instantly
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


/**
 * Simulates a typing effect by gradually appending characters to an element.
 *
 * @param {HTMLElement} element - The HTML element where the text will be displayed.
 * @param {string} text - The full text that should appear with the typing effect.
 * @param {number} delay - The delay (in milliseconds) between each character being added.
 */
function typeMessage(element, text) {
    let i = 0;
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = text;
    let content = tempDiv.innerHTML;

    function typeChar() {
        if (i < content.length) {
            element.innerHTML = content.substring(0, i + 1);
            i++;
            setTimeout(typeChar, 30);
        }
    }

    typeChar();
}


/**
 * Sends a question to the SiteSense AI API and retrieves the AI-generated response.
 * 
 * This function sends a POST request to the backend API with a user's question and waits 
 * for the AI's response. Once the response is received, it processes the JSON and returns
 * the AI's answer.
 * 
 * @param {string} humanMessage - The question to be sent to the AI for processing.
 * @returns {Promise<string|Object>} - A promise that resolves to the AI's response (string), 
 * or an error message (Object) if the API call fails.
 * 
 * @throws {Error} - If the API call fails or the response is not in the expected format.
 */
async function generateAIResponse(humanMessage) {
    const data = { 
        question: humanMessage 
    };

    try {
        const response = await fetch(sitesenseAI.apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            console.log("response not okay");
            throw new Error(`HTTP error! Status: ${response.status}`);
        } 

        const jsonResponse = await response.json();
        console.log(jsonResponse[1]);
        return jsonResponse[1];
    } catch (error) {
        console.error("Error:", error);
        return "There was an error generating a response. If this continues please contact sunsigndesigns.com";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const msg = "Hello, im Emily! Your personal Web AI assistant here to " + 
    "answer all your website questions. Ask me anything web related!!";

    // Append a welcome message from the AI when the page loads
    appendMessage(msg, 'ai');

    // Add auto-expanding textarea behavior
    const textarea = document.querySelector('.emily_chat');

    textarea.addEventListener('input', () => {
      textarea.style.height = 'auto'; // Reset height to auto to recalculate height
      textarea.style.height = `${textarea.scrollHeight}px`; // Set height to scrollHeight to match content
    });
});
