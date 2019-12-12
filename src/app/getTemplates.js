const main = async function() {
    const res = await fetch("http://localhost:3000/get_templates");
    const data = await res.json();
    console.log(JSON.stringify(data));
    AddFileEntries(data);
}

main();

function AddFileEntries(files){
    let divEle = document.getElementById("fetch_files");
    files.forEach(file => {

        divEle.innerHTML +=   `
            <a href="/download/${file}" class="file">${file}</a>
            <hr class="hr-mod">
        `;
    });
}