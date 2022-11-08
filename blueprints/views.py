from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import EmailCaptchaModel, UserModel, CategoryModel, TodoModel, NotificationModel
from .forms import RegisterForm, LoginForm, AddCategoryForm, AddTodoForm
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mail, db
from flask_mail import Message
import string
import random
from datetime import datetime
from decoration import login_required, check_category, email_inform
from controller import todos_list, progress_bar, get_all_todos, basic_information, notification_list, check_notification\
    , pie_chart, bar_chart, calender_chart
from sqlalchemy import or_

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def index():

    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")
    attribute = "index"

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, attribute)
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)
    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    notification_trigger, notification_contents = check_notification()
    if notification_trigger:
        for content in notification_contents:
            flash(content)

    # function: get the pie chart
    pie_chart_data = pie_chart()
    bar_chart_data = bar_chart()
    calender_data = calender_chart()

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Inbox",
                           notification_list=notificatons_total_list, pie_chart_data=pie_chart_data,
                           bar_chart_data=bar_chart_data, calender_data=calender_data)


@bp.route("/important", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def important():
    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, "important")
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Important",
                           notification_list=notificatons_total_list)


@bp.route("/today", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def today():
    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, "today")
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Today",
                           notification_list=notificatons_total_list)


@bp.route("/upcoming", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def upcoming():
    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, "upcoming")
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Upcoming",
                           notification_list=notificatons_total_list)


@bp.route("/timeout", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def timeout():
    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, "timeout")
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Timeout",
                           notification_list=notificatons_total_list)


@bp.route("/trash", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def trash():
    user_id, user, categories = basic_information()

    todos = TodoModel.query.filter_by(user_id=user_id, trash=1).order_by(TodoModel.id.desc()).all()
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("trash.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle="Trash Box",
                           notification_list=notificatons_total_list)



@bp.route("/category/<int:category_id>", methods=['GET', 'POST'])
@login_required
@check_category
@email_inform
def category(category_id):
    # get the name of the category
    category = CategoryModel.query.get(category_id)

    if category is None:
        return redirect(url_for("views.index"))

    category_name = category.name

    user_id, user, categories = basic_information()

    filters_name = session.get("filter")
    sort = session.get("sort")

    todos = get_all_todos(TodoModel, user_id, filters_name, sort, "index", category_id)
    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate, pagetitle=category_name,
                           category_id=category_id, notification_list=notificatons_total_list)


@bp.route("/search")
@login_required
@check_category
@email_inform
def search():
    user_id, user, categories = basic_information()

    search = request.args.get("todos")

    todos = TodoModel.query.filter_by(user_id=user_id, trash=0).filter(or_(TodoModel.assessment_name.like("%" + search + "%"),
                                                              TodoModel.module_name.like("%" + search + "%"),
                                                              TodoModel.module_code.like("%" + search + "%"),
                                                              TodoModel.due_date.like("%" + search + "%"),
                                                              TodoModel.description.like("%" + search + "%"))).all()

    # Using user id and category id to get the category name
    for todo in todos:
        category = CategoryModel.query.get(todo.category_id)
        todo.category_name = category.name
        todo.category_color = category.color

    # function: get the todos list
    todos_total_list = todos_list(todos)

    notificatons = NotificationModel.query.filter_by(user_id=user_id).all()
    notificatons_total_list = notification_list(notificatons)

    # function: fully fulfill the progress bar
    todo_sum, todo_completed, todo_rate = progress_bar(todos)

    return render_template("search.html", user=user, categories=categories, todos=todos, todos_list=todos_total_list,
                           todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate,
                           pagetitle="Search Result", notification_list=notificatons_total_list)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # encrypt
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("This email has been registered! ")
                return redirect(url_for("views.register"))
            return redirect(url_for("views.login"))
        else:
            flash("Failed: The information you entered is not valid!")
            return redirect(url_for("views.register"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['filter'] = "all"
                session['sort'] = "Duedate"
                rememverme = request.form.getlist("remember")
                if "rememberme" in rememverme:
                    session['remember'] = "true"
                else:
                    session['remember'] = "false"
                return redirect("/")
            else:
                flash("Password or email is wrong! ")
                return redirect(url_for("views.login"))
        else:
            flash("The format of email or password is wrong! ")
            return redirect(url_for("views.login"))


@bp.route("/filter", methods=["POST"])
@login_required
def filters():
    if request.method == "POST":
        filters_name = request.form.get("filters")
        session["filter"] = filters_name
        return redirect(url_for("views.index"))


@bp.route("/sort", methods=["POST"])
@login_required
def sort():
    if request.method == "POST":
        sort_name = request.form.get("sort")
        session["sort"] = sort_name
        return redirect(url_for("views.index"))


@bp.route("/add_category", methods=['POST'])
@login_required
def add_category():
    # Add a new category
    if request.method == 'POST':
        user_id = session.get("user_id")
        # Using the form to validate the data
        form1 = AddCategoryForm(request.form)
        if form1.validate():
            name = form1.module_name.data
            color = form1.module_color.data
            category = CategoryModel(name=name, user_id=user_id, color=color, create_time=datetime.now())
            try:
                db.session.add(category)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("Failed: This category has been added! ")
                return redirect(url_for("views.index"))
            contents = "Add a new category: " + name
            # save in the NotificationModel
            notification = NotificationModel(user_id=user_id, content=contents, create_time=datetime.now())
            db.session.add(notification)
            db.session.commit()
            flash("Success: Add a new category: " + name)
            return redirect(url_for('views.index'))
        else:
            flash("Failed: This category has been added! ")
            return redirect(url_for('views.index'))


@bp.route("/delete_category", methods=['POST'])
@login_required
def delete_category():
    category_id = request.form.get("category_id")
    category = CategoryModel.query.get(category_id)
    try:
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({'code': 200, 'message': 'Success'})


@bp.route("/edit_category", methods=['POST'])
@login_required
def edit_category():
    form = AddCategoryForm(request.form)
    user_id = session.get("user_id")
    if form.validate():
        name = form.module_name.data
        color = form.module_color.data
        category_id = request.form.get("category_id")
        category = CategoryModel.query.get(category_id)
        category.name = name
        category.color = color
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        contents = "Edit a category: " + name
        # save in the NotificationModel
        notification = NotificationModel(user_id=user_id, content=contents, create_time=datetime.now())
        try:
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        flash("Success: Edit a category: " + name)
        return redirect(url_for('views.index'))
    else:
        error = form.errors
        flash("Failed: " + error['module_name'][0])
        return redirect(url_for('views.index'))


@bp.route("/add_todo", methods=['POST'])
@login_required
def add_todo():
    form = AddTodoForm(request.form)
    if form.validate():
        user_id = session.get("user_id")
        module_code = form.module_code.data
        module_name = form.module_name_input.data
        assessment_title = form.assessment_title.data
        description = form.description.data
        category_id = request.form.get("category")
        due_date = request.form.get("due_date")
        important = request.form.get("important")
        mail_notifier = request.form.get("mail_notifier")
        if mail_notifier == 'mail_notifier':
            mail_notifier = 1
        else:
            mail_notifier = 0
        if important == 'important':
            important = 1
        else:
            important = 0
        # convert the date format from '2022-11-03T00:00' to '2022-11-03 00:00:00'
        due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
        todo = TodoModel(module_code=module_code, module_name=module_name, assessment_name=assessment_title,
                         description=description, category_id=category_id, due_date=due_date, important=important,
                         email_inform=mail_notifier, user_id=user_id, create_time=datetime.now(), status=0, trash=0,
                         status_email=0, status_notification=0)
        try:
            db.session.add(todo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        contents = "Add a new todo: " + assessment_title
        # save in the NotificationModel
        notification = NotificationModel(user_id=user_id, content=contents, create_time=datetime.now())
        try:
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        flash("Success: Add a new category: " + assessment_title)
        return redirect(url_for('views.index'))
    else:
        flash("Failed: " + "You have to fill in the blanks except 'description' !")
        return redirect(url_for('views.index'))


@bp.route("/completed", methods=['POST', 'GET'])
@login_required
def completed():
    todo_id = request.form.get("id")
    todo = TodoModel.query.get(todo_id)
    if todo.status == 0:
        todo.status = 1
    else:
        todo.status = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"code": 200})


@bp.route("/trash_todo", methods=['POST'])
@login_required
def trash_todo():
    todo_id = request.form.get("id")
    todo = TodoModel.query.get(todo_id)
    if todo.trash == 0:
        todo.trash = 1
    else:
        todo.trash = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"code": 200})


