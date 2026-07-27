document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("chat-form");
    const question = document.getElementById("question");
    const answerBox = document.getElementById("answer-box");
    const answerText = document.getElementById("answer-text");

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const formData = new FormData();
        formData.append("question", question.value);

        // Show loading message
         answerBox.style.display = "block";
         answerText.innerHTML = `
         <div class="ai-loading">
         <div class="spinner"></div>
         
         <h3>🤖 AI Assistant</h3>
         
         <p>Analyzing your chemistry question...</p>
         
         <small>Please wait a moment.</small>
         
         </div>
         `;
         
         const response = await fetch("/ask_ai", {
            
            method: "POST",
            body: formData
        });
        const data = await response.json();
        
        // Render Markdown
         answerText.innerHTML = marked.parse(data.answer);
         
         question.value = "";
         question.focus();
        
        });
    
    });