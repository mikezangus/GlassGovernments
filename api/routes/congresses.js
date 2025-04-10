const express = require("express");
const router = express.Router();
const pool = require("../db");


const TABLE = "Bills";


router.get("/", async (req, res) => {
    try {
        const [rows] = await pool.query(`SELECT DISTINCT congress FROM ${TABLE}`);
        res.json(rows);
    } catch (err) {
        console.error("DB error:", err);
        res.status(500).json({ error: "DB error" });
    }
});


module.exports = router;
