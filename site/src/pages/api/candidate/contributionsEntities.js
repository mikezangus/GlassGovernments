import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Contributions Entities API";
    if (req.method === "GET") {
        try {
            const { year, candID } = req.query;
            if (!year || !candID) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = db.collection(`${year}_contributions`);
            const query = { CAND_ID: candID };
            const group = {
                _id: "$ENTITY",
                entityContributionAmount: { $sum: "$TRAN_AMT" }
            };
            const pipeline = [
                { $match: query },
                { $group: group }
            ];
            const data = await collection
                .aggregate(pipeline)
                .toArray();
            res.json(data);
        } catch (err) {
            console.error(name, " | Error: ", err);
            res
                .status(500)
                .send("Internal server error");
        }
    }
};
