const express = require('express');
const app = express();
const port = 3000;

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

app.get('/politicians', async (req, res) => {
  const politicians = await Politician.find();
  res.json(politicians);
});