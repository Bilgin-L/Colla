// # ///////////////////////////////////////////////////////////////////////////
// # @file: base.js
// # @time: 2022/10/19
// # @author: Yuheng Liu
// # @email: sc20yl2@leeds.ac.uk && i@bilgin.top
// # @organisation: University of Leeds
// # @url: colla.bilgin.top
// # ///////////////////////////////////////////////////////////////////////////

// on load function
window.onload = function () {
    // load bootstrap
    var tooltipTriggerList = Array.prototype.slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // call functions
    displayWindowSize();
    closeAlert();
}

// on resize function
window.addEventListener("resize", displayWindowSize);

// set the width of the elements
function displayWindowSize() {
    // get all elements
    var container = document.getElementsByClassName("side-list3")[0];
    var add_container = document.getElementById("add-container");
    var calender = document.getElementById("calender-chart");

    // set the height
    container.style.height = "calc(100vh - 485px)"

    // set the width
    if (document.body.clientWidth < 750) {
        add_container.style.width = "96vw";
    } else {
        add_container.style.width = "40%";
    }
    if (document.body.clientWidth < 995) {
        calender.style.visibility = "hidden";
        calender.style.height = "0px";
    } else {
        calender.style.visibility = "visible";
        calender.style.height = "auto";
    }

}

// click event for the button hide and show the side list
function side() {
    var side = document.getElementById("side-menu");
    var container = document.getElementById("container-box");
    const cssSide = window.getComputedStyle(side);

    // detect the status of the side list
    if (cssSide.getPropertyValue("width") !== "0px") {
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

// click event for the animation of the button
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

// ajax function for deleting the category
function deleteCategory(obj, id) {
    obj.parentNode.parentNode.removeChild(obj.parentNode);
    $.ajax({
            url: "/delete_category",
            method: "POST",
            data: {
                "category_id": id
            },
            success: function () {
                window.location.reload();
            }
        }
    )
}

// function for closing the alert in 5s
function closeAlert() {
    // after 5 seconds, the alert will be closed automatically with a fade out effect
    setTimeout(function () {
        $(".alert").fadeOut();
    }, 5000)
}

// convert the format of the time
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

// ajax function for clearing the notification
function clearNotification() {
    $.ajax({
        url: "/clear_notification",
        method: "POST",
        success: function () {
            // delete all classes called 'notification-table'
            $(".notification-table").remove();
        }
    })
}

// click function for open the modal
function openStatistic() {
    $("#statistic").modal("show");
}
