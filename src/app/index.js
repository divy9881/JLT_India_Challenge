const { app, BrowserWindow } = require('electron')
const fs = require('fs');
const http = require('http');

let win

function createWindow () {
  
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('index.html');

  win.setMenu(null);

  win.webContents.openDevTools()

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

global.store = function(url, file) {
  http.request(url)
    .on('response', function(res) {
      var body = ''
      res.setEncoding('binary')
      res
        .on('error', function(err) {
          callback(err)
        })
        .on('data', function(chunk) {
          body += chunk
        })
        .on('end', function() {
          var path = `${__dirname}/templates/${file}`
          fs.writeFile(path, body, 'binary', function(err) {
            console.log("Done");
          })
        })
    })
    .on('error', function(err) {
      console.log("Error")
    })
    .end();
}