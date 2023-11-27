const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");
const { groupCoordinates, sortGroupsBySize } = require("../utilities/locationUtils");

router.get("/", async (req, res) => {
    try {
        const db = getDB();
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        console.log("Request query via route:", req.query);
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
                    coordinates: "$contributor_location.coordinates"
                }
            }
        ]).toArray();
        console.log("Aggregation result via route:", aggregation);
        const hotspots = aggregation.map(item => ({
            longitude: item.coordinates[0],
            latitude: item.coordinates[1]
        }));
        let groupedHotspots = groupCoordinates(hotspots);
        groupedHotspots = sortGroupsBySize(groupedHotspots);
        const topGroupedHotspots = groupedHotspots.slice(0, 5)
        console.log("Top 5 grouped hotspots via route:", topGroupedHotspots)
        res.json(topGroupedHotspots);
    } catch (err) {
        console.error("Error fetching donation hotspots from MongoDB via fundingByLocation.js:", err);
        res.status(500).send("Internal server error via fundingByLocation.js");
    }
});

module.exports = router;