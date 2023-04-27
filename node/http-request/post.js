const https = require('https');

const data = JSON.stringify({
    todo: 'Buy the milk'
})

const options = {
    hostname: '192.168.1.187',
    port: 8000,
    path: '/todos',
    method: 'POST',
    header: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
}

const req = https.request(options, res => {
    console.log(`statusCode : ${res.statusCode}`);
    res.on('data', d => {
        process.stdout.write(d);
    })
})

req.on('error', error => {
    console.log(error)
})

req.write(data)
req.end()