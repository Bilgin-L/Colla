from flask import Flask
from blueprints import views_bp
import config
# from extensions import db, mail

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(views_bp)


if __name__ == '__main__':
    app.run()
