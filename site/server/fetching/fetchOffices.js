const { getDB } = require("../mongoClient");


module.exports = async function fetchOffices({ year }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const offices = await collection.distinct("OFFICE");
        return offices;
    } catch (err) {
        console.error("Fetch Offices | Error: ", err);
        throw err;
    };
};
