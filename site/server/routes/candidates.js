const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");

router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022_house");
        const { state, district } = req.query;
        let matchStage = {};
        if (state && district) {
            matchStage = {
                $match: {
                    candidate_state: state,
                    candidate_district: district
                }
            };
        };
        const aggregationStages = [
            matchStage,
            {
                $group: {
                    _id: {
                        firstName: "$candidate_first_name",
                        lastName: "$candidate_last_name",
                        state: "$candidate_state",
                        district: "$candidate_district",
                        party: "$candidate_party"
                    },
                    totalFunding: { $sum: "$contribution_receipt_amount" }
                }
            }
        ].filter(stage => Object.keys(stage).length > 0);
        const aggregation = await collection.aggregate(aggregationStages).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching data from mongo:", err);
        res.status(500).send("Internal server error");
    }
});

module.exports = router;