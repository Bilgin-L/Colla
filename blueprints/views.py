from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")
