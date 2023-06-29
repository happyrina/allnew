const express    = require('express');
const app        = express.Router();
const multer = require("multer")
const fs = require('fs')

var storage = multer.diskStorage({
  destination(req, file, cb) {
    cb(null, 'uploadedFiles/');
  },
  filename(req, file, cb) {
    cb(null, `${Date.now()}__${file.originalname}`);
  },
});

var upload = multer({ dest : 'uploadedFiles/' });
var uploadWithOriginalFilename = multer({ storage : storage });
const fullPath = process.cwd() + '/uploadedFiles' //(not __dirname)

app.get('/', function(req, res) {
  res.render('upload');
});

app.post('/uploadFile', upload.single('attachment'), function (req, res) {
  res.render('confirmation', { file:req.file, files:null });
});

app.post('/uploadFileWithOriginalFilename', uploadWithOriginalFilename.single('attachment'), function (req, res) {
  res.render('confirmation', { file:req.file, files:null });
});

app.post('/uploadFiles', upload.array('attachments'), function (req, res) {
  res.render('confirmation', { file:null, files:req.files });
});

app.post('/uploadFilesWithOriginalFilename', uploadWithOriginalFilename.array('attachments'), function (req, res) {
  res.render('confirmation', { file:null, files:req.files });
});

app.get('/list', (req, res) => {
    const dir = fs.opendirSync(fullPath)
    let entity
    let listing = []
    while((entity = dir.readSync()) !== null) {
        if(entity.isFile()) {
            listing.push({ type: 'f', name: entity.name })
        } else if(entity.isDirectory()) {
            listing.push({ type: 'd', name: entity.name })
        }
    }
    dir.closeSync()
    // res.send(listing)
      res.writeHead(200);
      var template = `
        <!doctype html>
        <table border="1" margin: auto; text-align: center;>
          <tr>
            <th> Type </th>
            <th> Name </th>
            <th> Down </th>
            <th> Del </th>
          </tr>
      `;
      for(var i=1;i<listing.length;i++) {
        template += `
          <tr>
            <th>${listing[i]['type']}</th>
            <th>${listing[i]['name']}</th>
            <th>
            <form method='post' action='/downloadFile'>
            <button type="submit" name='dlKey' value=${listing[i]['name']}>down</button>
            </form>
            </th>
            <th>
            <form method='post' action='/deleteFile'>
            <button type="submit" name='dlKey' value=${listing[i]['name']}>del</button>
            </form>
            </th>
          </tr>
          `;
        }
        template +=`
        </table>
    `;
    res.end(template);
})

app.post('/downloadFile', function(req,res) {
  var filename = req.body.dlKey;
  console.log(filename);
  const directoryPath = fullPath + '/';

  res.download(directoryPath + filename, filename, (err) => {
    if (err) {
      res.status(500).send({
        message: "Could not download the file. " + err,
      });
    }
  });
})

app.post('/deleteFile', function(req,res) {
  var filename = req.body.dlKey;
  console.log(filename);
  const directoryPath = fullPath + '/';

  fs.unlink(directoryPath + filename, (err) => {
    if (err) {
      res.status(500).send({
        message: "Could not delete the file. " + err,
      });
    }
    // res.status(200).send({
    //   message: "File is deleted.",
    // });
    res.redirect('/list');
  });
  setTimeout(function(){}, 1000);
})

module.exports = app;