const testFolder = './templates/';
const fs = require('fs');
const express = require('express');
const app = express();
app.get('/', (req, res)=>{
    res.send("Doc Assist");
})

app.get('/download/:filename', (req, res) => {
    const path = `${__dirname}/templates/${req.params.filename}`;
    res.download(path);
});

app.get('/get_templates', (req, res) => {
    op = [];
    fs.readdirSync(testFolder).forEach(file => {
        op.push(file);
    });
    res.send(op);
});

app.listen(3000);