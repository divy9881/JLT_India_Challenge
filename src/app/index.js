const { app, BrowserWindow, Menu } = require('electron')
const fs = require('fs');
const http = require('http');

let win
Menu.setApplicationMenu(false)

function createWindow() {

  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('index.html');

    win.setMenu(null);

    win.webContents.openDevTools();

  win.on('closed', () => {
    win = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (win === null) {
    createWindow()
  }
})

let file = null

global.store = function (url, file) {
  http.request(url)
    .on('response', function (res) {
      var body = ''
      res.setEncoding('binary')
      res
        .on('error', function (err) {
          callback(err)
        })
        .on('data', function (chunk) {
          body += chunk
        })
        .on('end', function () {
          var path = `${__dirname}/templates/${file}`
          fs.writeFile(path, body, 'binary', function (err) {
            //console.log("Downloaded File");
          })
        })
    })
    .on('error', function (err) {
      //console.log("Error")
    })
    .end();
}

global.setFilename = function (filename) {
  file = filename
  //console.log("setFilename", file)
}

global.getFilename = function () {
  //console.log("getFilename", file)
  return file
}