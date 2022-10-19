function side() {
    var side = document.getElementById("side-menu");
    var container = document.getElementById("container-box");
    if (side.style.width !== "0px") {
        side.style.width = "0px";
        container.style.width = "100vw";
    } else {
        side.style.width = "255px";
        container.style.width = "calc(100vw - 255px)";
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