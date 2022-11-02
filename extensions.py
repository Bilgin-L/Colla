from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 初始化数据库
db = SQLAlchemy()

# 绑定邮箱服务
mail = Mail()
