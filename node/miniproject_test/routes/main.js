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


//request 1, query 0
app.get('/aa', (req, res) => {
    const result = connection.query('select * from schedule');
    console.log(result);
    res.send(result);
})

//request1, query 0
app.post('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
})

//request1, query 1

app.get('/selectQuery', (req, res) => {
    const home = req.query.home;
    const result = connection.query("select * from schedule where home=?", [home]);
    console.log(result);
    res.send(result);
})






app.post('/selectQuery', (req, res) => {
    const userid = req.body.userid;
    const result = connection.query("select * from user where userid=?", [userid]);
    console.log(result);
    res.send(result);
})

app.post("/insert", (req, res) => {
    const { home, Away, schedule_date, schedule_time } = req.body;
    const result = connection.query("insert into schedule values (?, ?, ?, ?)", [home, Away, schedule_date, schedule_time]);
    res.redirect("/selectQuery?home=" + req.body.home);
})


app.post('/update', (req, res) => {
    const { home, Away, schedule_date, schedule_time } = req.body;
    const result = connection.query("update schedule set Away=?, schedule_date=?, schedule_time=?  where home=?", [Away, schedule_date, schedule_time, home]);
    console.log(result);
    res.redirect('/selectQuery?home=' + req.body.home);
})

app.post('/delete', (req, res) => {
    const home = req.body.home;
    const result = connection.query("delete from schedule where home=?", [home]);
    console.log(result);
    res.redirect('/aa');
})



module.exports = app;
