from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register")
def register():
    return render_template("register.html")