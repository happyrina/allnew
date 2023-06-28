const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const CircularJSON = require('circular-json');
const request = require('request');

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

let urls = "";

app.get('/hello', (req, res) => {
    urls = "http://3.34.107.240:8000/hello";
    request(urls, {json:true}, (err, result, body) => {
        if (err) { return console.log(err); }
        res.send(CircularJSON.stringify(body))
    })
});

// request X , response O
app.get("/api/users", (req, res) => {
    axios
        .get('http://3.34.107.240:8000/api/users')
        .then(result => {
            res.send(CircularJSON.stringify(result.data))
        })
        .catch(error => {
            console.error(error)
        })
})

// Query param, request O, response O
app.get("/api/users/user", (req, res) => {
    if (req.query.name == null) {
        urls = "http://3.34.107.240:8000/api/users/user?user_id="+req.query.user_id;
    } else {
        urls = "http://3.34.107.240:8000/api/users/user?user_id="+req.query.user_id+"&name="+req.query.name;
    }
    request(urls, {json:true}, (err, result, body) => {
        if (err) { return console.log(err); }
        res.send(CircularJSON.stringify(body))
    })
})

module.exports = app;
