const express = require("express");
const router = express.Router();
const { getDB } = require("../mongoClient");


router.get("/", async(req, res) => {

    const selectedChamber = req.query.chamber;
    const selectedState = req.query.state;
    const selectedDistrict = req.query.district;

    if (!selectedChamber || !selectedState || !selectedDistrict) {
        return res.status(400).send("Chamber, state, and district selection requried")
    }

    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const query = {
            election_chamber: selectedChamber,
            election_state: selectedState,
            election_constituency: selectedDistrict
        }
        const candidates = await collection.aggregate([
            { $match: query },
            { $group: {
                _id: {
                    firstName: "$candidate_first_name",
                    lastName: "$candidate_last_name",
                    party: "$candidate_party"
                }
            }}
        ]).toArray();
        res.json(candidates.map(candidate => ({
            firstName: candidate._id.firstName,
            lastName: candidate._id.lastName,
            party: candidate._id.party
        })));
        console.log("Candidates: ", candidates)
    } catch (err) {
        console.error("Error fetching candidates: ", err);
        res.status(500).send("Internal server error")
    }

});

module.exports = router;