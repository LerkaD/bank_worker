from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    BooleanField,
    SubmitField
)
from wtforms import SelectField
from wtforms.validators import DataRequired, Email, InputRequired

from wtforms import SelectMultipleField, widgets

from database import get_all_cities,get_all_citizenship, get_all_dissability, get_all_marital_status, get_mat_stat_id

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RegistrationForm(FlaskForm):
    # Данные для Person
    surname = StringField('Фамилия', validators=[DataRequired()])
    f_name = StringField('Имя', validators=[DataRequired()])
    s_name = StringField('Отчество', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    passport_seria = StringField('Серия паспорта', validators=[DataRequired()])
    passport_num = StringField('Номер паспорта', validators=[DataRequired()])
    p_issued_by = StringField('Кем выдан', validators=[DataRequired()])
    p_issued_date = DateField('Дата выдачи', format='%Y-%m-%d', validators=[DataRequired()])
    p_ident_num = StringField('Идент. номер', validators=[DataRequired()])

    # Данные для PersonContactInfo
    address_residence = StringField('Адрес проживания', validators=[DataRequired()])
    home_number = StringField('Телефон домашний')
    mobile_number = StringField('Телефон мобильный')
    e_mail = StringField('E-mail', validators=[Email()])

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

    # pensioner = BooleanField('Пенсионер', validators=[InputRequired()])
    # military_duty = CheckboxField('Военнообязанный', validators=[InputRequired()])
    submit = SubmitField('Отправить')

