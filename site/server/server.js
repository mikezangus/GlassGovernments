const express = require("express");
const cors = require("cors");
const { connectToMongo } = require("./mongoClient");

const chambersRoute = require("./routes/chambers");
const statesRoute = require("./routes/states");
const districtsRoute = require("./routes/districts");
const candidatesRoute = require("./routes/candidates");
const candidateBioRoute = require("./routes/candidate/bio");
const candidateContributionsTotalRoute = require("./routes/candidate/contributionsTotal");
const candidateContributionsEntitiesRoute = require("./routes/candidate/contributionsEntities");
const candidateCoordinatesRoute = require("./routes/candidate/coordinates");

const app = express();
const PORT = 4000;

app.use(cors());
connectToMongo();

app.use("/api/chambers", chambersRoute);
app.use("/api/states", statesRoute);
app.use("/api/districts", districtsRoute);
app.use("/api/candidates", candidatesRoute);
app.use("/api/candidate/bio", candidateBioRoute);
app.use("/api/candidate/contributions/total", candidateContributionsTotalRoute);
app.use("/api/candidate/contributions/entities", candidateContributionsEntitiesRoute);
app.use("/api/candidate/coordinates", candidateCoordinatesRoute);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});