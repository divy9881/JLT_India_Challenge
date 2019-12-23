let local_btn = document.getElementById("local-btn")

let {dialog} = require("electron").remote
let { remote } = require('electron');

local_btn.addEventListener("click", function(){
    dialog.showOpenDialog({
        filters:[{
            name:"DOCX FILE",
            extensions:["docx"]
        }]
    }).then(function(docxFile){
        if(docxFile === undefined){
            alert("No file was selected")
            return
        }
        else{
            let file_str = JSON.stringify(docxFile.filePaths)
            let filepath = file_str.slice(2,file_str.length-2)
            let str_arr = filepath.split("\\")
            let filename = str_arr[str_arr.length-1]

            remote.getGlobal("setFilename")(filepath)

            alert(filename + " has been selected to generate the output documents.")

            document.location = __dirname + "/template-data-fields.html"
        }
    })
})