const express = require('express');
const morgan = require('morgan');
const path = require('path');
const fs = require("fs")
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');

const app = express();

app.set('port', process.env.PORT || 8000);
app.set('views', path.join(__dirname, 'public'));
app.set('view engine','ejs');
app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var main = require('./routes/main.js');
app.use('/', main);

app.listen(app.get('port'), () => {
    var dir = './uploadedFiles';
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
    console.log('8000 Port : Server Started...')
});