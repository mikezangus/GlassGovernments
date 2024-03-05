import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Constituency API";
    if (req.method === "GET") {
        try {
            const { year, state, candID } = req.query;
            if (!year || !state || !candID) {
                return res
                    .status(400)
                    .send(name, " | Prior selections required");
            }
            const db = await getDB();
            const collection = await db.collection(`${year}_conts`);
            const query = { CAND_ID: candID };
            const addField = {
                fromCandState:
                    { $eq: ["$STATE", state] }
            };
            const group = {
                _id: "$fromCandState",
                COUNT:
                    { $sum: 1 },
                AMT:
                    { $sum: "$AMT" }
            };
            const projection = {
                _id: 0,
                LOCATION: 
                    { $cond:
                        {
                            if: "$_id",
                            then: "IN",
                            else: "OUT"
                        }
                    },
                COUNT: 1,
                AMT: 1
            };
            const pipeline = [
                { $match: query },
                { $addFields: addField },
                { $group: group },
                { $project: projection }
            ];
            const pipeline2 = [
                { $match: query }
            ]
            const data2 = await collection.aggregate(pipeline2).toArray();

            console.log("DATA: ", data2)

            const data = await collection
                .aggregate(pipeline)
                .toArray();
            res.json(data);
            console.log("CONSTITUENCIES: ", data);
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