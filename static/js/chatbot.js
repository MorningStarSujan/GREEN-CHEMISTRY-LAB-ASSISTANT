document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("chat-form");
    const question = document.getElementById("question");
    const answerBox = document.getElementById("answer-box");
    const answerText = document.getElementById("answer-text");

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const formData = new FormData();
        formData.append("question", question.value);

        const response = await fetch("/ask_ai", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        answerText.textContent = data.answer;

        answerBox.style.display = "block";

        question.value = "";
        question.focus();

    });

});