const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async(req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const aggregation = await collection.aggregate([
            {
                $group: {
                    _id: "$election_chamber"
                }
            },
            {
                $sort: { _id: 1 }
            }
        ]).toArray();
        res.json(aggregation);
        console.log(aggregation)
    } catch (err) {
        console.error("Error fetching chamber data from mongo: ", err);
        res.status(500).send("Internal server error");
    };
});

module.exports = router;