let { dialog } = require("electron").remote

let outputFolder = null

document.getElementById("selectOutputDirectoryBtn").addEventListener("click", function () {
    dialog.showOpenDialog({
        properties: ['openDirectory']
    }).then(function (file) {
        if (file === undefined || file.filePaths.length === 0) {
            // alert("NO FILE WAS SELECTED.")
            outputFolder = null
            document.getElementById("outputFolder").innerText = "Output folder: NOT SELECTED";
        } else {
            outputFolder = file.filePaths[0]
            document.getElementById("outputFolder").innerText = "Output folder: " + outputFolder;
        }
    })
});

document.getElementById("convertButton").addEventListener("click", function () {
    if (outputFolder == null) {
        alert("Please select output file and folder")
    } else {
        if(!outputFolder || !document.getElementById("outputFilenameInput").value) {
            alert("Please select an output file")
            return
        }

        let outputFile = outputFolder + "\\" + document.getElementById("outputFilenameInput").value
        
        let { remote } = require("electron")
        let inputFile = remote.getGlobal("getInputForConverter")()

        let python = require('child_process').spawn('python', [__dirname + "\\..\\python\\output_converter.py", inputFile, outputFile]);
        python.on('error', (error) => {
            dialog.showMessageBox({
                title: 'Error',
                type: 'warning',
                message: 'An error occured:\r\n' + error
            });
        });
        python.stdout.on('data', function (dump) {
            dump = String(dump.toString('utf8'))
            let status = String(dump).substr(0, dump.indexOf("\n")).trim();
            if (status == "True") {
                alert("File Converted");
                document.location = __dirname + "/index.html"
            } else {
                alert(dump.substring(dump.indexOf("\n") + 1).trim());
            }
        });
        python.stderr.on('data', (data) => {
            console.error(data.toString());
            alert("An error occurred");
        });
        python.on('exit', (code) => {
            console.log(`Process exited with code ${code}`);
        });
    }
});

document.getElementById("backButton").addEventListener("click", function () {
    document.location = __dirname + "/index.html"
});