const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");

router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        
        const aggregation = await collection.aggregate([
            {
                $match: {
                    candidate_state: state,
                    candidate_district: district,
                    candidate_first_name: firstName,
                    candidate_last_name: lastName
                }
            },
            {
                $group: {
                    _id: "$entity_type_desc",
                    totalAmount: { $sum: "$contribution_receipt_amount" }
                }
            },
            { $sort: { totalAmount: -1 } }
        ]).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching funding by entity from MongoDB:", err);
        res.status(500).send("Internal server error");
    }
});

module.exports = router;