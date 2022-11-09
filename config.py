# ///////////////////////////////////////////////////////////////////////////
# @file: config.py
# @time: 2022/10/19
# @author: Yuheng Liu
# @email: sc20yl2@leeds.ac.uk && i@bilgin.top
# @organisation: University of Leeds
# @url: colla.bilgin.top
# ///////////////////////////////////////////////////////////////////////////

# link to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Key information
SECRET_KEY = "CGBHGCYTGYIHUONHGVTGYHUBHJG"

# mail server
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "2964992240@qq.com"
MAIL_PASSWORD = "lvnbpinsuqcvdgcb"
MAIL_DEFAULT_SENDER = "2964992240@qq.com"
