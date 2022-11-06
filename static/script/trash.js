function recoverTodo(obj, id) {
    // delete the parent's parent element of the obj
    obj.parentNode.parentNode.remove();
    $.ajax({
        url: "/recover_todo",
        method: "POST",
        data: {
            "id": id
        }
    })
}

function deleteTodo(obj, id) {
    // delete the parent's parent element of the obj
    obj.parentNode.parentNode.remove();
    $.ajax({
        url: "/delete_todo",
        method: "POST",
        data: {
            "id": id
        }
    })
}