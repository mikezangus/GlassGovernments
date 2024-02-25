import getDB from "../../lib/mongoClient";
import fetchYears from "../../lib/fetchYears";


async function createIndexes(db) {
    const years = await fetchYears(db);
    for (const year of years) {
        try {
            await Promise.all([
                db
                    .collection(`${year}_cands`)
                    .createIndex(
                        {
                            OFFICE: 1,
                            STATE: 1,
                            DISTRICT: 1
                        }
                    ),
                db
                    .collection(`${year}_cands`)
                    .createIndex({ CAND_ID: 1 }),
                db
                    .collection(`${year}_conts`)
                    .createIndex({ CAND_ID: 1 })
            ]);
        } catch (err) {
            console.error(`Create Indexes (${year}) | Error: `, err);
        }
    }
};


export default async function handler(req, res) {
    if (req.method === "POST") {
        try {
            const db = await getDB();
            await createIndexes(db);
            res
                .status(200)
                .json(
                    { message: "Indexes created successfully" }
                );
        } catch (err) {
            console.error("Create Indexes | Error: ", err);
            res
                .status(500)
                .json(
                    { error: "Create Indexes | Failure" }
                );
        }
    } else {
        res.setHeader("Allow", ["POST"]);
        res
            .status(405)
            .end(`Method ${req.method} Not Allowed`);
    }
};
