from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    BooleanField,
    SubmitField,
)
from wtforms import SelectField, DecimalField
from wtforms.fields.choices import RadioField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange, Optional
from wtforms import SelectMultipleField, widgets
from database import get_all_cities, get_all_citizenship, get_all_dissability, get_all_marital_status, get_mat_stat_id, \
    check_unique_seria_num
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date
import datetime

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationForm(FlaskForm):
    # Данные для Person
    surname = StringField('Фамилия', validators=[DataRequired()])
    f_name = StringField('Имя', validators=[DataRequired()])
    s_name = StringField('Отчество', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    sex = RadioField('Пол', choices= [('м','мужской'), ('ж', 'женский')], default= 'ж', validators=[InputRequired()])
    passport_seria = StringField('Серия паспорта', validators=[DataRequired()])
    passport_num = StringField('Номер паспорта', validators=[DataRequired()])
    p_issued_by = StringField('Кем выдан', validators=[DataRequired()])
    p_issued_date = DateField('Дата выдачи', format='%Y-%m-%d', validators=[DataRequired()])
    p_ident_num = StringField('Идент. номер', validators=[DataRequired()])

    # Данные для PersonContactInfo
    address_residence = StringField('Адрес проживания', validators=[DataRequired()])
    home_number = StringField('Телефон домашний')
    mobile_number = StringField('Телефон мобильный')
    e_mail = StringField('E-mail', validators=[Email(), Optional()], default= None)

    city = SelectField('Город проживания',
                       choices=[(city.city_name, city.city_name) for city in get_all_cities()],
                       validators=[DataRequired()])

    mat_stat = SelectField('Семейное положение',
                                  choices=[(stat.id, stat.marital_type) for stat in get_all_marital_status()],
                                  validators=[DataRequired()])
    citizenship = SelectField('Гражданство',
                              choices=[(city.citizenship_name, city.citizenship_name) for city in get_all_citizenship()],
                              validators=[DataRequired()])

    disability = SelectField('Инвалидность',
                             choices=[(diss.id, diss.disability_name) for diss in get_all_dissability()],
                             validators=[DataRequired()])

    pensioner = BooleanField('Пенсионер', default= False)

    amount = DecimalField(
        'Сумма',
        validators=[Optional(), NumberRange(min=0.01, message='Минимальная сумма: 0.01')],
        places=2,
        default=None,
        widget=DecimalField.widget
    )

    military_duty = BooleanField('Военный', default= False)

    submit = SubmitField('Отправить')

    def validate_surname(self, field):
        if not field.data.replace("-", "").isalpha():
            raise ValidationError('Фамилия должна содержать только буквы и дефис')

    def validate_f_name(self, field):
        if not field.data.replace("-", "").isalpha():
            raise ValidationError('Имя должно содержать только буквы и дефис')

    def validate_s_name(self, field):
        if not field.data.isalpha():
            raise ValidationError('Отчество должно содержать только буквы')

    def validate_passport_seria(self, field):
        if field.data.isdigit():
            raise ValidationError('Серия должна содержать только цифры')

    def validate_number(self, field):
        if not field.data.isdigit():
            raise ValidationError('Номер должен содержать только цифры')

    def validate_birth_date(self, field):
        if field.data > date.today():
            raise ValidationError('Дата рождения не может быть в будущем')
        today = date.today()
        age = today.year - field.data.year

        if (today.month, today.day) < (field.data.month, field.data.day):
            age -= 1
        if age < 16:
            raise ValidationError('Возраст должен быть не менее 16 лет')

    def validate_p_issued_date(self, field):
        if field.data > datetime.date.today():
            raise ValidationError('Дата выдачи не может быть в будущем')
        if field.data < self.birth_date.data:
            raise ValidationError('Дата выдачи не может быть раньше даты рождения')

    def validate(self, extra_validators=None):
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False

        uniq_person = check_unique_seria_num(self.passport_seria.data,self.passport_num.data)
        if not uniq_person:
            self.passport_seria.errors.append('Серия и номер паспорта уже зарегистрированы')
            self.passport_num.errors.append('Серия и номер паспорта уже зарегистрированы')
            return False

        return True


class DeleteForm(FlaskForm):
    p_ident_num = StringField('Введите идентификационный номер', validators=[DataRequired()])
    submit = SubmitField('Удалить')

class CheckForm(FlaskForm):
    p_ident_num = StringField('Введите идентификационный номер', validators=[DataRequired()])
    submit = SubmitField('Обновить')


class UpdateForm(FlaskForm):
    # Данные для Person
    surname = StringField('Фамилия', validators=[DataRequired()])
    f_name = StringField('Имя', validators=[DataRequired()])
    s_name = StringField('Отчество', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    sex = RadioField('Пол', choices= [('м','мужской'), ('ж', 'женский')], default= 'ж', validators=[InputRequired()])
    passport_seria = StringField('Серия паспорта', validators=[DataRequired()])
    passport_num = StringField('Номер паспорта', validators=[DataRequired()])
    p_issued_by = StringField('Кем выдан', validators=[DataRequired()])
    p_issued_date = DateField('Дата выдачи', format='%Y-%m-%d', validators=[DataRequired()])

    # Данные для PersonContactInfo
    address_residence = StringField('Адрес проживания', validators=[DataRequired()])
    home_number = StringField('Телефон домашний')
    mobile_number = StringField('Телефон мобильный')
    e_mail = StringField('E-mail', validators=[Email(), Optional()], default= None)

    city = SelectField('Город проживания',
                       choices=[(city.city_name, city.city_name) for city in get_all_cities()],
                       validators=[DataRequired()])

    mat_stat = SelectField('Семейное положение',
                                  choices=[(stat.id, stat.marital_type) for stat in get_all_marital_status()],
                                  validators=[DataRequired()])
    citizenship = SelectField('Гражданство',
                              choices=[(city.citizenship_name, city.citizenship_name) for city in get_all_citizenship()],
                              validators=[DataRequired()])

    disability = SelectField('Инвалидность',
                             choices=[(diss.id, diss.disability_name) for diss in get_all_dissability()],
                             validators=[DataRequired()])

    pensioner = BooleanField('Пенсионер', default= False)

    amount = DecimalField(
        'Сумма',
        validators=[Optional(), NumberRange(min=0.01, message='Минимальная сумма: 0.01')],
        places=2,
        default = None
    )

    military_duty = BooleanField('Военный', default= False)

    submit = SubmitField('Обновить')

    def validate_surname(self, field):
        if not field.data.replace("-", "").isalpha():
            raise ValidationError('Фамилия должна содержать только буквы и дефис')

    def validate_f_name(self, field):
        if not field.data.replace("-", "").isalpha():
            raise ValidationError('Имя должно содержать только буквы и дефис')

    def validate_s_name(self, field):
        if not field.data.isalpha():
            raise ValidationError('Отчество должно содержать только буквы')

    def validate_passport_seria(self, field):
        if field.data.isdigit():
            raise ValidationError('Серия должна содержать только цифры')

    def validate_number(self, field):
        if not field.data.isdigit():
            raise ValidationError('Номер должен содержать только цифры')

    def validate_birth_date(self, field):
        if field.data > date.today():
            raise ValidationError('Дата рождения не может быть в будущем')
        today = date.today()
        age = today.year - field.data.year

        if (today.month, today.day) < (field.data.month, field.data.day):
            age -= 1
        if age < 16:
            raise ValidationError('Возраст должен быть не менее 16 лет')

    def validate_p_issued_date(self, field):
        if field.data > datetime.date.today():
            raise ValidationError('Дата выдачи не может быть в будущем')
        if field.data < self.birth_date.data:
            raise ValidationError('Дата выдачи не может быть раньше даты рождения')

    def validate(self, extra_validators=None):
        initial_validation = super(UpdateForm, self).validate()
        if not initial_validation:
            return False

        uniq_person = check_unique_seria_num(self.passport_seria.data,self.passport_num.data)
        if not uniq_person:
            self.passport_seria.errors.append('Серия и номер паспорта уже зарегистрированы')
            self.passport_num.errors.append('Серия и номер паспорта уже зарегистрированы')
            return False

        return True