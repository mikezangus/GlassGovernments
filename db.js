const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/my_database', {useNewUrlParser: true, useUnifiedTopology: true});

const Politician = mongoose.model('Politician', new mongoose.Schema({
  id: Number,
  name: String,
  csvFile: String,
  incumbency: String,
  party: String,
  constituency: String,
  photoUrl: String,
}));