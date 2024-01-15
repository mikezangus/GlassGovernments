const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async(req, res) => {

    const { chamber } = req.query;
    if (!chamber) return res.status(400).send("Chamber selection is required");
    
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const states = await collection.distinct(
            "election_state",
            { election_chamber: chamber }
        );
        res.json(states);
        console.log("States: ", states);
    } catch (err) {
        console.error("Error fetching states: ", err);
        res.status(500).send("Internal server error");
    };
});

module.exports = router;