const { getDB } = require("../../../src/lib/mongoClient");


module.exports = async function fetchYears() {
    try {
        const db = getDB();
        let uniqueYears = new Set();
        const collections = await db.listCollections().toArray();
        const candidateCollections = collections.filter(
            col => col.name.endsWith("candidates")
        );
        for (let collection of candidateCollections) {
            let years = await db.collection(collection.name).aggregate([
                { $match: { ELECTION_YEAR: { $exists: true } } },
                { $group: { _id: "$ELECTION_YEAR" } }
            ]).toArray()
            years.forEach(
                yearDoc => uniqueYears.add(yearDoc._id)
            );
        }
        const data = Array
            .from(uniqueYears)
            .filter(year => year != null)
            .map(String);
        return data
    } catch (err) {
        console.error("Fetch Years | Error: ", err);
        throw err;
    };
};
