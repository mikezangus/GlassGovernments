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

app.get("/api/candidate-funding-by-entity", async (req, res) => {
    try {
        const db = client.db(config.mongoDatabase);
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        
        const aggregation = await collection.aggregate([
            {
                $match: {
                    candidate_state: state,
                    candidate_district: district,
                    candidate_first_name: firstName,
                    candidate_last_name: lastName
                }
            },
            {
                $group: {
                    _id: "$entity_type_desc",
                    totalAmount: { $sum: "$contribution_receipt_amount" }
                }
            },
            { $sort: { totalAmount: -1 } }
        ]).toArray();
        res.json(aggregation);
    } catch (err) {
        console.error("Error fetching funding by entity from MongoDB:", err);
        res.status(500).send("Internal server error");
    }
});

function haversine(lat1, lon1, lat2, lon2) {
    const R = 3958.8;
    const rlat1 = Math.PI * lat1 / 180;
    const rlat2 = Math.PI * lat2 / 180;
    const difflat = rlat2-rlat1;
    const difflon = Math.PI * (lon2 - lon1)/180;

    const d = 2 * R * Math.asin(Math.sqrt(Math.sin(difflat / 2) * Math.sin(difflat / 2) + Math.cos(rlat1) * Math.cos(rlat2) * Math.sin(difflon / 2)));
    return d;
};

function groupCoordinates(coordinates) {
    const groupedCoords = [];
    const threshold = 10;
    coordinates.forEach(coord => {
        let isGrouped = false;
        for (const group of groupedCoords) {
            for (const point of group) {
                if (haversine(coord.latitude, coord.longitude, point.latitude, point.longitude) <= threshold) {
                    group.push(coord);
                    isGrouped = true;
                    break;
                }
            }
            if (isGrouped) break;
        }
        if (!isGrouped) {
            groupedCoords.push([coord]);
        }
    });

    return groupedCoords;
};

app.get("/api/candidate-donation-hotspots", async (req, res) => {
    try {
        const db = client.db(config.mongoDatabase);
        const collection = db.collection("2022_house");
        const { state, district, lastName, firstName } = req.query;
        console.log("Request query:", req.query);
        const aggregation = await collection.aggregate([
            {
                $match: {
                    candidate_state: state,
                    candidate_district: district,
                    candidate_first_name: firstName,
                    candidate_last_name: lastName,
                    "contributor_location.coordinates": { $exists: true, $ne: null }
                }
            },
            {
                $project: {
                    _id: 0,
                    longitude: { $arrayElemAt: ["$contributor_location.coordinates", 0] },
                    latitude: { $arrayElemAt: ["$contributor_location.coordinates", 1] }
                }
            }
        ]).toArray();
        console.log("Aggregation result:", aggregation);
        const groupedHotspots = groupCoordinates(aggregation);
        res.json(groupedHotspots);
    } catch (err) {
        console.error("Error fetching donation hotspots from MongoDB:", err);
        res.status(500).send("Internal server error");
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});