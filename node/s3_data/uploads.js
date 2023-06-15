const fs = require('fs');
const env = require("dotenv").config({ path: "../../.env"});

const AWS =  require('aws-sdk');
const ID = process.env.ID;
const SECRET = process.env.SECRET;
const BUCKET_NAME = 'lunar-2075';
const MYREGION = 'ap-northeast-2'
const s3 = new AWS.S3({accessKeyId: ID, secretAccessKey: SECRET, region: MYREGION});

const uploadFile = (fileName) => {
  const fileContent = fs.readFileSync(fileName);
  const params = {
    Bucket: BUCKET_NAME,
    Key: 'axios.png',
    Body: fileContent
  };
  s3.upload(params, function(err, data) {
    if (err) {throw err;}
    console.log(`File uploaded succssfully. ${data.Location}`);
  });
};
uploadFile('axios.png');
