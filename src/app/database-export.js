document.querySelector("form").addEventListener("submit", function (event){
    event.preventDefault()
})

// mongoexport --uri="mongodb://mongodb0.example.com:27017/reporting"  --collection=events  --out=events.json [additional options]

document.getElementById("data-btn").addEventListener("click",function(){
    const url = document.getElementById("url").value
    const collection = document.getElementById("collection").value
    const outfilename = document.getElementById("filename").value

    let mongoexport = require('child_process').spawn('mongoexport', [`--uri=\"${url}\"`, `--collection=${collection}`, `--out=${outfilename}`]);

    mongoexport.on('exit', (code) => {
        const fs = require("fs")
    
        var oldPath = __dirname + "\\" + outfilename
        var newPath = __dirname + "\\exports\\" + outfilename

        fs.rename(oldPath, newPath, function (err) {
            if (err) throw err
            alert("EXPORT FILE GENERATED.")
        })
    });
    
})

document.getElementById("back").addEventListener("click", function(){
    document.location = __dirname + "/index.html"
})