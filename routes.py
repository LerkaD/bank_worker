from crypt import methods
from flask import Flask, render_template, request, redirect
from database import Base, engine, insert_data
from database import add_new_person_in_database, delete_person_by_ident_num
from typing import List
from forms import RegistrationForm

app: Flask = Flask(__name__)

# # создаем таблицы
# @app.before_request
# def before_request_function():
#     Base.metadata.create_all(bind=engine)
#     insert_data()


@app.route('/')
def all_books() -> str:
    return render_template('base.html')

@app.route('/addperson', methods = ['POST'])
def add_person() -> str:
    add_form = RegistrationForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            print()
            new_person_data = {
                "f_name": request.form.get('first_name', type=str),
                "s_name": request.form.get('middle_name', type=str),
                "surname": request.form.get('last_name', type=str),
                "birthdate": request.form.get('birth_date', type=str),
                "passport_seria": request.form.get('passport_series', type=str),
                "passport_num": request.form.get('passport_number', type=str),
                "p_issued_by": request.form.get('issued_by', type=str),
                "p_issued_date": request.form.get('issue_date', type=str),
                "p_ident_num": request.form.get('identification_number', type=str),

                "address_residence": request.form.get('address_residence', type=str),
                "home_number": request.form.get('home_phone', type=str),
                "mobile_number": request.form.get('mobile_phone', type=str),
                "e_mail": request.form.get('email', type=str),
                "city": request.form.get('city_residence', type=str),
                "mat_stat": request.form.get('marital_status', type=str),
                "citizenship_name": request.form.get('citizenship', type=str),
                "disability": request.form.get('disability', type=str)
            }
            print(new_person_data)
            add_new_person_in_database(new_person_data)
            return render_template('add_person.html', form = add_form)
    return render_template('add_person.html', form = add_form)

if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
