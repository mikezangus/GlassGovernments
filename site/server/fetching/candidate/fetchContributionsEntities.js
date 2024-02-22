const { getDB } = require("../../../src/lib/mongoClient");


module.exports = async function fetchContributionsEntities({ year, candID }) {
    try {
        const db = getDB();
        const collection = db.collection(`${year}_contributions`);
        const match = { CAND_ID: candID };
        const group = {
            _id: "$ENTITY",
            entityContributionAmount: { $sum: "$TRAN_AMT" }
        };
        const pipeline = [
            { $match: match },
            { $group: group }
        ];
        const data = await collection.aggregate(pipeline).toArray();
        return data;
    } catch (err) {
        console.error("Fetch Contrributions Entities | Error: ", err);
        throw err;
    };
};