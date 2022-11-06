function timeCount(due_date, id) {
    function addZero(i) {
        return i < 10 ? '0' + i : i;
    }

    let countDownDate = document.querySelector("#countDown-" + id);
    let timer = null;
    const startTime = new Date().getTime();
    const endTime = new Date(due_date).getTime();
    const time = endTime - startTime;
    if (time > 0) {
        timer = setInterval(function () {
            const nowTime = new Date().getTime();
            const time = endTime - nowTime;
            const day = Math.floor(time / 1000 / 60 / 60 / 24);
            const hour = Math.floor(time / 1000 / 60 / 60 % 24);
            const minute = Math.floor(time / 1000 / 60 % 60);
            const second = Math.floor(time / 1000 % 60);
            countDownDate.innerHTML = addZero(day) + " D " + addZero(hour) + " h " + addZero(minute) + " m " + addZero(second) + " s";
        }, 1000);
    } else {
        countDownDate.style.color = "red";
        countDownDate.innerHTML = "Time Out";
    }
}

function completed(id) {
    $.ajax({
        url: "/completed",
        method: "POST",
        data: {
            "id": id
        },
        success: function (res) {
            if (res['code'] === 200) {
                window.location.reload();
            } else {
                alert(res['message']);
            }
        }
    })
}

function trashTodo(obj, id) {
    // delete the parent's parent element of the obj
    obj.parentNode.parentNode.remove();
    $.ajax({
        url: "/trash_todo",
        method: "POST",
        data: {
            "id": id
        },
        success: function (res) {
            if (res['code'] === 200) {
                window.location.reload();
            } else {
                alert(res['message']);
            }
        }
    })
}

function indexAll() {
    $.ajax({
        url: "/filter",
        method: "POST",
        data: {
            "filters" : "all"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexCompleted() {
    $.ajax({
        url: "/filter",
        method: "POST",
        data: {
            "filters" : "completed"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexUnCompleted() {
    $.ajax({
        url: "/filter",
        method: "POST",
        data: {
            "filters" : "uncompleted"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexAssessment(){
    $.ajax({
        url: "/sort",
        method: "POST",
        data: {
            "sort" : "Assessment"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexModule(){
    $.ajax({
        url: "/sort",
        method: "POST",
        data: {
            "sort" : "Module"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexDuedate(){
    $.ajax({
        url: "/sort",
        method: "POST",
        data: {
            "sort" : "Duedate"
        },
        success: function () {
            window.location.reload();
        }
    })
}

function indexDateadded(){
    $.ajax({
        url: "/sort",
        method: "POST",
        data: {
            "sort" : "Dateadded"
        },
        success: function () {
            window.location.reload();
        }
    })
}

