const express = require("express");
const router = express.Router();
const fetchStates = require("../fetching/fetchStates");


module.exports = router.get("/", async(req, res) => {
    const name = "States Route";
    try {
        const { year, office } = req.query;
        if (!year || !office) {
            return res
                .status(400)
                .send(name, "| Prior selections required");
        }
        const states = await fetchStates({ year, office });
        console.log("States: ", states);
        res.json(states);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error");
    };
});
