const { MongoClient, ServerApiVersion } = require('mongodb');
const { mongoUsername, mongoPassword, mongoDBName } = require ("./credentials");
const uri = `mongodb+srv://${mongoUsername}:${mongoPassword}@${mongoDBName}.vbtb9b1.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
});

async function run() {
    try {
        await client.connect();
        await client.db("admin").command({ ping: 1 });
        console.log("Pinged your deployment. You successfully connected to MongoDB!");
    } finally {
        await client.close();
    }
}

module.exports = { run };