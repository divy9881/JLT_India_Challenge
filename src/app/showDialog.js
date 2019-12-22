let {dialog} = require("electron").remote

console.log("hello")

let selectFileButton = document.querySelector("#select-file")

console.log(selectFileButton)

selectFileButton.addEventListener("click",function(){
    dialog.showOpenDialog({
        filters:[{
            name:"CSV FILE",
            extensions:["csv"]
        }]
    }).then(function(filename){
        if(filename === undefined){
            alert("No file was selected")
            return
        }
        else{
            alert(filename)
            console.log(filename.filePaths)
        }
    })
})