window.onload = function () {
    displayWindowSize();
    closeAlert();
}

window.addEventListener("resize", displayWindowSize);

function displayWindowSize() {
    var container = document.getElementsByClassName("side-list3")[0];
    var side = document.getElementById("side-menu");
    var container2 = document.getElementById("container-box");
    var center = document.getElementById("center-box");
    var add_container = document.getElementById("add-container");
    container.style.height = "calc(100vh - 485px)"
    if (document.body.clientWidth < 750) {
        side.style.width = "0px";
        // set the box shadow
        side.style.boxShadow = "0px 20px 40px 0px rgb(0 0 0 / 40%)";
        container2.style.width = "100vw";
        side.style.zIndex = "100";
        center.style.width = "90vw";
        add_container.style.width = "96vw";
    } else {
        side.style.boxShadow = "none";
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
        if (document.body.clientWidth >= 750) {
            container.style.width = "calc(100vw - 255px)";
        } else {
            container.style.width = "100vw";
        }
    }
}

function rotate() {
    var container = document.getElementsByClassName("side-list3")[0];
    var id = document.getElementById("side-title-btn2");
    if (id.style.transform === "rotate(0deg)") {
        id.style.transform = "rotate(90deg)";
    } else {
        container.style.height = "calc(100vh - 485px) !important";
        id.style.transform = "rotate(0deg)";
    }
}

function deleteCategory(obj, id) {
    obj.parentNode.parentNode.removeChild(obj.parentNode);
    $.ajax({
            url: "/delete_category",
            method: "POST",
            data: {
                "category_id": id
            }
        }
    )
}

function closeAlert() {
    // after 5 seconds, the alert will be closed automatically with a fade out effect
    setTimeout(function () {
        $(".alert").fadeOut();
    }, 5000)
}

function timeFormat(time) {
    // convert the date format from '2022-11-03 00:00:00' to '2022-11-03T00:00'
    let date = new Date(time);
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    let hour = date.getHours();
    let minute = date.getMinutes();
    let second = date.getSeconds();
    if (month < 10) {
        month = "0" + month;
    } else {
        month = month.toString();
    }
    if (day < 10) {
        day = "0" + day;
    } else {
        day = day.toString();
    }
    if (hour < 10) {
        hour = "0" + hour;
    } else {
        hour = hour.toString();
    }
    if (minute < 10) {
        minute = "0" + minute;
    } else {
        minute = minute.toString();
    }
    if (second < 10) {
        second = "0" + second;
    } else {
        second = second.toString();
    }
    return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second;
}

