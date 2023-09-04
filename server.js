const express = require('express');
const app = express();
const port = 3000;
const Politician = require('./db');

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

app.get('/', async (req, res) => {
    try {
        const politicians = await Politician.find({});
        res.json(politicians);
    } catch (error) {
        console.error(`Error fetching politicians: ${error}`);
        res.status(500).json({ error: `Internal Server Error`})
    }
});