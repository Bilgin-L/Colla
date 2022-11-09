# ///////////////////////////////////////////////////////////////////////////
# @file: forms.py
# @time: 2022/10/19
# @author: Yuheng Liu
# @email: sc20yl2@leeds.ac.uk && i@bilgin.top
# @organisation: University of Leeds
# @url: colla.bilgin.top
# ///////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////
# import wtforms
import wtforms
from wtforms.validators import length, email
# import models
from models import EmailCaptchaModel, UserModel, CategoryModel
# ///////////////////////////////////////////////////////////////////////////


class RegisterForm(wtforms.Form):
    """
    When user register, the form will be sent to this validator.

    username - the length of username should be between 3 and 20
    email - the format of email should be correct
    captcha - the length of captcha should be 4
    password - the length of password should be between 6 and 40

    """

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
    """
    When user login, the form will be sent to this validator.

    email - the format of email should be correct
    password - the length of password should be between 6 and 40

    """

    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=40)])


class AddCategoryForm(wtforms.Form):
    """
    When user add a category, the form will be sent to this validator.

    module_name - the length of module_name should be between 1 and 10
    module_color - the length of module_color should be between 1 and 20

    """

    module_name = wtforms.StringField(validators=[length(min=1, max=10)])
    module_color = wtforms.StringField(validators=[length(min=1, max=20)])

    def validate_module_name(self, field):
        module_name = field.data
        module_model = CategoryModel.query.filter_by(name=module_name).first()
        if module_model:
            raise wtforms.ValidationError("This category has been added! ")


class AddTodoForm(wtforms.Form):
    """
    When user add a todos, the form will be sent to this validator.

    module_code - the length of module_code should be between 1 and 10
    module_name_input - the length of module_name_input should be between 1 and 50
    assessment_title - the length of assessment_title should be between 1 and 50
    description - the length of description should be between 0 and 500

    """

    module_code = wtforms.StringField(validators=[length(min=1, max=10)])
    module_name_input = wtforms.StringField(validators=[length(min=1, max=50)])
    assessment_title = wtforms.StringField(validators=[length(min=1, max=50)])
    description = wtforms.StringField(validators=[length(min=0, max=500)])
