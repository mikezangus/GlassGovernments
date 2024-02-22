const express = require("express");
const cors = require("cors");
const { connectToMongo } = require("../src/lib/mongoClient");
const createIndexes = require("./createIndexes");
const fetchYears = require("./fetching/selections/fetchYears");

const yearsRoute = require("./routing/selections/routeYears");
const officesRoute = require("./routing/selections/routeOffices");
const statesRoute = require("./routing/selections/routeStates");
const districtsRoute = require("./routing/selections/routeDistricts");
const candidatesRoute = require("./routing/selections/routeCandidates");
const contributionsEntitiesRoute = require("./routing/candidate/routeContributionsEntities");
const coordsRoute = require("./routing/candidate/routeCoords");


const app = express();
const PORT = 4000;


function loadRoutes() {
    app.use("/api/years", yearsRoute);
    app.use("/api/offices", officesRoute);
    app.use("/api/states", statesRoute);
    app.use("/api/districts", districtsRoute);
    app.use("/api/candidates", candidatesRoute);
    app.use("/api/candidate/contributions/entities", contributionsEntitiesRoute);
    app.use("/api/candidate/coords", coordsRoute);
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
        console.error("Failed to start server");
    };
};


startServer();
