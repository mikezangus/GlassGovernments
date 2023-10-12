const express = require("express");
const { MongoClient } = require("mongodb");
const path = require("path");
const app = express();

const port = process.env.PORT || 3000;
const config = require("./config");
const mongoURI = config.uri;

const client = new MongoClient(mongoURI);

async function startServer() {
    try {
        await client.connect();
        console.log("Connected to MongoDB");
        app.get("/", (req, res) => {
            res.sendFile(path.join(__dirname, "index.html"));
        });
        app.use(express.static(__dirname));

        app.get("/data", async (req, res) => {
            const db = client.db(config.database);
            const collection = db.collection(config.collection);
            const data = await collection.find().toArray();
            res.json(data);
        });
        app.listen(port, () => {
            console.log(`Server is running on http://localhost:${port}`);
        });
    } catch (err) {
        console.error(err);
    }
}

startServer();