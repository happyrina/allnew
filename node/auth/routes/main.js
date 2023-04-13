// const express = require('express');
// const bodyParser = require('body-parser');
// const mysql = require('sync-mysql');
// const env = require('dotenv').config({ path: "../../.env" });

// var connection = new mysql({
//     host: process.env.host,
//     user: process.env.user,
//     password: process.env.password,
//     database: process.env.database
// });

// const app = express()

// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: false }));
// app.use(express.json());
// app.use(express.urlencoded({ extended: true }));

// app.post('/login', (req, res) => {
//     const { id, pw } = req.body;
//     const result = connection.query("insert into userform values (?, ?)", [userid, passwd]);
//     console.log(result);
//     result[0].id;
//     result[0].passwd;
//     res.send(result);
// })

// //login
// app.post('/login', (req, res) => {
//     const { id, pw } = req.body;
//     const result = connection.query("select * from user where userid=?
//     and passwd =? ", [id, pw]);
//     if (result.length == 0) {
//         res.redirect('error.html')
//     }
//     if (id == 'admin' || id == 'root') {
//         console.log(id + " => Administrator Logined")
//         res.redirect('member.html')
//     }
// })

// // register
// app.post('/insert', (req, res) => {
//     const { id, pw } = req.body;
//     const result = connection.query("insert into user values (?, ?)", [id, pw]);
//     console.log(result);
//     res.redirect('/selectQuery?id=' + req.body.id);
// })









// app.post('/insert', (req, res) => {
//     const { id, pw } = req.body;
//     const result = connection.query("update user set passwd=? where userid=?", [pw, id]);
//     console.log(result);
//     res.send(result);
//     res.redirect('/selectQuery?id=' + req.body.id);
// })

// app.post('/register', (req, res) => {
//     const { userid, passwd } = req.body;
//     const result = connection.query("update userform set register=? where userid=?", [userid]);
//     res.redirect('/selectQuery?userform=' + req.body.home);
//     if (result.length == 0) {
//         res.redirect('error.html')
//     }
// })

// app.post('/delete', (req, res) => {
//     const id = req.body.id;
//     const result = connection.query("delete from user where userid=?", [id]);
//     console.log(result);
//     res.redirect('/select');
// })

// module.exports = app;

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
    res.send('Welcome back~!!')
})

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

// login
app.post('/login', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("select * from user where userid=? and passwd=?", [id, pw]);
    if (result.length == 0) {
        res.redirect('error.html')
    }
    if (id == 'admin' || id == 'root') {
        console.log(id + " => Administrator Logined")
        res.redirect('member.html')
    } else {
        console.log(id + " => User Logined")
        res.redirect('main.html')

    }
})

// register
app.post('/register', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("insert into user values (?, ?)", [id, pw]);
    console.log(result);
    res.redirect('/');
})

// request O, query X
app.get('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
})

// request O, query X
app.post('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
})

// request O, query O
// app.get('/selectQuery', (req, res) => {
//     const id = req.query.id;
//     const result = connection.query("select * from user where userid=?", [id]);
//     console.log(result);
//     res.send(result);
// })
app.get('/selectQuery', (req, res) => {
    const id = req.query.id;
    const result = connection.query('SELECT * FROM user where userid=?', [id]);
    console.log(result);
    //res.send(result);
    if (result.length == 0) {
        res.send("<p style='background-color: white; background-opacity: 70%; color: red; font-size: 30px; font-weight: 20px; text-align: center;'>데이터가 없습니다.</p>");


    } else {

        res.writeHead(200);
        var templete = `
        <!doctype html>
        <html>
        <
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

// request O, query O
app.post('/selectQuery', (req, res) => {
    const id = req.body.id;
    // console.log(req.body);
    const result = connection.query("select * from user where userid=?", [id]);
    console.log(result);
    res.send(result);
})

// request O, query O
// app.post('/insert', (req, res) => {
//     const { id, pw } = req.body;
//     const result = connection.query("insert into user values (?, ?)", [id, pw]);
//     console.log(result);
//     if (result.length == 0) {
//         res.send("데이터를 넣어주세요!");


//     } else {
//         res.redirect('/selectQuery?id=' + req.body.id);
//     }
// })

app.post('/insert', (req, res) => {
    const { id, pw } = req.body;
    if (id == 0 || pw == 0) { //!pw pw가 있으면, 
        res.send("<p style='background-color: white; color: red; font-size:20px; text-align: center;';>🤬id와 pw를 넣어주세요!!!!!!🤬</p>");
    } else {
        const result = connection.query("insert into user values (?, ?)", [id, pw]);
        console.log(result);
        res.redirect('/selectQuery?id=' + req.body.id);
    }
});

// request O, query O
app.post('/update', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("update user set passwd=? where userid=?", [pw, id]);
    console.log(result);
    res.redirect('/selectQuery?id=' + req.body.id);
})

// request O, query O
app.post('/delete', (req, res) => {
    const id = req.body.id;
    const result = connection.query("delete from user where userid=?", [id]);
    console.log(result);

    if (id == 0 || pw == 0) { //!pw pw가 있으면, 
        res.send("제발 데이터를 넣어주세요!!!!!!!!!!");
    } else {
        const result = connection.query("insert into user values (?, ?)", [id, pw]);
        console.log(result);
        res.redirect('/select');
    }
})



module.exports = app;

