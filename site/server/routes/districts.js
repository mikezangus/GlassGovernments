const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async(req, res) => {

    const { chamber, state } = req.query;
    if (!chamber || !state) return res.status(400).send("Chamber and state selection is required");
    
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const districts = await collection.distinct(
            "election_constituency", {
                election_chamber: chamber,
                election_state: state
            }
        );
        res.json(districts);
        console.log("Districts: ", districts)
    } catch (err) {
        console.error("Error fetching districts: ", err);
        res.status(500).send("Internal server error");
    };
});

module.exports = router;