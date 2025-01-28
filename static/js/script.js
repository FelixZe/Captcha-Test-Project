window.onload = function () {
    // Canvas setup
    const canvas = new fabric.Canvas("sheet");
    const targetNumberElement = document.getElementById("target-number");
    const clearBtn = document.getElementById("clear-btn");
    const submitBtn = document.getElementById("submit-btn");
    const responseMessage = document.getElementById("response-message");
    const refreshBtn = document.getElementById("refresh-btn");

    // Set random target number
    let targetNumber = Math.floor(Math.random() * 10);
    targetNumberElement.textContent = targetNumber;

    refreshBtn.addEventListener("click", () => {
        targetNumber = Math.floor(Math.random() * 5) + 2; // Random number 2-6
        targetNumberElement.textContent = targetNumber;
        canvas.clear();
    });

    // Configure drawing mode
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 26;
    canvas.freeDrawingBrush.color = "#000000";

    // Clear canvas
    clearBtn.addEventListener("click", () => {
        canvas.clear(); // Clear all objects from the canvas
        responseMessage.textContent = "";
    });

    // Submit drawing
    submitBtn.addEventListener("click", async () => {
        // Original Canvas Dimensions
        const originalCanvasWidth = canvas.width; // 200
        const originalCanvasHeight = canvas.height; // 400

        // Create a new padded canvas (400x400)
        const paddedCanvas = document.createElement("canvas");
        paddedCanvas.width = originalCanvasWidth + 200; // Add 100px on each side
        paddedCanvas.height = originalCanvasHeight; // Same height
        const paddedContext = paddedCanvas.getContext("2d");

        // Fill background with white
        paddedContext.fillStyle = "white";
        paddedContext.fillRect(0, 0, paddedCanvas.width, paddedCanvas.height);

        // Draw original canvas in the center of the padded canvas
        const originalDataURL = canvas.toDataURL("image/png"); // Get original canvas data
        const image = new Image();
        image.src = originalDataURL;

        image.onload = async () => {
            paddedContext.drawImage(image, 100, 0); // Center the original canvas (100px padding left/right)

            // Convert padded canvas to Base64
            const dataURL = paddedCanvas.toDataURL(); // Convert to Base64

            // Send the padded image to the server
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
        };
    });
};
