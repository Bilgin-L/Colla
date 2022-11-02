from flask import Flask, session, g
from blueprints import views_bp
import config
from flask_migrate import Migrate
from extensions import db, mail
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(views_bp)

# 在所有内容加载走之前会先执行这个函数
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g, "user", user)
            g.user = user
        except:
            g.user = None

# 请求来了 -》 执行before_request -> 视图函数 -> 返回模板 -》执行context_processor

# 写的所有模板都会去执行这个函数
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
