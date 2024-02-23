import getDB from "../../../lib/mongoClient";
import fetchYears from "../../../lib/fetchYears";


export default async function handler(req, res) {
    if (req.method === "GET") {
        try {
            const db = await getDB();
            const data = await fetchYears(db);
            res.json(data);
        } catch (err) {
            console.error("Years API | Error: ", err);
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
