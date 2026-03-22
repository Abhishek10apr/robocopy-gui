// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {

    const startBtn = document.getElementById("startBtn");
    const outputBox = document.getElementById("output");

    startBtn.addEventListener("click", async function () {

        // Get values from input fields
        const source = document.getElementById("source").value.trim();
        const destination = document.getElementById("destination").value.trim();
        const filename = document.getElementById("filename")?.value.trim();

        // Basic validation
        if (!source || !destination) {
            outputBox.innerText = "❌ Please enter source and destination paths.";
            return;
        }

        // Show loading
        outputBox.innerText = "⏳ Copy in progress... Please wait.";

        try {
            // Send request to backend
            const response = await fetch("http://127.0.0.1:5000/copy", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    source: source,
                    destination: destination,
                    filename: filename || null
                })
            });

            // Check if response is OK
            if (!response.ok) {
                throw new Error("Server error: " + response.status);
            }

            const data = await response.json();

            // Display result
            if (data.success) {
                outputBox.innerText = "✅ " + data.message;
            } else {
                outputBox.innerText = "❌ " + data.message;
            }

        } catch (error) {
            console.error(error);
            outputBox.innerText = "❌ Error: Unable to connect to backend.";
        }

    });

});