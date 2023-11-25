const express = require("express");
const cors = require("cors");
const { connectToMongo } = require("./mongoClient");
const districtsRoute = require("./routes/districts");
const candidatesRoute = require("./routes/candidates");
const fundingByEntityRoute = require("./routes/fundingByEntity");
const fundingByLocationRoute = require("./routes/fundingByLocation");

const app = express();
const PORT = 4000;

app.use(cors());
connectToMongo();

app.use("/api/districts", districtsRoute);
app.use("/api/candidates", candidatesRoute);
app.use("/api/funding-by-entity", fundingByEntityRoute);
app.use("/api/funding-by-location", fundingByLocationRoute);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});