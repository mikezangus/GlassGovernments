const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


module.exports = router.get("/", async (req, res) => {
    const { chamber, state, district } = req.query;
    if (!chamber || !state || !district) return res.status(400).send("Chamber, state, and district selection requried");
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const query = {
            election_chamber: chamber,
            election_state: state,
            election_constituency: district
        };
        const group = {
            _id:
            {
                firstName: "$candidate_first_name",
                lastName: "$candidate_last_name",
                party: "$candidate_party"
            },
            totalContributionAmount: { $sum: "$contribution_amount" }
        };
        const candidates = await collection.aggregate([
            { $match: query },
            { $group: group }
        ]).toArray();
        res.json(candidates);
        console.log("Candidates: ", candidates)
    } catch (err) {
        console.error("Error fetching candidates: ", err);
        res.status(500).send("Internal server error")
    }
});