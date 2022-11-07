from flask import session
from models import UserModel, CategoryModel
import datetime
from sqlalchemy import extract
from datetime import timezone, timedelta

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


def notification_list(notifications):
    notification_total_list = []
    data = []
    # Add all data in 'notification' in notifications to the list
    for notification in notifications:
        data.append(notification.id)
        data.append(notification.content)
        # get the year, month and day of the notification
        date = notification.create_time.date()
        data.append(date)
        notification_total_list.append(data)
        data = []
    return notification_total_list


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


def get_all_todos(todo_model, user_id, filters, sort, attribute, category=None):

    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    today = datetime.datetime.now(SHA_TZ)

    model_year = extract('year', todo_model.due_date)
    model_month = extract('month', todo_model.due_date)
    model_day = extract('day', todo_model.due_date)

    if attribute == "index":
        todos = todo_model.query.filter_by(user_id=user_id, trash=0)
    elif attribute == "important":
        todos = todo_model.query.filter_by(important=1)
    elif attribute == "today":
        todos = todo_model.query.filter_by(user_id=user_id, trash=0).filter(model_year == today.year,
                                                                            model_month == today.month,
                                                                            model_day == today.day)
    elif attribute == "upcoming":
        todos = todo_model.query.filter_by(user_id=user_id, trash=0).filter(model_year >= today.year,
                                                                            model_month >= today.month,
                                                                            model_day > today.day)
    elif attribute == "timeout":
        todos = todo_model.query.filter_by(user_id=user_id, trash=0).filter(todo_model.due_date < today)

    if filters == "completed":
        todos = todos.filter_by(user_id=user_id, trash=0, status=1)
    elif filters == "uncompleted":
        todos = todos.filter_by(user_id=user_id, trash=0, status=0)
    else:
        # Get all todos which 'trash' == 0 in a user, and sort them by 'status' and 'due_date'
        todos = todos.filter_by(user_id=user_id, trash=0)

    if category is not None:
        todos = todos.filter_by(category_id=category)

    if sort == "Duedate":
        todos = todos.order_by(todo_model.status, todo_model.due_date).all()
    elif sort == "Dateadded":
        todos = todos.order_by(todo_model.status, todo_model.create_time).all()
    elif sort == "Assessment":
        todos = todos.order_by(todo_model.status, todo_model.assessment_name).all()
    elif sort == "Module":
        todos = todos.order_by(todo_model.status, todo_model.module_name).all()
    
    return todos


def basic_information():
    user_id = session.get("user_id")
    # Get the user information
    user = UserModel.query.get(user_id)
    # Get all categories in a user
    categories = CategoryModel.query.filter_by(user_id=user_id).all()

    return user_id, user, categories
