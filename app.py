# ///////////////////////////////////////////////////////////////////////////
# @file: app.py
# @time: 2022/10/19
# @author: Yuheng Liu
# @email: sc20yl2@leeds.ac.uk && i@bilgin.top
# @organisation: University of Leeds
# @url: colla.bilgin.top
# ///////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////
# import flask
from flask import Flask, session, g
# import blueprints
from blueprints import views_bp
# import config
import config
# import database
from flask_migrate import Migrate
from models import UserModel
# import extensions
from extensions import db, mail
# ///////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////
# init app
app = Flask(__name__)
app.config.from_object(config)

# init database
db.init_app(app)

# init mail
mail.init_app(app)

# init migrate
migrate = Migrate(app, db)

# register blueprints
app.register_blueprint(views_bp)
# ///////////////////////////////////////////////////////////////////////////


@app.before_request
def before_request():
    """
    This function will be executed before all requests.

    """

    # get user id from session
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # bind user to g
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    """
    This function will be executed before all templates.

    :return: user

    """

    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
