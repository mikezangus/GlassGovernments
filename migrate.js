const { MongoClient, ServerApiVersion } = require('mongodb');
const { mongoUsername, mongoPassword, mongoServerName} = require ("./credentials");
const uri = `mongodb+srv://${mongoUsername}:${mongoPassword}@${mongoServerName}.vbtb9b1.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
});

async function main() {
    try {
        await client.connect();
        console.log("Connected correctly to MongoDB Atlas");
        const db = client.db("cluster0");
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
        const result = await db.collection("politicians").insertMany(politicians);
        console.log(`Inserted ${result.insertedCount} documents into the collection`);       
    } catch(err) {
        console.log(err.stack);
    } finally {
        await client.close();
    }
}

main().catch(console.error);