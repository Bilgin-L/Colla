# ///////////////////////////////////////////////////////////////////////////
# @file: controller.py
# @time: 2022/10/19
# @author: Yuheng Liu
# @email: sc20yl2@leeds.ac.uk && i@bilgin.top
# @organisation: University of Leeds
# @url: colla.bilgin.top
# ///////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////
# import flask
from flask import session
# import database
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import extract
from models import UserModel, CategoryModel, NotificationModel, TodoModel
# import pyecharts
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Calendar
# import extensions
import calendar
import datetime
from datetime import timezone, timedelta
from extensions import db
# ///////////////////////////////////////////////////////////////////////////


def todos_list(todos):
    """
    This function is used to get all todos in a user

    :param todos: all todos in a user
    :return: a list of all todos

    """

    todos_total_list = []
    data = []

    # Add all data in 'todos' in todos to the list
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
    """
    This function is used to get all notifications in a user

    :param notifications: all notifications in a user
    :return: a list of all notifications

    """

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
    """
    This function is used to generate a progress bar

    :param todos: all todos in a user
    :return: all attributes of the progress bar

    """

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

    return todo_sum, todo_completed, todo_rate


def get_all_todos(todo_model, user_id, filters, sort, attribute, category=None):
    """
    This function is used to get all todos in a user

    :param todo_model: the model of todos
    :param user_id: the id of a user
    :param filters: the filters of todos
    :param sort: the sort of todos
    :param attribute: the attribute of todos
    :param category: the category of todos
    :return: all todos in a user

    """

    # set timezone
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    # get the current time
    today = datetime.datetime.now(SHA_TZ)

    # get the model date
    model_year = extract('year', todo_model.due_date)
    model_month = extract('month', todo_model.due_date)
    model_day = extract('day', todo_model.due_date)

    # the attribute
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

    # if the category is not None, get all todos in the category
    if category is not None:
        todos = todos.filter_by(category_id=category)

    # sort the todos
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
    """
    This function is used to get the basic information of a user

    :return: the basic information of a user

    """

    # get the current user
    user_id = session.get("user_id")

    # Get the user information
    user = UserModel.query.get(user_id)

    # Get all categories in a user
    categories = CategoryModel.query.filter_by(user_id=user_id).all()

    return user_id, user, categories


def check_notification():
    """
    This function is used to check the notification status

    :return: the notification status

    """

    # get the current user
    user_id = session.get("user_id")

    # Get all notifications in a user
    todos = TodoModel.query.filter_by(user_id=user_id, trash=0).all()
    notification_trigger = 0
    contents_list = []

    # Traverse all todos of the current user
    for todo in todos:

        # If the time of todos is less than 24 hours and the notification is not sent, then send a notification
        if todo.due_date - datetime.datetime.now() < datetime.timedelta(hours=24) and todo.status_notification == 0 \
                and todo.status == 0:
            todo.status_notification = 1
            db.session.commit()

            # Generate a notification
            contents = "Your todo '" + todo.assessment_name + "' is due in 24 hours."
            notification = NotificationModel(user_id=user_id, content=contents, create_time=datetime.datetime.now())

            # database rollback
            try:
                db.session.add(notification)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e

            # save the contents
            contents_list.append(contents)

            # set the notification trigger
            notification_trigger = 1

    return notification_trigger, contents_list


def pie_chart():
    """
    This function is used to generate a pie chart

    :return: the pie chart
    """

    # get the current user
    user_id = session.get("user_id")

    # Get all categories in a user
    categories = CategoryModel.query.filter_by(user_id=user_id).all()

    # Get all todos in a user
    todos = TodoModel.query.filter_by(user_id=user_id, trash=0).all()

    # Get the number of todos in each category
    category_num = []
    for category in categories:
        num = 0
        for todo in todos:
            if todo.category_id == category.id:
                num += 1
        category_num.append(num)

    # Get the name of each category
    category_name = []
    for category in categories:
        category_name.append(category.name)

    c = (
        # Generate a pie chart
        Pie(init_opts=opts.InitOpts(width="330px", height="200px"))

        # Add data
        .add(
            "",
            [list(z) for z in zip(category_name, category_num)],
            radius=["40%", "70"],
            label_opts=opts.LabelOpts(position="center",
                                      is_show=False),

        )

        # Set the style of the pie chart
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top="20px", is_show=False),
        )

        # Set the style of the pie chart
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}"),
        )

        # Render the pie chart
        .render("static/echarts/pie_radius.html")
    )
    return c


def bar_chart():
    """
    This function is used to generate a bar chart

    :return: the bar chart

    """

    # get the current user
    user_id = session.get("user_id")

    # Get all todos in a user
    todos = TodoModel.query.filter_by(user_id=user_id, trash=0).all()

    # Get the num of important todos in a user
    important_num = 0
    for todo in todos:
        if todo.important == 1:
            important_num += 1

    # Get the num of Today todos in a user
    today_num = 0
    for todo in todos:
        if todo.due_date.date() == datetime.datetime.now().date():
            today_num += 1

    # Get the num of Upcoming todos in a user
    upcoming_num = 0
    for todo in todos:
        if todo.due_date.date() > datetime.datetime.now().date():
            upcoming_num += 1

    # Get the num of Timeout todos in a user
    timeout_num = 0
    for todo in todos:
        if todo.due_date.date() < datetime.datetime.now().date():
            timeout_num += 1

    c = (
        # Generate a bar chart
        Bar(init_opts=opts.InitOpts(width="330px", height="200px", theme=ThemeType.LIGHT))

        # Add data
        .add_xaxis(
            [
                "Important",
                "Today",
                "Upcoming",
                "Timeout",
            ]
        )

        # Add data
        .add_yaxis("Todos", [important_num, today_num, upcoming_num, timeout_num],
                   label_opts=opts.LabelOpts(position="center", is_show=False),)

        # Set the style of the bar chart
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        )

        # Render the bar chart
        .render("static/echarts/bar_chart.html")
        )

    return c


def calender_chart():
    """
    This function is used to generate a calendar chart

    :return: the calendar chart

    """

    # Use calendar to record the number of todos in each day
    # Get the user id
    user_id = session.get("user_id")

    # Get all todos in a user
    todos = TodoModel.query.filter_by(user_id=user_id, trash=0).all()

    cal = calendar.Calendar()
    year = datetime.datetime.now().year
    data = []
    for month in range(1, 13):
        for day in cal.itermonthdays(year, month):
            if day != 0:
                num = 0
                for todo in todos:
                    if todo.due_date.date() == datetime.date(year, month, day):
                        num += 1
                data.append([str(year) + "-" + str(month) + "-" + str(day), num])

    c = (
        # Generate a calendar chart
        Calendar(init_opts=opts.InitOpts(width="760px", height="250px"))

        # Add data
        .add(
            "",
            data,
            calendar_opts=opts.CalendarOpts(
                range_=year,
                pos_right="100px",
                pos_top="60px",
                pos_bottom="100px",
            ),
        )

        # Set the style of the calendar chart
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=5,
                min_=0,
                orient="horizontal",
            ),
        )

        # Render the calendar chart
        .render("static/echarts/calendar_chart.html")
    )
    return c
