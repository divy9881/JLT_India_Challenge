let fields = null
let file = null

function generateDataFields(){
    
    let {remote} = require("electron")
    file = remote.getGlobal("getFilename")()
    remote.getGlobal("setFilename")(null)

    let python = require('child_process').spawn('python', [__dirname+"../app/python/parse.py",__dirname+"/templates/"+file]);
    python.stdout.on('data',function(dump){
        dump = dump.toString('utf8')
        fields = JSON.parse(dump)
        let data_fields = document.getElementById("data-fields")
        let inner_html = ""
        for(let key in fields){
            inner_html += `<div class="form-group">
            <label for="${fields[key]}">${fields[key]}</label>
            <textarea class="form-control" id="${fields[key]}" rows="3"></textarea>
            </div>`
        }
        data_fields.innerHTML = inner_html
    });

}

let userData = {}

function PassTheDataFields(){
    for(let key in fields){
        let data_field = document.getElementById(`${fields[key]}`)
        let data = data_field.value
        userData[fields[key]] = data
    }
    let userDataStr = JSON.stringify(userData)
    let python = require('child_process').spawn('python', [__dirname+"../app/python/doc_assist.py",__dirname+"/templates/"+file,userDataStr]);
    python.stdout.on('data',function(dump){
        dump = dump.toString('utf8')
        console.log(dump)
        fields = JSON.parse(dump)
        console.log(fields)
    })
}

generateDataFields()
