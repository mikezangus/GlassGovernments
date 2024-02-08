const { getDB } = require("../mongoClient");


module.exports = async function fetchDistricts({ year, office, state }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_candidates`);
        const districts = await collection.distinct(
            "DISTRICT", {
                OFFICE: office,
                STATE: state
            }
        );
        return districts
    } catch (err) {
        console.error("Fetch Districts | Error: ", err);
        throw err
    };
};
