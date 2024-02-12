const express = require("express");
const router = express.Router();
const fetchCoords = require("../../fetching/candidate/fetchCoords")


module.exports = router.get("/", async (req, res) => {
    const name = "Coordinates route";
    try {
        const { year, candID } = req.query;
        if (!year || !candID) {
            return res
                .status(400)
                .send(name, " | Prior selections required");
        }
        const data = await fetchCoords({ year, candID });
        console.log("Coordinates: ", data)
        res.json(data);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error");
    };
});