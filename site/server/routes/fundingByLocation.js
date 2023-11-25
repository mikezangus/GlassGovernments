const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");
const { groupCoordinates } = require("../utilities/locationUtils");

router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        console.log("Request query:", req.query);
        const aggregation = await collection.aggregate([
            {
                $match: {
                    candidate_state: state,
                    candidate_district: district,
                    candidate_first_name: firstName,
                    candidate_last_name: lastName,
                    "contributor_location.coordinates": { $exists: true, $ne: null }
                }
            },
            {
                $project: {
                    _id: 0,
                    longitude: { $arrayElemAt: ["$contributor_location.coordinates", 0] },
                    latitude: { $arrayElemAt: ["$contributor_location.coordinates", 1] }
                }
            }
        ]).toArray();
        console.log("Aggregation result:", aggregation);
        const groupedHotspots = groupCoordinates(aggregation);
        res.json(groupedHotspots);
    } catch (err) {
        console.error("Error fetching donation hotspots from MongoDB:", err);
        res.status(500).send("Internal server error");
    }
});

module.exports = router;