const { MongoClient, ServerApiVerison } = require("mongodb");
const { mongoUsername, mongoPassword, mongoDBName} = require ("./credentials");
const fs = require("fs");
const csv = require("csv-parser");

const uri = `mongodb+srv://${mongoUsername}:${mongoPassword}@${mongoDBName}.vbtb9b1.mongodb.net/?retryWrites=true&w=majority`;

const csvFilePath = "test.csv";
const collectionName = "test_collection";



async function uploadCSVToMongoDB() {
  try {
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    await client.connect();
    console.log('Connected to MongoDB');

    const db = client.db(mongoDBName);
    const collection = db.collection(collectionName);

    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on('data', (row) => {
        // Insert each row from the CSV into MongoDB
        collection.insertOne(row);
      })
      .on('end', () => {
        console.log('CSV data has been imported into MongoDB');
        client.close();
      });
  } catch (error) {
    console.error('Error uploading CSV to MongoDB:', error);
  }
}

uploadCSVToMongoDB();
