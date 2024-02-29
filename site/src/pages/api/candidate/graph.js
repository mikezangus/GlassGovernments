import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Graph API";
    if (req.method === "GET") {
        try {
            const { year, candID } = req.query;
            if (!year || !candID) {
                return res
                    .status(400)
                    .send(name, " | Prior selections required");
            }
            const db = await getDB();
            const collection = db.collection(`${year}_conts`);
            const matchYear = {
                $expr:
                {
                    $gte: [
                        { $year: { $toDate: "$DATE" } },
                        (parseInt(year) - 6)
                    ]
                }
            };
            const query =
            {
                CAND_ID: candID,
                ...matchYear
            };
            const group =
            {
                _id: {
                    YEAR: { $year: { $toDate: "$DATE" } },
                    MONTH: { $month: { $toDate: "$DATE" } }
                },
                AMT: { $sum: "$AMT" }
            };
            const sort = { "_id.YEAR": 1, "_id.MONTH": 1 };
            const projection =
            {
                _id: 0,
                YEAR: "$_id.YEAR",
                MONTH: "$_id.MONTH",
                AMT: 1
            };
            const pipeline = [
                { $match: query },
                { $group: group },
                { $sort: sort },
                { $project: projection }
            ];
            const data = await collection
                .aggregate(pipeline)
                .toArray();
            res.json(data);
            console.log("GRAPH: ", data)
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
            .end(`Method ${req.method} Not Allowed`)
    }
};
