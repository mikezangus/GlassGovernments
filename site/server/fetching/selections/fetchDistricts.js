const { getDB } = require("../../../src/lib/mongoClient");


module.exports = async function fetchDistricts({ year, office, state }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const data = await collection.distinct(
            "DISTRICT", {
                OFFICE: office,
                STATE: state
            }
        );
        return data
    } catch (err) {
        console.error("Fetch Districts | Error: ", err);
        throw err
    };
};
