import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Candidates API";
    if (req.method === "GET") {
        try {
            const { year, office, state, district } = req.query;
            if (!year || !office || !state || !district) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = await db.collection(`${year}_cands`);
            const query = {
                OFFICE: office,
                STATE: state,
                DISTRICT: district
            };
            const lookup = {
                from: `${year}_conts`,
                localField: "CAND_ID",
                foreignField: "CAND_ID",
                as: "conts"
            };
            const unwind = {
                path: "$conts",
                preserveNullAndEmptyArrays: true
            };
            const group = {
                _id: {
                    candId: "$CAND_ID",
                    name: "$NAME",
                    party: "$PARTY",
                    district: "$DISTRICT",
                    office: "$OFFICE",
                },
                amt: {
                    $sum: "$conts.AMT"
                }
            };
            const projection = {
                _id: 0,
                candId: "$_id.candId",
                name: "$_id.name",
                party: "$_id.party",
                district: "$_id.district",
                office: "$_id.office",
                amt: 1
            };
            const pipeline = [
                { $match: query },
                { $lookup: lookup },
                { $unwind: unwind },
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
            .end(`Method ${req.method} Not Allowed`)
    }
};
