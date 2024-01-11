const { MongoClient } = require("mongodb");
const path = require("path");
const fs = require("fs");

const configPath = path.join(__dirname, "..", "..", "config.json");
const rawConfig = fs.readFileSync(configPath);
const config = JSON.parse(rawConfig);

const uri = `mongodb+srv://${config.mongoUsername}:${config.mongoPassword}@${config.mongoCluster}.px0sapn.mongodb.net/?retryWrites=true&w=majority`;
const client = new MongoClient(uri);

const connectToMongo = async () => {
    try {
        await client.connect();
        console.log(`Connected to cluster at uri:\n${uri}`);
    } catch (err) {
        console.error("Failed to connect to cluster. Error: ", err);
        process.exit(1);
    }
};

const getDB = () => {
    return client.db(config.mongoDatabase);
};

module.exports = { connectToMongo, getDB };