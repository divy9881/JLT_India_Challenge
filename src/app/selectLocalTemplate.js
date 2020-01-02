let local_btn = document.getElementById("local-btn")

let { dialog } = require("electron").remote
let { remote } = require('electron');

local_btn.addEventListener("click", function () {
    dialog.showOpenDialog({
        filters: [{
            name: "DOCX FILE",
            extensions: ["docx"]
        }]
    }).then(function (docxFile) {

        if (docxFile === undefined || docxFile.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
            return
        }
        else {
            let file_str = JSON.stringify(docxFile.filePaths)
            let filepath = file_str.slice(2, file_str.length - 2)
            let str_arr = filepath.split("\\")
            let filename = str_arr[str_arr.length - 1]

            remote.getGlobal("setFilename")(filepath)

            alert("\"" + filename + "\" HAS BEEN SELECTED TO GENERATE THE OUTPUT DOCUMENT.")

            document.location = __dirname + "/template-data-fields.html"
        }
    })
});

document.getElementById("input-converter-btn").addEventListener("click", function () {
    dialog.showOpenDialog({
        filters: [{
            name: "DATA FILE",
            extensions: ["csv", "json", "xml"]
        }]
    }).then(function (file) {
        if (file === undefined || file.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
        } else {
            let file_str = JSON.stringify(file.filePaths)
            let filepath = file_str.slice(2, file_str.length - 2)
            let str_arr = filepath.split("\\")
            let filename = str_arr[str_arr.length - 1]

            remote.getGlobal("setInputForConverter")(filepath)

            document.location = __dirname + "/inputConverter.html"
            
            alert("\"" + filename + "\" HAS BEEN SELECTED TO BE CONVERTED.")
        }
    })
});

document.getElementById("output-converter-btn").addEventListener("click", function () {
    dialog.showOpenDialog({
        filters: [{
            name: "DOCX FILE",
            extensions: ["docx"]
        }]
    }).then(function (file) {
        if (file === undefined || file.filePaths.length === 0) {
            alert("NO FILE WAS SELECTED.")
        } else {
            let file_str = JSON.stringify(file.filePaths)
            let filepath = file_str.slice(2, file_str.length - 2)
            let str_arr = filepath.split("\\")
            let filename = str_arr[str_arr.length - 1]

            remote.getGlobal("setInputForConverter")(filepath)

            document.location = __dirname + "/outputConverter.html"
            
            alert("\"" + filename + "\" HAS BEEN SELECTED TO BE CONVERTED.")
        }
    })
});