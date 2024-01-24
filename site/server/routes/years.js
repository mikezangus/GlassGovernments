const { connectToMongo, getDB } = require("./../mongoClient");


async function fetchYears() {
    await connectToMongo();
    const db = getDB();
    let uniqueYears = new Set();
    const collectionNames = await db.listCollections().toArray();
    const group = { _id: "$election_year" };
    for (let collection of collectionNames) {
        let years = await db.collection(collection.name).aggregate([
            { $group: group }
        ]).toArray();
        years.forEach(yearDoc => uniqueYears.add(yearDoc._id));
    }
    return Array.from(uniqueYears);
};


fetchYears().then(uniqueYears => console.log(uniqueYears)).catch(err => console.error("Error: ", error))