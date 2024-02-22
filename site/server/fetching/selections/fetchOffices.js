const { getDB } = require("../../../src/lib/mongoClient");


module.exports = async function fetchOffices({ year }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const data = await collection.distinct("OFFICE");
        return data;
    } catch (err) {
        console.error("Fetch Offices | Error: ", err);
        throw err;
    };
};
