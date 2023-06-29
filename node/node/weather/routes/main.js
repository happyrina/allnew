const express = require("express")
const app = express.Router()
const mongoose = require("mongoose")
const request = require('request')
const moment = require("moment")
const dateutil = require("data-utils")
const mongoClient = require('mongodb').MongoClient

let day = new Date().toLocaleDateString('sv').replaceAll('-','');

var keys = "daWuY85swWW6dXGiwv5KvI2e%2BwQSMSA7X%2BAzzK4j7BeGNMiWTSVGqJuv5Qp5PdI6vSSB8Vm6Qp8dHLgsRQaOWw%3D%3D";
var url = "https://apis.data.go.kr/1360000/WthrChartInfoService/getSurfaceChart";

var queryParams ='?' + encodeURIComponent('serviceKey') + "=" + keys;
queryParams +='&' + encodeURIComponent('pageNo') + "=" + encodeURIComponent('1');
queryParams +='&' + encodeURIComponent('numOfRows') + "=" + encodeURIComponent('10');
queryParams +='&' + encodeURIComponent('dataType') + "=" + encodeURIComponent('JSON');
queryParams +='&' + encodeURIComponent('code') + "=" + encodeURIComponent('3');
queryParams +='&' + encodeURIComponent('time') + "=" + encodeURIComponent(day);

// define schema
var DataSchema = mongoose.Schema({
    day_v : String,
    imgSrc1_v : String,
    imgSrc2_v : String
})

var Data = mongoose.model('weathers', DataSchema);

// getdata
app.get('/getdata', function (req, res, next) {
    request({
        url : url + queryParams,
        method : "GET"
    }, function (error, response, body) {
        Data.find({}).remove().exec();
        if (error) console.log(error);
        let data = JSON.parse(body);
        let imgSrcArr = data['response']['body']['items']['item'][0]['man-file'].split(',');
        let imgSrc1 = imgSrcArr[0].slice(1);
        let imgSrc2 = imgSrcArr[1].slice(1);
        console.log("imgSrc1 : " + imgSrc1);
        console.log("imgSrc2 : " + imgSrc2);
        
        res.writeHead(200);
        var template = `
        <!doctype html>
        <html>
        <head>
        <title>Result</title>
        <meta charset='utf-8'>
        </head>
        <body>
        <img src="${imgSrc1}" width="500" height="500"></img><p>
        <img src="${imgSrc2}" width="500" height="500"></img><p>
        </body>
        </html>
        `;
        res.end(template);
        
        var newData = new Data({day_v : day, imgSrc1_v : imgSrc1, imgSrc2_v : imgSrc2})
        newData.save(function(err, result) {
            if (err) return console.error(err)
            console.log(new Date(), result)
        })
    })
})

// list
app.get('/list', function(req, res, next) {
    Data.findOne({}, function(err, docs) {
        if (err) console.log('err');
        console.log(docs);
        res.writeHead(200);
        var template = `
        <!doctype html>
        <html>
        <head>
        <title>Result</title>
        <meta charset='utf-8'>
        </head>
        <body>
        <img src="${docs['imgSrc1_v']}" width="500" height="500"></img><p>
        <img src="${docs['imgSrc2_v']}" width="500" height="500"></img><p>
        </body>
        </html>
        `;
        res.end(template);
    })
})
module.exports = app;