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

function templete_nodata(res) {
    res.writeHead(200);
    var templete = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
            <link type="text/css" rel="stylesheet" href=mystyle.css" />
        </head>
        <body>
            <h3>데이터가 존재하지 않습니다</h3>
        </body>
        </html>
    `;
    res.end(templete);
}

function templete_result(dataUser, res) {
    res.writeHead(200);
    var templete = `
        <!doctype html>
        <html>
        <head>
            <title>Result</title>
            <meta charset="utf-8">
            <link type="text/css" rel="stylesheet" href="mystyle.css"/>
        </head>
        <body>
        <table border="1" style="margin;auto;">
       <thead>
        <tr><th>nickName</th><th>userID</th><th>userPW</th><th>phone</th></tr>
    </thead>
    <tbody>
    `;
    for (var i = 0; i < restbl.length; i++) {
        templete += `
    <tr>
        <td>${dataUser[i]['nickName']}</td>
        <td>${dataUser[i]['userID']}</td>
        <td>${restbl[i]['shopId']}</td>
        <td>${dataUser[i]['userPW']}</td>
        <td>${dataUser[i]['phone']}</td>
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




//login page - user, admin / id와 pw가 맞지 않으면 "id와 pw를 확인해 주세요!"라는 문구 띄우기
app.post('/login', (req, res) => {
    const { userID, userPW } = req.body;
    const query = connection.query("SELECT * FROM dataUser WHERE userID=? AND userPW=?", [userID, userPW]);
    if (query.length == 0) {
        // console.log(query)
        // res.send({ 'ok': false, 'queryt': query.affectedRows, 'text': '입력을 확인하세요' })
        //res.redirect로 해야 웹 서버에 보여줌
        // res.redirect('/');
        res.send("<script>alert('공백을 확인해주세요'); window.location.replace('/index.html');</script>")

    }
    else if (userID == "admin") {
        // res.send({ 'ok': true, 'query': query.affectedRows, 'text': '관리자가 로그인 했습니다!' })
        // console.log(userID + " => 관리자가 로그인했습니다");
        res.send("<script>alert('관리자가 로그인했습니다:)'); window.location.replace('/admin.html');</script>")
        // res.redirect('admin.html');
    } else {
        // res.send({ 'ok': true, 'query': query.affectedRows, 'text': `사용자 ${userID} 가 로그인 했습니다.` })
        res.redirect('main-login.html');
    };
});



//register page 
app.post("/register", (req, res) => {
    const { nickName, userID, userPW, phone } = req.body;
    if (nickName == "" || userID == "" || userPW == "" || phone == "") {
        // res.send({ 'ok': true, 'text': '입력내용을 확인해 주세요' })
        // res.redirect('/login?error=true');
        // res.send("<script>alert('입력내용을 확인해 주세요!'); window.location.replace('/register.html');</script>")
        res.send("<script>alert('입력내용을 확인해 주세요!'); window.location.replace('/register.html');</script>");
    } else {
        let result1 = connection.query("select * from dataUser where nickName=?", [nickName]);
        let result2 = connection.query("select * from dataUser where userID=?", [userID]);
        if (result1.length > 0) {
            // res.send({ 'ok': true, 'result1': result1.affectedRows, 'text': '이미 존재하는 닉네임입니다' })
            res.send("<script>alert('이미 존재하는 닉네임입니다'); window.location.replace('/register.html');</script>")
        } else if (result2.length > 0) {
            // res.send({ 'ok': true, 'result2': result2.affectedRows, 'text': '이미 존재하는 아이디입니다.' })
            res.send("<script>alert('이미 존재하는 아이디입니다.'); window.location.replace('/register.html');</script>")

        } else {
            let result = connection.query("insert into dataUser values (?,?,? ,?)", [nickName, userID, userPW, phone]);
            // console.log(result);
            // res.send({ "ok": true, "result": result.affectedRows, 'text': "회원가입이 완료되었습니다." })
            res.send("<script>alert('회원가입이 완료되었습니다! 다시 로그인을 해주세요!'); window.location.replace('/index.html');</script>")
        }
    }
});



//admin page
//user select
//user select
app.get("/user/select", (req, res) => {
    const result = connection.query('select * from dataUser');
    console.log(result);
    res.send({ "ok": true, "result": result });
});

//user selectQuery
// app.get("/user/selectQuery", (req, res) => {
//     const userID = req.body.userID;
//     console.log(req.body);
//     const result = connection.query("select * from dataUser where userID=?", [userID]);
//     console.log(result);
//     res.send({ "ok": true, "result": result });
// });

app.get('/user/selectQuery', (req, res) => {
    const userID = req.query.userID;
    const result = connection.query("SELECT * FROM dataUser where userID=?", [userID]);
    if (userID == "") {
        // res.send('원하는 동을 입력하세요.')
        res.write("<script>alert('ID를 입력하세요')</script>");
    } else {
        if (result.length == 0) {
            res.write("<script>alert('존재하지 않는 사용자입니다.')</script>")
        } else {
            res.writeHead(200);
            var template = `
       <!doctype html>
       <html>
       <head>
           <title>Result</title>
           <meta charset="utf-8">
       </head>
       <body>
       <table border="1" style="margin:auto; text-align:center;">
       <thead>
           <tr><th>nickName</th><th>User ID</th><th>Password</th><th>phone</th></tr>
       </thead>
       <tbody>
       `;
            for (var i = 0; i < result.length; i++) {
                template += `
       <tr>
       <td>${result[i]['nickName']}</td>
           <td>${result[i]['userID']}</td>
           <td>${result[i]['userPW']}</td>
           <td>${result[i]['phone']}</td>
       </tr>
       `;
            }
            template += `
       </tbody>
       </table>
       </body>
       </html>
   `;
        }
        res.end(template);
    }
})


//user insert
// app.post("/user/insert", (req, res) => {
//     const { nickName, userID, userPW, phone } = req.body;
//     let result = "";
//     if (nickName == "" || userID == "" || userPW == "" || phone == "") {
//         res.send({ "ok": true, "result": result.affectedRows, 'text': "공백을 채워주세요!" });

//     } else {
//         result = connection.query("select * from dataUser where nickName=? OR userID=?", [nickName, userID]);
//         if (result.length > 0) {
//             res.send({ "ok": true, "result": result.affectedRows, 'text': "이미 존재하는 닉네임과 id 입니다." });
//         } else {
//             result = connection.query("insert into dataUser values (?, ?, ?, ?)", [nickName, userID, userPW, phone]);
//             console.log(result);
//             res.send({ "ok": true, "result": result.affectedRows, "text": "새로운 사용자가 추가되었습니다." });
//             //({ ok : true 하고 result를 넣으면 알 수 있음})
//         }
//     }
// })

// app.post("/user/insert", async (req, res) => {
//     const { nickName, userID, userPW, phone } = req.body;
//     let result = "";
//     if (nickName == "" || userID == "" || userPW == "" || phone == "") {
//         res.send({ "ok": true, "result": result.affectedRows, 'text': "공백을 채워주세요!" });

//     } else {
//         result = await new Promise((resolve, reject) => {
//             connection.query("select * from dataUser where userID=?", [userID], (err, rows) => {
//                 if (err) reject(err);
//                 else resolve(rows);
//             });
//         });
//         if (result.length > 0) {
//             res.send({ "ok": true, "result": result.affectedRows, 'text': "이미 존재하는 닉네임과 id 입니다." });
//         } else {
//             result = await new Promise((resolve, reject) => {
//                 connection.query("insert into dataUser values (?, ?, ?, ?)", [nickName, userID, userPW, phone], (err, rows) => {
//                     if (err) reject(err);
//                     else resolve(rows);
//                 });
//             });
//             console.log(result);
//             res.send({ "ok": true, "result": result.affectedRows, "text": "새로운 사용자가 추가되었습니다." });

//         }
//     }
// })



//user update
app.post("/user/update", (req, res) => {
    let result = ""
    const { nickName, userID, userPW, phone } = req.body;
    if (userID == "" || userPW == "" || nickName == "" || phone == "") {
        res.send({ "ok": true, "result": result.affectedRows, 'text': "공백을 채워주세요!" });
    } else {
        result = connection.query("select * from dataUser where userID=?", [userID]);
        if (result.length == 0) {
            res.send({ "ok": true, "result": result.affectedRows, 'text': "존재하지 않는 유저입니다." });

        } else {
            let result1 = connection.query("update dataUser set nickName=?, userPW=?, phone=? where userID=?", [nickName, userPW, phone, userID]);
            console.log(result1);
            res.send({ "ok": true, "result1": result1.affectedRows, "text": "업데이트가 완료되었습니다!!" })
        }
    }
})

//user delete
app.post("/user/delete", (req, res) => {
    const userID = req.body.userID;
    if (userID == "") {
        res.send({ "ok": true, "userID": userID.affectedRows, 'text': 'ID를 입력하세요' });

    } else {
        const result = connection.query("select * from dataUser where userID=?", [userID]);
        console.log(result);

        if (result.length == 0) {
            res.send({ "ok": true, "userID": userID.affectedRows, 'text': "ID가 존재하지 않습니다." });
        } else {
            const result5 = connection.query("delete from dataUser where userID=?", [userID]);
            console.log(result);
            res.send({ "ok": true, "result5": result5.affectedRows, "text": "사용자 삭제가 완료되었습니다!!" });
        }

    }
})

//감채
//select from userID
app.get('/select/userID', (req, res) => {
    const userID = req.query.userID;
    const result = connection.query('select * from dataUser where userID=?', [userID]);
    console.log(result);
    res.send({ "ok": true, "result": result });
})


module.exports = app;