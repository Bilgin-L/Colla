from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g, jsonify
from models import EmailCaptchaModel, UserModel, CategoryModel, TodoModel
from .forms import RegisterForm, LoginForm, AddCategoryForm, AddTodoForm
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mail, db
from flask_mail import Message
import string
import random
from datetime import datetime
from decoration import login_required, check_category

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/", methods=['GET', 'POST'])
@check_category
def index():
    user_id = session.get("user_id")
    if user_id:
        # Get the user information
        user = UserModel.query.get(user_id)
        # Get all categories in a user
        categories = CategoryModel.query.filter_by(user_id=user_id).all()
        # get the name of the category
        default = False
        # detect if the user has a default category
        for category in categories:
            if category.name == 'Default':
                default = True
                break
        # if the user doesn't have a default category, create one
        if not default:
            default_category = CategoryModel(name='Default', user_id=user_id, color='blue', create_time=datetime.now())
            db.session.add(default_category)
            db.session.commit()
            return redirect(url_for('views.index'))

        # Add a new category
        if request.method == 'POST':
            # Using the form to validate the data
            form1 = AddCategoryForm(request.form)
            if form1.validate():
                name = form1.module_name.data
                color = form1.module_color.data
                category = CategoryModel(name=name, user_id=user_id, color=color, create_time=datetime.now())
                db.session.add(category)
                db.session.commit()
                flash("Success: Add a new category successfully!")
                return redirect(url_for('views.index'))
            else:
                error = form1.errors
                flash("Failed: " + error['module_name'][0])
                return redirect(url_for('views.index'))

        # Get all todos which 'trash' == 0 in a user, and sort them by 'status' and 'due_date'
        todos = TodoModel.query.filter_by(user_id=user_id, trash=0).order_by(TodoModel.status,
                                                                             TodoModel.due_date).all()
        # Using user id and category id to get the category name
        for todo in todos:
            category = CategoryModel.query.get(todo.category_id)
            todo.category_name = category.name
            todo.category_color = category.color

        todos_list = []
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
            todos_list.append(data)
            data = []
        # print(todos_list)

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

        return render_template("index.html", user=user, categories=categories, todos=todos, todos_list=todos_list,
                               todo_sum=todo_sum, completed_sum=todo_completed, todo_rate=todo_rate)
    else:
        return redirect(url_for("views.login"))


@bp.route("/delete_category", methods=['POST'])
@login_required
def delete_category():
    category_id = request.form.get("category_id")
    category = CategoryModel.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Success'})


@bp.route("/edit_category", methods=['POST'])
@login_required
def edit_category():
    form = AddCategoryForm(request.form)
    if form.validate():
        name = form.module_name.data
        color = form.module_color.data
        category_id = request.form.get("category_id")
        category = CategoryModel.query.get(category_id)
        category.name = name
        category.color = color
        db.session.commit()
        flash("Success: Edit successfully!")
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
        db.session.add(todo)
        db.session.commit()
        flash("Success: Add a new todo successfully!")
        return redirect(url_for('views.index'))
    else:
        # flash("Failed: " + error['module_code'][0])
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
    db.session.commit()
    # code:200说明是一个成功的正常的请求
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
    db.session.commit()
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
        db.session.commit()
        flash("Success: Edit successfully!")
        return redirect(url_for('views.index'))
    else:
        flash("Failed: " + "You have to fill in the blanks except 'description' !")
        return redirect(url_for('views.index'))


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
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("views.login"))
        else:
            flash("Failed: The information you entered is not valid!")
            return redirect(url_for("views.register"))


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
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        # code:200说明是一个成功的正常的请求
        return jsonify({"code": 200})
    else:
        # code:400 客户端错误
        return jsonify({"code": 400, "message": "Please deliver your e-mail first! "})


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


@bp.route("/logout", methods=['GET'])
def logout():
    # 清楚session当中所有的数据
    session.clear()
    return redirect(url_for('views.login'))
