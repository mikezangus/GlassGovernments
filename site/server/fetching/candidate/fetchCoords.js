const { getDB } = require("../../mongoClient");


module.exports = async function fetchCoords({ year, candID }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_contributions`);
        const projection = { _id: 0, LOCATION: 1 };
        const contributions = await collection.find(
            { CAND_ID: candID },
            { projection: projection}
        ).toArray();
        const coords = contributions
            .map(
                contribution => contribution.LOCATION
            )
            .filter(
                location => location != null
            )
        return coords;
    }
    catch (err) {
        console.error("Error:", err);
        throw err;
    }
}