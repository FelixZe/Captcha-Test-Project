window.onload = function () {
    const canvas = new fabric.Canvas("sheet");
    const targetNumberElement = document.getElementById("target-number");
    const clearBtn = document.getElementById("clear-btn");
    const submitBtn = document.getElementById("submit-btn");
    const responseMessage = document.getElementById("response-message");

    // Set random target number
    let targetNumber = Math.floor(Math.random() * 5) + 2 ; // Random number 0-9
    targetNumberElement.textContent = targetNumber;

    // Configure drawing mode
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 25;
    canvas.freeDrawingBrush.color = "#000000";

    // Clear canvas
    clearBtn.addEventListener("click", () => {
        canvas.clear(); // Clear all objects from the canvas
        responseMessage.textContent = "";
    });

    // Submit drawing
    submitBtn.addEventListener("click", async () => {
        const dataURL = canvas.toDataURL(); // Get image data
        const response = await fetch("/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: dataURL, target: targetNumber }),
        });

        const result = await response.json();
        console.log(result);
        responseMessage.textContent = result.message;
    });
};
