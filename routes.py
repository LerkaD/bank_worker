from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Update

from database import init_database, check_by_p_ident_num
from database import add_new_person_in_database, delete_person_by_ident_num, get_simple_pers_info, update_person_in_database
from typing import List
from forms import RegistrationForm, CheckForm, DeleteForm, UpdateForm

app: Flask = Flask(__name__)

# @app.before_request
# def before_request_function():
#     init_database()


@app.route('/')
def start() -> str:
    return render_template('base.html')

@app.route('/persons', methods = ['GET'] )
def persons() -> str:
    print(get_simple_pers_info)
    return render_template('person_info.html', persons = get_simple_pers_info())

@app.route('/person/add', methods = ['GET', 'POST'])
def add_person() -> str:
    add_form = RegistrationForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            new_person_data = {
                "f_name": add_form.f_name.data,
                "s_name": add_form.s_name.data,
                "surname": add_form.surname.data,
                "birthdate": add_form.birth_date.data,
                "sex" : add_form.sex.data,
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
                "disability": add_form.disability.data,
                "pensioner": add_form.pensioner.data,
                "amount" : add_form.amount.data,
                "military_duty": add_form.military_duty.data
            }
            print(new_person_data)
            add_new_person_in_database(new_person_data)
            return redirect('/persons')
        else:
            print("Ошибки валидации:", add_form.errors)
            return render_template('add_person.html', form=add_form)
    return render_template('add_person.html', form = add_form)

@app.route('/person/delete', methods=['GET', 'POST'])
def delete_person()-> str:
    delete_form = DeleteForm()
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            ident_num = delete_form.p_ident_num.data
            print(check_by_p_ident_num(ident_num))
            if check_by_p_ident_num(ident_num):
                delete_person_by_ident_num(ident_num)
                return redirect('/persons')
            else:
                return render_template('delete_person.html', form=delete_form, not_found = True)
    return render_template('delete_person.html', form = delete_form, not_found = False)

@app.route('/person/update', methods=['GET', 'POST'])
def update_person_info()-> str:
    update_check_f = CheckForm()
    if request.method == 'POST':
        if update_check_f.validate_on_submit():
            ident_num = update_check_f.p_ident_num.data
            if check_by_p_ident_num(ident_num):
                return redirect(url_for('update_person_info_by_ident', ident_num=ident_num))
            else:
                return render_template('update_person.html', form=update_check_f, not_found=True)
    return render_template('update_person.html', form = update_check_f, not_found = False)

@app.route('/person/update/<string:ident_num>', methods = ['GET', 'POST'])
def update_person_info_by_ident(ident_num: str)-> str:
    update_form = UpdateForm()
    if request.method == 'POST':
        if update_form.validate_on_submit():
            update_person_data = {
                "f_name": update_form.f_name.data,
                "s_name": update_form.s_name.data,
                "surname": update_form.surname.data,
                "birthdate": update_form.birth_date.data,
                "sex": update_form.sex.data,
                "passport_seria": update_form.passport_seria.data,
                "passport_num": update_form.passport_num.data,
                "p_issued_by": update_form.p_issued_by.data,
                "p_issued_date": update_form.p_issued_date.data,
                "address_residence": update_form.address_residence.data,
                "home_number": update_form.home_number.data,
                "mobile_number": update_form.mobile_number.data,
                "e_mail": update_form.e_mail.data,
                "city": update_form.city.data,
                "mat_stat": update_form.mat_stat.data,
                "citizenship_name": update_form.citizenship.data,
                "disability": update_form.disability.data,
                "pensioner": update_form.pensioner.data,
                "amount": update_form.amount.data,
                "military_duty": update_form.military_duty.data
            }
            update_person_in_database(ident_num, update_person_data)
            return redirect('/persons')
        else:
            print("Ошибки валидации:", update_form.errors)
            return render_template('update_person_info_by_ident.html', form=update_form)
    return render_template('update_person_info_by_ident.html', form=update_form)


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
