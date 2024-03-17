import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Legend API";
    if (req.method === "GET") {
        try {
            const { year, state, candId } = req.query;
            if (!year || !state || !candId) {
                return res
                    .status(400)
                    .send(name, " | Prior selections required");
            }
            const db = await getDB();
            const collection = await db.collection(`${year}_conts`);
            const query = {
                CAND_ID: candId,
            };
            const group = {
                _id: "$DOMESTIC",
                COUNT: { $sum: 1 },
                AMT: { $sum: "$AMT" }
            };
            const projection = {
                _id: 0,
                DOMESTIC: "$_id",
                COUNT: 1,
                AMT: 1
            };
            const pipeline = [
                { $match: query },
                { $group: group },
                { $project: projection }
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
    } else {
        res.setHeader("Allow", ["GET"]);
        res
            .status(405)
            .end(`Method ${req.method} Not Allowed`);
    }
};
