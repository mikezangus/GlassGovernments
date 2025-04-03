require("dotenv").config();
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const port = process.env.PORT || 3000;

const BILL_TEXTS_DIR = path.resolve(__dirname, "../data/bill-texts/source");


app.get("/api/bill_text", async(req, res) => {
    try {
        const { congress, type, bill_num } = req.query;
        if (!congress || !type || !bill_num) {
            return res
                .status(400)
                .json({ error: "Missing required parameteres: congress, type, bill_num" });
        }
        const billID = `${String(congress)}_${String(type)}_${String(bill_num)}`;
        const fileName = `${billID}.txt`;
        const filePath = path.join(BILL_TEXTS_DIR, fileName);
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({ error: "File not found" });
        }
        fs.readFile(filePath, "utf8", (err, data) => {
            if (err) {
                return res.status(500).json({ error: "Error reading file"});
            }
            res.json({ text: data });
        });
    } catch (error) {
        res.status(500).json({ error: error.message});
    }
});


app.use((req, res, next) => {
    console.log(`Received request: ${req.method} ${req.url}`);
    next();
});


app.get('/', (req, res) => {
    res.send("API is running");
});


app.use((req, res) => {
    res.status(404).json({ error: "Not found" });
});


app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
