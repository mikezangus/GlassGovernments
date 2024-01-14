const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async(req, res) => {

    const selectedChamber = req.query.chamber;
    const selectedState = req.query.state;

    if (!selectedChamber  || !selectedState) {
        return res.status(400).send("Chamber and state selection is required");
    }

    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const districts = await collection.distinct(
            "election_constituency", {
                election_chamber: selectedChamber,
                election_state: selectedState
            }
        );
        res.json(districts);
        console.log("Districts: ", districts)
    } catch (err) {
        console.error("Error fetching districts: ", err);
        res.status(500).send("Internal server error");
    }

});

module.exports = router;