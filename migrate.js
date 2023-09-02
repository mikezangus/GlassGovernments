const MongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';
const dbName = 'my_database';
const client = new MongoClient(url, { unifiedTopology: true});

const politicians = [
    {
        id: 1,
        name: "Chris Deluzio",
        csvFile: "2022_Deluzio_output.csv",
        incumbency: "Incumbent",
        party: "Democrat",
        constituency: "PA-17",
        photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Rep._Chris_Deluzio_-_118th_Congress.jpg/1280px-Rep._Chris_Deluzio_-_118th_Congress.jpg",
    },
    {
        id: 2,
        name: "Summer Lee",
        csvFile: "2022_Lee_output.csv",
        incumbency: "Incumbent",
        party: "Democrat",
        constituency: "PA-18",
        photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Rep._Summer_Lee_-_118th_Congress.jpg/1280px-Rep._Summer_Lee_-_118th_Congress.jpg",
    },
    {
        id: 3,
        name: "Mike Kelly",
        csvFile: "2022_Kelly_output.csv",
        incumbency: "Incumbent",
        party: "Republican",
        constituency: "PA-16",
        photoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Mike_Kelly%2C_Official_Portrait%2C_112th_Congress.jpg/1024px-Mike_Kelly%2C_Official_Portrait%2C_112th_Congress.jpg",
    },
];

async function main() {
    try {
        await client.connect();
        console.log("Connected correctly to server");
        const db = client.db(dbName);
        const collection = db.collection('politicians');

        // Insert the politicians data
        const result = await collection.insertMany(politicians);
        console.log(`Inserted ${result.insertedCount} documents into the collection`);
    } catch (err) {
        console.log(err.stack);
    } finally {
        await client.close();
    }
}

main().catch(console.error);