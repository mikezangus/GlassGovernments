import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Districts API"
    if (req.method === "GET") {
        try {
            const { year, office, state } = req.query;
            if (!year || !office || !state) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = await db.collection(`${year}_candidates`);
            const data = await collection.distinct(
                "DISTRICT",
                {
                    OFFICE: office,
                    STATE: state
                }
            );
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
