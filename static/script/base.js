window.onload=function ()
{
    displayWindowSize();
}

window.addEventListener("resize", displayWindowSize);

function displayWindowSize(){
    var container = document.getElementsByClassName("side-list3")[0];
    var side = document.getElementById("side-menu");
    var container2 = document.getElementById("container-box");
    var center = document.getElementById("center-box");
    var add_container = document.getElementById("add-container");
    container.style.height = "calc(100vh - 485px)"
    if (document.body.clientWidth < 750){
        side.style.width = "0px";
        container2.style.width = "100vw";
        side.style.zIndex = "100";
        center.style.width = "90vw";
        add_container.style.width = "96vw";
    } else {
        side.style.width = "255px";
        center.style.width = "calc(100vw - 500px)";
        container2.style.width = "calc(100vw - 255px)";
        add_container.style.width = "40%";
    }

}

function side() {
    var side = document.getElementById("side-menu");
    var container = document.getElementById("container-box");
    if (side.style.width !== "0px") {
        side.style.width = "0px";
        container.style.width = "100vw";
    } else {
        side.style.width = "255px";
        if (document.body.clientWidth >= 750){
            container.style.width = "calc(100vw - 255px)";
        } else {
            container.style.width = "100vw";
        }
    }
}

function rotate() {
    var id = document.getElementById("side-title-btn2");
    if (id.style.transform === "rotate(0deg)") {
        id.style.transform = "rotate(90deg)";
    } else {
        id.style.transform = "rotate(0deg)";
    }
}

