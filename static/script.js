let multiplefileInput = document.getElementById("file-input-multiple");
let singlefileInput = document.getElementById("file-input-single");
let multipleimageContainer = document.getElementById("images");
let singleimageContainer = document.getElementById("images-single");
let numOfFiles = document.getElementById("num-of-files");

function multiplePreview(){
    multipleimageContainer.innerHTML = "";
    numOfFiles.textContent = `${multiplefileInput.files.length} Files Selected`;

    for(i of multiplefileInput.files){
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerText = i.name;
        figure.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            figure.insertBefore(img,figCap);
        }
        multipleimageContainer.appendChild(figure);
        reader.readAsDataURL(i);
    }
}

function singlePreview(){
    singleimageContainer.innerHTML = "";
    numOfFiles.textContent = `${singlefileInput.files.length} Files Selected`;

    for(i of singlefileInput.files){
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerText = i.name;
        figure.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            figure.insertBefore(img,figCap);
        }
        singleimageContainer.appendChild(figure);
        reader.readAsDataURL(i);
    }
}