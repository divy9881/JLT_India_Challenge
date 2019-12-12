const fs = require('fs');
const express = require('express');
const app = express();
app.get('/', (req, res)=>{
    req.send("Doc Assist");
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
app.listen(3000, () => {

});
