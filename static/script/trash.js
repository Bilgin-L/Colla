// # ///////////////////////////////////////////////////////////////////////////
// # @file: register.js
// # @time: 2022/10/19
// # @author: Yuheng Liu
// # @email: sc20yl2@leeds.ac.uk && i@bilgin.top
// # @organisation: University of Leeds
// # @url: colla.bilgin.top
// # ///////////////////////////////////////////////////////////////////////////

// recover the todos from trash
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

// delete the todos permanently
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