from flask import Flask, render_template, request, redirect
from database import Base, engine, insert_data
from database import add_new_person_in_database, delete_person_by_ident_num, get_simple_pers_info
from typing import List
from forms import RegistrationForm

app: Flask = Flask(__name__)

# # создаем таблицы
# @app.before_request
# def before_request_function():
#     Base.metadata.create_all(bind=engine)
#     insert_data()


@app.route('/')
def start() -> str:
    return render_template('base.html')

@app.route('/persons', methods = ['GET'] )
def all_persons() -> str:
    print(get_simple_pers_info)
    return render_template('person_info.html', persons = get_simple_pers_info())

@app.route('/addperson', methods = ['GET', 'POST'])
def add_person() -> str:
    add_form = RegistrationForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            new_person_data = {
                "f_name": add_form.f_name.data,
                "s_name": add_form.s_name.data,
                "surname": add_form.surname.data,
                "birthdate": add_form.birth_date.data,
                "passport_seria": add_form.passport_seria.data,
                "passport_num": add_form.passport_num.data,
                "p_issued_by": add_form.p_issued_by.data,
                "p_issued_date": add_form.p_issued_date.data,
                "p_ident_num": add_form.p_ident_num.data,
                "address_residence": add_form.address_residence.data,
                "home_number": add_form.home_number.data,
                "mobile_number": add_form.mobile_number.data,
                "e_mail": add_form.e_mail.data,
                "city": add_form.city.data,
                "mat_stat": add_form.mat_stat.data,
                "citizenship_name": add_form.citizenship.data,
                "disability": add_form.disability.data
            }
            print(new_person_data)
            add_new_person_in_database(new_person_data)
            return redirect('/persons')
    return render_template('add_person.html', form = add_form)

if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
