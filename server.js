const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post("/check", (req, res) => {
    const word = req.body.word;
    const pythonProcess = spawn("python", ["main.py", word]);  // Change "python" to "python3" if needed

    pythonProcess.stdout.on("data", (data) => {
        try {
            const suggestions = JSON.parse(data.toString());
            res.json({ corrections: suggestions });
        } catch (error) {
            console.error("JSON Parsing Error:", error);
            res.status(500).json({ error: "Failed to parse Python output." });
        }
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Error from Python script: ${data}`);
        res.status(500).json({ error: "An error occurred while processing your request." });
    });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
