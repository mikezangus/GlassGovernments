import getDB from "../../../lib/mongoClient";


export default async function handler(req, res) {
    const name = "Offices API";
    if (req.method === "GET") {
        try {
            const { year } = req.query;
            if (!year) return res
                .status(400)
                .send(name, " | Prior selections required");
            const db = await getDB();
            const collection = await db.collection(`${year}_candidates`);
            const data = await collection.distinct("OFFICE");
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
