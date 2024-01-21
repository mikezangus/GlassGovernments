const express = require("express");
const cors = require("cors");
const { connectToMongo } = require("./mongoClient");

const chambersRoute = require("./routes/chambers");
const statesRoute = require("./routes/states");
const districtsRoute = require("./routes/districts");
const candidatesRoute = require("./routes/candidates");
const candidateInfoRoute = require("./routes/candidateInfo");
const candidateEntitiesRoute = require("./routes/candidateEntities");
const candidateCoordinatesRoute = require("./routes/candidateCoordinates");

const app = express();
const PORT = 4000;

app.use(cors());
connectToMongo();

app.use("/api/chambers", chambersRoute);
app.use("/api/states", statesRoute);
app.use("/api/districts", districtsRoute);
app.use("/api/candidates", candidatesRoute);
app.use("/api/candidate/info", candidateInfoRoute);
app.use("/api/candidate/entities", candidateEntitiesRoute);
app.use("/api/candidate/coordinates", candidateCoordinatesRoute);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});