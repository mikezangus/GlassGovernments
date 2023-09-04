const mongoose = require('mongoose');
const { mongoUsername, mongoPassword, mongoServerName} = require ("./credentials");
mongoose.connect(`mongodb+srv://${mongoUsername}:${mongoPassword}@${mongoServerName}.vbtb9b1.mongodb.net/?retryWrites=true&w=majority`, {useNewUrlParser: true, useUnifiedTopology: true});

const Politician = mongoose.model('Politician', new mongoose.Schema({
  id: Number,
  name: String,
  csvFile: String,
  incumbency: String,
  party: String,
  constituency: String,
  photoUrl: String,
}));

module.exports = Politician;