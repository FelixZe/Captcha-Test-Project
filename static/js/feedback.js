document.addEventListener("DOMContentLoaded", function () {
    const feedbackForm = document.getElementById("feedbackForm");
    const feedbackResponseMessage = document.getElementById("responseMessage");

    feedbackForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // ⛔ Verhindert GET-Request (Standardaktion)

        const name = document.getElementById("name").value.trim();
        const message = document.getElementById("message").value.trim();

        if (!message) {
            feedbackResponseMessage.textContent = "Bitte geben Sie eine Nachricht ein.";
            feedbackResponseMessage.style.color = "red";
            return;
        }

        try {
            const response = await fetch("/feedback", {
                method: "POST", // ✅ Richtige Methode setzen
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, message }),
            });

            const result = await response.json();
            print("📩 Serverantwort:", result); 

            if (response.ok) {
                feedbackResponseMessage.textContent = "Vielen Dank für Ihr Feedback!";
                feedbackResponseMessage.style.color = "green";
                feedbackForm.reset();
            } else {
                feedbackResponseMessage.textContent = `Fehler: ${result.error}`;
                feedbackResponseMessage.style.color = "red";
            }
        } catch (error) {
            feedbackResponseMessage.textContent = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.";
            feedbackResponseMessage.style.color = "red";
        }
    });
});
