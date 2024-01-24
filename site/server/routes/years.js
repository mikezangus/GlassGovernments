const express = require("express");
const router = express.Router();
const { getDB } = require("./../mongoClient");


module.exports = router.get("/", async (req, res) => {
    try {
        const db = getDB();
        let uniqueYears = new Set();
        const collectionNames = await db.listCollections().toArray();
        const group = { _id: "$election_year"};
        for (let collection of collectionNames) {
            let years = await db.collection(collection.name).aggregate([
                { $group: group }
            ]).toArray();
            years.forEach(yearDoc => uniqueYears.add(yearDoc._id));
        }
        const data = Array.from(uniqueYears);
        res.json(data);
        console.log("Years: ", data);
    } catch (err) {
        console.error("Error fetching year data from mongo: ", err);
        res.status(500).send("Internal server error");
    };
});