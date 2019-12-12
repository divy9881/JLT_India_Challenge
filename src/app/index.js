document.getElementById("filesList").innerHTML = "hello";
const request = net.request({
    method: 'GET',
    protocol: 'http:',
    hostname: 'localhost',
    port: 3000,
    path: '/list'
})
request.on('response', (response) => {
    document.getElementById("filesList").innerHTML = "response";
    console.log(response);
})