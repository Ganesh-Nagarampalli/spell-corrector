async function checkSpelling() {
    const word = document.getElementById("wordInput").value;
    try {
        const response = await fetch("http://127.0.0.1:5000/check", {  // Update this URL if deploying
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ word: word })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Clear previous results
        const resultElement = document.getElementById("result");
        resultElement.innerHTML = ""; // Clear previous suggestions
        
        // Loop through each correction and display
        if (data.corrections && Array.isArray(data.corrections)) {
            data.corrections.forEach(correction => {
                const item = document.createElement("p");
                item.innerText = `Suggested correction: ${correction[0]} (Probability: ${correction[1].toFixed(5)})`;
                resultElement.appendChild(item);
            });
        } else {
            resultElement.innerText = "No corrections found.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "An error occurred while checking the spelling.";
    }
}
