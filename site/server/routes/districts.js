const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");

router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022_house");
        const aggregation = await collection.aggregate([
            {
                $group: {
                    _id: {
                        state: "$candidate_state",
                        district: "$candidate_district"
                    }
                }
            }
        ]).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching data from mongo:", err);
        res.status(500).send("Internal server error");
    };
});

module.exports = router;