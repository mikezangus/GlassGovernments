const express = require("express");
const router = express.Router();
const fetchOffices = require("../../fetching/selections/fetchOffices");


module.exports = router.get("/", async (req, res) => {
    const name = "Office Route";
    try {
        const { year } = req.query;
        if (!year) {
            return res
                .status(400)
                .send(name, " | Prior selections required");
        }
        const offices = await fetchOffices({ year });
        console.log("Offices: ", offices);
        res.json(offices);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error");
    };
});
