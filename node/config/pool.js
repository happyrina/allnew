const mysql = require('mysql2')

const pool = mysql.createPool({
    //mysql connection info
    host: "192.168.1.183",
    port: 3306,
    user: "mysql",
    password: "1234",
    database: "testdb"
})

const promisePool = pool.promise()

module.exports = promisePool;