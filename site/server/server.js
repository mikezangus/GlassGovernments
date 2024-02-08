const express = require("express");
const cors = require("cors");
const { connectToMongo } = require("./mongoClient");
const createIndexes = require("./createIndexes");
const fetchYears = require("./fetching/fetchYears");

const yearsRoute = require("./routing/routeYears");
const officesRoute = require("./routing/routeOffices");
const statesRoute = require("./routing/routeStates");
const districtsRoute = require("./routing/routeDistricts");
const candidatesRoute = require("./routing/routeCandidates");
const candidateBioRoute = require("./routing/candidate/bio");
const candidateContributionsTotalRoute = require("./routing/candidate/contributionsTotal");
const candidateContributionsEntitiesRoute = require("./routing/candidate/contributionsEntities");
const candidateCoordinatesRoute = require("./routing/candidate/coordinates");


const app = express();
const PORT = 4000;


function loadRoutes() {
    app.use("/api/years", yearsRoute);
    app.use("/api/offices", officesRoute);
    app.use("/api/states", statesRoute);
    app.use("/api/districts", districtsRoute);
    app.use("/api/candidates", candidatesRoute);
    app.use("/api/candidate/bio", candidateBioRoute);
    app.use("/api/candidate/contributions/total", candidateContributionsTotalRoute);
    app.use("/api/candidate/contributions/entities", candidateContributionsEntitiesRoute);
    app.use("/api/candidate/coordinates", candidateCoordinatesRoute);
};


async function startServer() {
    app.use(cors());
    try {
        await connectToMongo();
        loadRoutes();
        app.listen(PORT, () => {
            console.log(`Server is running on http://localhost:${PORT}`);
        });
        const years = await fetchYears();
        await createIndexes(years);
    } catch (err) {
        console.error("Failed to start server")
    };
};


startServer();