@bp.route("/edit_todo", methods=['POST'])
@login_required
def edit_todo():
    form = AddTodoForm(request.form)
    if form.validate():
        todo_id = request.form.get("todo_id")
        todo = TodoModel.query.get(todo_id)
        todo.module_code = form.module_code.data
        todo.module_name = form.module_name_input.data
        todo.assessment_name = form.assessment_title.data
        todo.description = form.description.data
        todo.category_id = request.form.get("category")
        todo.due_date = request.form.get("due_date")
        todo.important = request.form.get("important")
        todo.email_inform = request.form.get("mail_notifier")
        if todo.email_inform == 'mail_notifier':
            todo.email_inform = 1
        else:
            todo.email_inform = 0
        if todo.important == 'important':
            todo.important = 1
        else:
            todo.important = 0
        # convert the date format from '2022-11-03T00:00' to '2022-11-03 00:00:00'
        todo.due_date = datetime.strptime(todo.due_date, '%Y-%m-%dT%H:%M')
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        contents = "Edit a todo: " + todo.assessment_name
        # save in the NotificationModel
        notification = NotificationModel(user_id=todo.user_id, content=contents, create_time=datetime.now())
        try:
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        flash("Success: Edit a todo: " + todo.assessment_name)
        return redirect(url_for('views.index'))
    else:
        flash("Failed: " + "You have to fill in the blanks except 'description' !")
        return redirect(url_for('views.index'))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    # GET请求
    email = request.form.get("email")
    name = request.form.get("username")
    if name == "":
        name = "user"
    # 生成一个验证码
    letters = string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="[Colla] - your register code",
            recipients=[email],
            body=f"Hi, {name} ! \n\n"
                 f"You can enter this code to register into Colla: \n\n"
                 f"{captcha} \n\n"
                 f"If you weren't trying to register in, let me know."
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.creat_time = datetime.now()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "Please deliver your e-mail first! "})


@bp.route("/logout", methods=['GET'])
def logout():
    # 清楚session当中所有的数据
    session.clear()
    return redirect(url_for('views.login'))


@bp.route("/recover_todo", methods=['POST'])
@login_required
def recover_todo():
    todo_id = request.form.get("id")
    todo = TodoModel.query.get(todo_id)
    todo.trash = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"status": "success"})


@bp.route("/delete_todo", methods=['POST'])
@login_required
def delete_todo():
    todo_id = request.form.get("id")
    todo = TodoModel.query.get(todo_id)
    try:
        db.session.delete(todo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"status": "success"})


@bp.route("/clear_notification", methods=['POST'])
@login_required
def clear_notification():
    user_id = session.get("user_id")
    # delete all data in the notification table
    NotificationModel.query.filter_by(user_id=user_id).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({"status": "success"})
