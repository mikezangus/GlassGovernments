const express = require("express");
const router = express.Router();
const fetchYears = require("../../fetching/selections/fetchYears");


module.exports = router.get("/", async (req, res) => {
    try {
        const years = await fetchYears();
        console.log("Years: ", years);
        res.json(years);
    } catch (err) {
        console.error("Year Route | Error: ", err);
        res.status(500).send("Internal server error");
    };
});
