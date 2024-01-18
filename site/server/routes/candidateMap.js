const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async (req, res) => {

    const { chamber, state, district, firstName, lastName, party } = req.query;

    if (!chamber || !state || !district || !firstName || !lastName || !party) {
        return res.status(400).send("Chamber, state, district, and candidate selections required")
    };

    try {

        const db = getDB();
        const collection = db.collection("2022x");

        const query = {
            election_chamber: chamber,
            election_state: state,
            election_constituency: district,
            candidate_first_name: firstName,
            candidate_last_name: lastName,
            candidate_party: party,
            "contribution_location.coordinates": { $exists: true, $ne: null }
        };

        const projection = {
            _id: 0,
            lat: "$contribution_location.coordinates.1",
            lng: "$contribution_location.coordinates.0",
            amount: "$contribution_amount"
        };

        const candidateMapData = await collection.find(query).project(projection).toArray();

        const filteredMapData = candidateMapData.filter(item => item.lat != null && item.lng != null);

        res.json(filteredMapData);

        console.log("Candidate map data: ", filteredMapData);

    } catch (err) {
        console.error("Error fetching candidate info: ", err);
        res.status(500).send("Internal server error")
    };

});

module.exports = router;