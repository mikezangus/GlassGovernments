import getDB from "../../lib/mongoClient";
import fetchYears from "../../lib/fetchYears";


async function createCandsIndex(db, year) {
    try {
        await db
            .collection(`${year}_cands`)
            .createIndex({
                OFFICE: 1,
                STATE: 1,
                DISTRICT: 1,
                CAND_ID: 1
            });
    } catch (err) {
        console.error(`Create Candidate Index ${year} | Error: ${err}`);
    }
};


async function createContsIndex(db, year) {
    try {
        await db
            .collection(`${year}_conts`)
            .createIndex({
                CAND_ID: 1,
                STATE: 1,
                CITY: 1
            })
        await db
            .collection(`${year}_conts`)
            .createIndex({
                CAND_ID: 1,
                "LOCATION.coordinates": "2dsphere"
            })
    } catch (err) {
        console.error(`Create Contributions Index ${year} | Error: ${err}`);
    }
};


async function createIndexes(db) {
    const years = await fetchYears(db);
    for (const year of years) {
        try {
            await createCandsIndex(db, year);
            await createContsIndex(db, year);
        } catch (err) {
            console.error(`Create Indexes ${year} | Error: ${err}`);
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
