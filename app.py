from flask import Flask
from blueprints import views_bp
import config
from flask_migrate import Migrate
from extensions import db, mail

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(views_bp)


if __name__ == '__main__':
    app.run()
