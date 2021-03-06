let { dialog } = require("electron").remote

let fields = null
let file = null

function generateDataFields() {
    let { remote } = require("electron")
    file = remote.getGlobal("getFilename")()

    //remote.getGlobal("setFilename")(null)

    let python = require('child_process').spawn('python', [__dirname + "\\..\\python\\parse.py", file]);
    python.on('error', (error) => {
        dialog.showMessageBox({
            title: 'Error',
            type: 'warning',
            message: 'Error occured.\r\n' + error
        });
    });
    python.stdout.on('data', function (dump) {
        dump = dump.toString('utf8')
        let status = String(dump).substr(0, dump.indexOf("\n")).trim();
        //console.log(status);
        let data = dump.substring(dump.indexOf("\n") + 1).trim();
        if (status == "True") {
            fields = JSON.parse(data);
            let data_fields = document.getElementById("data-fields")
            let inner_html = ""
            for (let key in fields) {
                inner_html += `<div class="form-group">
                <label for="${fields[key]}">${fields[key]}</label>
                <textarea class="form-control" id="${fields[key]}" rows="3"></textarea>
                </div>`
            }
            data_fields.innerHTML = inner_html
        } else {
            alert(data);
        }
    });
    python.stderr.on('data', (data) => {
        console.error(data.toString());
    });
    python.on('exit', (code) => {
        console.log(`Process exited with code ${code}`);
    });
}

let userData = {}

function PassTheDataFields() {
    dialog.showOpenDialog({
        properties: ['openDirectory']
    }).then(function (f) {
        if (f === undefined || f.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
            PassTheDataFields()
        } else {
            let outputFolder = f.filePaths[0]
            for (let key in fields) {
                let data_field = document.getElementById(`${fields[key]}`)
                let data = data_field.value
                userData[key] = data
            }
            let userDataStr = JSON.stringify(userData)
            //console.log(userData)
            let python = require('child_process').spawn('python', [__dirname + "\\..\\python\\doc_assist.py", file, userDataStr, outputFolder]);
            python.on('error', (error) => {
                dialog.showMessageBox({
                    title: 'Error',
                    type: 'warning',
                    message: 'Error occured.\r\n' + error
                });
            });
            python.stdout.on('data', function (dump) {
                dump = dump.toString('utf8')
                let status = String(dump).substr(0, dump.indexOf("\n")).trim();
                //console.log(status);
                let data = dump.substring(dump.indexOf("\n") + 1).trim();
                if (status == "True") {
                    alert("The generated file is: " + data);
                } else {
                    alert("Error: " + data);
                }
            })
            python.stderr.on('data', (data) => {
                console.error(data.toString());
            });
            python.on('exit', (code) => {
                console.log(`Process exited with code ${code}`);
            });
        }
    })
}

generateDataFields()