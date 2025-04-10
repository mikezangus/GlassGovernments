import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "States API";
    if (req.method === "GET") {
        try {
            const { year, office } = req.query;
            if (!year || !office) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = await db.collection(`${year}_cands`);
            const data = await collection.distinct(
                "STATE",
                {OFFICE: office}
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
