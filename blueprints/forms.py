import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel, CategoryModel


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=40)])

    # Check whether captcha correct
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha != captcha:
            raise wtforms.ValidationError("Captcha Error! ")

    # Check whether email exit
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("This email has been registered! ")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=3, max=20)])


class AddCategoryForm(wtforms.Form):
    module_name = wtforms.StringField(validators=[length(min=1, max=10)])
    module_color = wtforms.StringField(validators=[length(min=1, max=20)])

    def validate_module_name(self, field):
        module_name = field.data
        module_model = CategoryModel.query.filter_by(name=module_name).first()
        if module_model:
            raise wtforms.ValidationError("This category has been added! ")


class AddTodoForm(wtforms.Form):
    module_code = wtforms.StringField(validators=[length(min=1, max=10)])
    module_name_input = wtforms.StringField(validators=[length(min=1, max=50)])
    assessment_title = wtforms.StringField(validators=[length(min=1, max=50)])
    description = wtforms.StringField(validators=[length(min=0, max=500)])
