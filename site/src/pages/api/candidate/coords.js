import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Coordinates API";
    if (req.method === "GET") {
        try {
            const { year, candID } = req.query;
            if (!year || !candID) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = db.collection(`${year}_contributions`);
            const projection = {
                _id: 0,
                LOCATION: 1
            };
            const contributions = await collection
                .find(
                    { CAND_ID: candID },
                    { projection: projection}
                )
                .toArray();
            const data = contributions
                    .map(contribution => contribution.LOCATION)
                    .filter(location => location != null);
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
