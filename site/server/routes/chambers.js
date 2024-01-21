const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


module.exports = router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const chambers = await collection.distinct("election_chamber");
        res.json(chambers);
        console.log("Chambers: ", chambers)
    } catch (err) {
        console.error("Error fetching chamber data from mongo: ", err);
        res.status(500).send("Internal server error");
    };
});