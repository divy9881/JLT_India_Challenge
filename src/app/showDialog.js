// const { dialog } = require("electron").remote

//console.log("hello")

let selectFileButton = document.querySelector("#select-file")

let backButton = document.querySelector("#back")

backButton.addEventListener("click", function () {
    document.location = __dirname + "/index.html"
})

//console.log(selectFileButton)

selectFileButton.addEventListener("click", function () {
    dialog.showOpenDialog({
        filters: [{
            name: "DATA INPUT FILE",
            extensions: ["csv", "json", "xml"]
        }]
    }).then(function (csvFile) {
        if (csvFile === undefined || csvFile.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
            return
        }
        else {
            let file_str = JSON.stringify(csvFile.filePaths)
            // console.log(JSON.stringify(csvFile.filePaths))
            //console.log(file_str)
            let filepath = file_str.slice(2, file_str.length - 2)
            let str_arr = filepath.split("\\")
            let filename = str_arr[str_arr.length - 1]
            alert("\"" + filename + "\" HAS BEEN SELECTED TO GENERATE THE OUTPUT DOCUMENTS.")

            let { remote } = require("electron")
            let file = remote.getGlobal("getFilename")()
            // remote.getGlobal("setFilename")(null)

            //console.log(file, filepath)
            callPythonScript(file, filepath)
        }
    })
})

function callPythonScript(file, filepath) {
    dialog.showOpenDialog({
        properties: ['openDirectory']
    }).then(function (outputFolder) {
        if (outputFolder === undefined || outputFolder.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
            callPythonScript(file, filepath)
        } else {
            const outputFolderPath = outputFolder.filePaths[0]
            let python = require('child_process').spawn('python37', [__dirname + "\\..\\python\\main_file_input.py", file, filepath, outputFolderPath]);
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
                    alert("Successfully Generated the Document(s).");
                } else {
                    alert("Error: " + data);
                    console.log(data)
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