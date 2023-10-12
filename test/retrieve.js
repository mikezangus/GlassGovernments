const { MongoClient } = require ("mongodb");
const config = require("./config");

async function retrieveData() {
    try {
        const client = await MongoClient.connect(config.uri);
        const db = client.db(config.database);
        const collection = db.collection(config.collection);
        const data = await collection.find().toArray();
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}

retrieveData();