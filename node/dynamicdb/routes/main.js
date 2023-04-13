const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env" });

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/hello', (req, res) => {
    res.send('Welcome back~!.')
})

//request 1, query 0
app.get('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    // res.send(result);
    res.writeHead(200);
    var templete = `
       <!doctype html>
       <html>
       <head>
           <title>Result</title>
           <meta charset="utf-8">
           <link rel="stylesheet" href="select.css">
       </head>
       <body>
       <table border="1" style="margin:auto; text-align:center;">
       <thead>
           <tr><th>User ID</th><th>Password</th></tr>
       </thead>
       <tbody>
       `;
    for (var i = 0; i < result.length; i++) {
        templete += `
       <tr>
           <td>${result[i]['userid']}</td>
           <td>${result[i]['passwd']}</td>
       </tr>
       `;
    }
    templete += `
       </tbody>
       </table>
       </body>
       </html>
   `;
    res.end(templete);
})

//request1, query 0
app.post('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
})

//request1, query 1
app.get('/selectQuery', (req, res) => {
    const userid = req.query.userid;
    const result = connection.query('SELECT * FROM user where userid=?', [userid]);
    console.log(result);
    //res.send(result);
    if (result.length == 0) {
        res.send("데이터가 없습니다.");
    } else {
        res.writeHead(200);
        var templete = `
        <!doctype html>
        <html>
        <head>
            <title>Reult</title>
            <meta charset="utf-8">
            <link rel="stylesheet" href="selectQuery.css">
       </head>
       <body>
       <table border="1" style="margin:auto; text-align:center;">
       <thead>
           <tr><th>User ID</th><th>Password</th></tr>
       </thead>
       <tbody>
       `;
        for (var i = 0; i < result.length; i++) {
            templete += `
       <tr>
           <td>${result[i]['userid']}</td>
           <td>${result[i]['passwd']}</td>
       </tr>
       `;
        }
        templete += `
       </tbody>
       </table>
       </body>
       </html>
   `;
        res.end(templete);
    }
});

app.post('/selectQuery', (req, res) => {
    const userid = req.body.userid;
    const result = connection.query("select * from user where userid=?", [userid]);
    console.log(result);
    res.send(result);
})

app.post('/insert', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("insert into user values (?, ?)", [id, pw]);
    console.log(result);
    res.send(result);
})

app.post('/insert', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("insert into user values (?, ?)", [id, pw]);
    console.log(result);
    res.send(result);
    res.redirect('/selectQuery?userid=' + req.body.id);
})

app.post('/update', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("update user set passwd=? where userid=?", [pw, id]);
    console.log(result);
    res.send(result);
    res.redirect('/selectQuery?userid=' + req.body.id);
})

app.post('/delete', (req, res) => {
    const id = req.body.id;
    const result = connection.query("delete from user where userid=?", [id]);
    console.log(result);
    res.redirect('/select');
})



module.exports = app;
