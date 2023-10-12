var axios = require("axios");

var data = JSON.stringify({
    "collection": "test_collection",
    "database": "test_database",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 1
    }
});
            
var config = {
    method: 'post',
    url: 'https://us-east-1.aws.data.mongodb-api.com/app/data-xzsks/endpoint/data/v1/action/findOne',
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Request-Headers': '*',
      'api-key': '64f6202e8cb0812c62ef3e9a'
    //   'api-key': '1jOqGoILo3z2UV1h4lqjSDm8id9lMVMeYAaYsvPtVYzQbLJwdh7FeM1sAMJuVLTT',
    },
    data: data
};
            
axios(config)
    .then(function (response) {
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        console.log(error);
    });