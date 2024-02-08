const express = require("express");
const router = express.Router();
const fetchDistricts = require("../../fetching/selections/fetchDistricts");


module.exports = router.get("/", async (req, res) => {
    const name = "Districts Route";
    try {
        const { year, office, state } = req.query;
        if (!year || !office || !state) {
            return res
                .status(400)
                .send(name, " | Prior selections required");
        }
        const districts = await fetchDistricts({ year, office, state});
        console.log("Districts: ", districts);
        res.json(districts);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error");
    };
});
