def todos_list(todos):
    todos_total_list = []
    data = []
    # Add all data in 'todo' in todos to the list
    for todo in todos:
        data.append(todo.id)
        data.append(todo.module_code)
        data.append(todo.module_name)
        data.append(todo.assessment_name)
        data.append(todo.due_date)
        data.append(todo.description)
        data.append(todo.status)
        data.append(todo.create_time)
        if todo.email_inform == 1:
            data.append("Turn on")
        else:
            data.append("Turn off")
        data.append(todo.status_email)
        data.append(todo.status_notification)
        if todo.important == 1:
            data.append("Important")
        else:
            data.append("Normal")
        data.append(todo.trash)
        data.append(todo.category_name)

        # get the month of the due date
        month = todo.due_date.month
        if month == 1:
            data.append("Jan")
        elif month == 2:
            data.append("Feb")
        elif month == 3:
            data.append("Mar")
        elif month == 4:
            data.append("Apr")
        elif month == 5:
            data.append("May")
        elif month == 6:
            data.append("Jun")
        elif month == 7:
            data.append("Jul")
        elif month == 8:
            data.append("Aug")
        elif month == 9:
            data.append("Sep")
        elif month == 10:
            data.append("Oct")
        elif month == 11:
            data.append("Nov")
        elif month == 12:
            data.append("Dec")
        # get the day of the due date
        day = todo.due_date.day
        data.append(day)
        data.append(todo.category_id)
        todos_total_list.append(data)
        data = []
    return todos_total_list


def progress_bar(todos):
    # ---------------------------------------------------
    # The code below is used to compute the progress bar
    # the sum of all todos
    todo_sum = len(todos)
    # the sum of all todos that are completed
    todo_completed = 0
    for todo in todos:
        if todo.status:
            todo_completed += 1
    # the rate of completed todos
    if todo_sum == 0:
        todo_rate = 0
    else:
        todo_rate = todo_completed / todo_sum * 100
    # ----------------------------------------------------
    return todo_sum, todo_completed, todo_rate


def get_all_todos(todo_model, user_id, filters):
    print(filters)
    if filters == "completed":
        print("11111")
        todos = todo_model.query.filter_by(user_id=user_id, trash=False, status=1).order_by(todo_model.due_date).all()
    elif filters == "uncompleted":
        todos = todo_model.query.filter_by(user_id=user_id, trash=False, status=0).order_by(todo_model.due_date).all()
    else:
        # Get all todos which 'trash' == 0 in a user, and sort them by 'status' and 'due_date'
        todos = todo_model.query.filter_by(user_id=user_id, trash=0).order_by(todo_model.status,
                                                                              todo_model.due_date).all()
    return todos
