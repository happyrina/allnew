var axios = require('axios');
var data = JSON.stringify({
    "collection": "testdb",
    "database": "test",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 0,
        "id": 1,
        "name": 1
    }
});

var config = {
    method: 'post',
    url: 'https://us-west-2.aws.data.mongodb-api.com/app/data-eqglt/endpoint/data/v1/action/findOne',
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': xxxx
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
