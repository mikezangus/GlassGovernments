const express = require("express");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { MongoClient } = require("mongodb");

const app = express();
const PORT = 4000;

app.use(cors());

const loadConfig = () => {
    const configPath = path.join(__dirname, "..", "..", "config.json")
    const rawConfig = fs.readFileSync(configPath)
    return JSON.parse(rawConfig)
};
const config = loadConfig();
const uri = `mongodb+srv://${config.mongoUsername}:${config.mongoPassword}@${config.mongoCluster}.px0sapn.mongodb.net/?retryWrites=true&w=majority`;
const client = new MongoClient(uri);

client.connect()
    .then(() => {
        console.log(`Connected to cluster at uri ${uri}`);
    })
    .catch(err => {
        console.error("Failed to connect to cluster", err);
        process.exit(1);
    });

app.get("/api/districts", async (req, res) => {
    try {
        const db = client.db(config.mongoDatabase);
        const collection = db.collection("2022_house");
        const aggregation = await collection.aggregate([
            {
                $group: {
                    _id: {
                        state: "$candidate_state",
                        district: "$candidate_district"
                    }
                }
            }
        ]).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching data from mongo:", err);
        res.status(500).send("Internal server error");
    };
});

app.get("/api/candidates", async (req, res) => {
    try {
        const db = client.db(config.mongoDatabase);
        const collection = db.collection("2022_house");
        const { state, district } = req.query;
        let matchStage = {};
        if (state && district) {
            matchStage = {
                $match: {
                    candidate_state: state,
                    candidate_district: district
                }
            };
        };
        const aggregationStages = [
            matchStage,
            {
                $group: {
                    _id: {
                        firstName: "$candidate_first_name",
                        lastName: "$candidate_last_name",
                        state: "$candidate_state",
                        district: "$candidate_district",
                        party: "$candidate_party"
                    },
                    totalFunding: { $sum: "$contribution_receipt_amount" }
                }
            }
        ].filter(stage => Object.keys(stage).length > 0);
        const aggregation = await collection.aggregate(aggregationStages).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching data from mongo:", err);
        res.status(500).send("Internal server error");
    }
});

app.get("/api/candidate-panel", async (req, res) => {
    try {
        const db = client.db(config.mongoDatabase);
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        let matchStage = {
            $match: {
                candidate_state: state,
                candidate_district: district,
                candidate_first_name: firstName,
                candidate_last_name: lastName
            }
        };
        const aggregationStages = [
            matchStage,
            {
                $group: {
                    _id: "$entity_type_desc",
                    totalAmount: { $sum: "$contribution_receipt_amount" }
                }
            },
            { $sort: { totalAmount: -1 } }
        ];
        const donations = await collection.aggregate(aggregationStages).toArray();
        res.json(donations);
    } catch (err) {
        console.error("Error fetching data from mongo:", err);
        res.status(500).send("Internal server error");
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});