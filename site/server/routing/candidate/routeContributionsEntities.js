const express = require("express");
const router = express.Router();
const fetchContributionsEntities = require("../../fetching/candidate/fetchContributionsEntities")


module.exports = router.get("/", async (req, res) => {
    const name = "Contributions Entities route";
    try {
        const { year, candID } = req.query;
        if (!year || !candID) {
            return res
                .status(400)
                .send(name, " | Prior selections required");
        }
        const data = await fetchContributionsEntities({ year, candID });
        console.log("Entities: ", data)
        res.json(data);
    } catch (err) {
        console.error(name, " | Error: ", err);
        res.status(500).send("Internal server error");
    };
});