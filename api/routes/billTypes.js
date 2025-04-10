const express = require("express");
const router = express.Router();
const pool = require("../db");


const TABLE = "Bills";


router.get("/", async (req, res) => {
    const congress = req.query.congress;
    if (!congress) {
        return res.status(400).json({ error: "Missing congress param" });
    }
    try {
        const [rows] = await pool.query(
            `SELECT DISTINCT type FROM ${TABLE} WHERE congress = ?`,
            [congress]
        );
        res.json(rows);
    } catch (err) {
        console.error("DB error:", err);
        res.status(500).json({ error: "DB error" });
    }
});


module.exports = router;
