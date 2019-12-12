const testFolder = './templates/';
const fs = require('fs');
const express = require('express');
const app = express();
app.get('/', (req, res)=>{
    res.send("Doc Assist");
})

app.get('/list', (req, res) => {
    res.json([
        { "name": "cpp.cpp" },
        { "name": "py.py" },
        { "name": "js.js" },
    ]);
});

app.get('/download/:filename', (req, res) => {
    console.log(req.params.filename);
});

app.get('/get_templates', (req, res) => {
    op = [];
    fs.readdirSync(testFolder).forEach(file => {
        op.push(file);
    });
    res.send(op);
});

app.listen(3000);