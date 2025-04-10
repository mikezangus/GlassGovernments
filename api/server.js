const express = require("express");
const app = express();
const port = process.env.SERVER_PORT || 3001;


const congressesRoute = require("./routes/congresses");
const billTypesRoute = require("./routes/billTypes");
const billNumsRoute = require("./routes/billNums");
app.use("/api/congresses", congressesRoute);
app.use("/api/bill-types", billTypesRoute);
app.use("/api/bill-nums", billNumsRoute);


app.get("/", (req, res) => {
    res.send("API is running\n");
});


app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
