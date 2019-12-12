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
        let html = "";
        if (response.statusCode == 200) {
            response.on('data', (chunk) => {
                filesList = JSON.parse(chunk);
                for(let i=0;i<filesList.length;i++) {
                    html += `<a href='http:localhost:3000/download/${filesList[i].name}>${filesList[i].name}</a>`
                }
                // TODO Modify document.getElementById("filesList").innerHTML to the html string
            })
        } else {
            console.log(response.statusMessage)
        }
    })
    request.end()
}

app.on('ready', createWindow)