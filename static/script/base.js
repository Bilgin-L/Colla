function side() {
    var side = document.getElementById("side-menu");
    if (side.style.width !== "0px") {
        side.style.width = "0px";
    } else {
        side.style.width = "255px";
    }
}