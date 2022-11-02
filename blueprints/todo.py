from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from extensions import db, mail
from sqlalchemy import or_

bp = Blueprint("todo", __name__, url_prefix="/todo")
