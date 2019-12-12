const { app, BrowserWindow, Menu, net } = require('electron')
// Menu.setApplicationMenu(false)
function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })
    win.loadFile('index.html')
    const request = net.request('http://localhost:3000/list')
    request.on('response', (response) => {
        if (response.statusCode == 200) {
            response.on('data', (chunk) => {
                console.log(JSON.parse(chunk))
            })
        } else {
            console.log(response.statusMessage)
        }
    })
    request.end()
}

app.on('ready', createWindow)