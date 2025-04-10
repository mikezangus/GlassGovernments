import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Graph API";
    if (req.method === "GET") {
        try {
            const { year, state, candID } = req.query;
            if (!year || !state || !candID) {
                return res
                    .status(400)
                    .send(name, " | Prior selections required");
            }
            const db = await getDB();
            const collection = db.collection(`${year}_conts`);
            const filterOutNegativeAmts = {
                $expr: { $gt: ["$AMT", 0] }
            };
            const query = {
                CAND_ID: candID,
                ...filterOutNegativeAmts
            };
            const group = {
                _id: {
                    YEAR: { $year: { $toDate: "$DATE" } },
                    MONTH: { $month: { $toDate: "$DATE" } }
                },
                DOMESTIC_AMT: {
                    $sum: {
                        $cond: [
                            { $eq: ["$DOMESTIC", true] },
                            "$AMT",
                            0
                        ]
                    }
                },
                FOREIGN_AMT: {
                    $sum: {
                        $cond: [
                            { $eq: ["$DOMESTIC", false] },
                            "$AMT",
                            0 
                        ]
                    }
                }
            };
            const filterOutNullDates = {
                "_id.YEAR": { $ne: null },
                "_id.MONTH": { $ne: null }
            };
            const sort = {
                "_id.YEAR": 1,
                "_id.MONTH": 1
            };
            const projection = {
                _id: 0,
                YEAR: "$_id.YEAR",
                MONTH: "$_id.MONTH",
                DOMESTIC_AMT: 1,
                FOREIGN_AMT: 1
            };
            const pipeline = [
                { $match: query },
                { $group: group },
                { $match: filterOutNullDates },
                { $sort: sort },
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
