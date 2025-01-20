document.addEventListener("DOMContentLoaded", function () {
    const feedbackForm = document.getElementById("feedbackForm");
    const feedbackResponseMessage = document.getElementById("responseMessage");

    feedbackForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // ⛔ Verhindert Standardaktion (GET-Request)

        // Eingabefelder referenzieren
        const nameInput = document.getElementById("name");
        const messageTextarea = document.getElementById("message");

        // Werte aus den Feldern lesen
        const name = nameInput.value.trim();
        const messages = messageTextarea.value.trim();

        // Validierung
        if (!messages) {
            feedbackResponseMessage.textContent = "Bitte geben Sie eine Nachricht ein.";
            feedbackResponseMessage.style.color = "red";
            return;
        }

        try {
            const response = await fetch("/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, messages }),
            });

            const result = await response.json();

            if (response.ok) {
                feedbackResponseMessage.textContent = result.message; // Erfolgsmeldung anzeigen
                feedbackResponseMessage.style.color = "green";
            } else {
                feedbackResponseMessage.textContent = result.error || "Ein Fehler ist aufgetreten.";
                feedbackResponseMessage.style.color = "red";
            }
        } catch (error) {
            ffeedbackResponseMessage.textContent = result.message;
            feedbackResponseMessage.style.color = "green";
        } finally {
            // Felder immer zurücksetzen, unabhängig vom Erfolg oder Fehler
            nameInput.value = "";
            messageTextarea.value = "";
        }
    });
});
