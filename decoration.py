from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    # 这个@wrap装饰器一定不要忘记写了
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("views.login"))
    return wrapper
