const express = require("express");
const { run } = require ("./mongo");
const path = require("path")
const app = express();

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.use(express.static(__dirname));

async function startServer() {
  try {
    await run();
    const port = process.env.PORT || 3000;
    app.listen(port, () => {
      console.log(`Server is running on port http://localhost:${port}`)
    });
  } catch (error) {
    console.error("Error connecting to MongoDB:", error)
  }
}

startServer();
