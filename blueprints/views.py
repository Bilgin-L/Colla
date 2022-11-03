from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g, jsonify
from models import EmailCaptchaModel, UserModel, CategoryModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mail, db
from flask_mail import Message
import string
import random
from datetime import datetime

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/")
def index():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        # Get all categories in a user
        categories = CategoryModel.query.filter_by(user_id=user_id).all()
        # get the name of the category
        default = False
        for category in categories:
            if category.name == 'Default':
                default = True
                break
        if not default:
            default_category = CategoryModel(name='Default', user_id=user_id, color='blue', create_time=datetime.now())
            db.session.add(default_category)
            db.session.commit()
        return render_template("index.html", user=user, categories=categories)
    else:
        return redirect(url_for("views.login"))


@bp.route("/delete_category", methods=['POST'])
def delete_category():
    category_id = request.form.get("category_id")
    category = CategoryModel.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Success'})


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
