import { MongoClient } from "mongodb";


const uri = process.env.URI;
const dbName = process.env.DB;
let cachedDB = null;


export default async function getDB() {
    if (cachedDB) return cachedDB;
    try {
        const client = new MongoClient(uri);
        await client.connect();
        cachedDB = client.db(dbName);
        return cachedDB;
    }
    catch (err) {
        console.error("Failed to connect to database", err);
        throw new Error("Failed to connect to database");
    }
};
