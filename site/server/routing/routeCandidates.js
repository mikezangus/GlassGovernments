const express = require("express");
const router = express.Router();
const fetchCandidates = require("../fetching/fetchCandidates");


module.exports = router.get("/", async (req, res) => {
    const name = "Candidates Route";
    try {
        const { year, office, state, district } = req.query;
        if (!year || !office || !state || !district) {
            return res
                .status(400)
                .send(name, " | Prior selections required");
        }
        const candidates = await fetchCandidates({ year, office, state, district });
        console.log("Candidates: ", candidates);
        res.json(candidates);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error")
    };
});
