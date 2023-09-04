const mongoose = require('mongoose');
mongoose.connect("mongodb+srv://zangus:vmtCdi3DsLV1fk9X@cluster0.vbtb9b1.mongodb.net/?retryWrites=true&w=majority", {useNewUrlParser: true, useUnifiedTopology: true});

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