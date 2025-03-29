from sqlalchemy import create_engine, Column, ForeignKey  #
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Text, DATE
from sqlalchemy import delete
from datetime import datetime, date
from typing import List


sqlite_database = "sqlite:///database.db"
# создаем движок SqlAlchemy
engine = create_engine(sqlite_database)
# создаем класс сессии
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = 'person'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(Text, nullable=False)
    s_name = Column(Text, nullable= False)
    surname = Column(Text, nullable=False)
    birth_date = Column(DATE, nullable= False)
    passport_seria = Column(Text, nullable=False)
    passport_num = Column(Text, nullable=False)
    p_issued_by = Column(Text, nullable=False)
    p_issued_date = Column(DATE, nullable=False)
    p_ident_num = Column(Text, nullable=False, unique= True, primary_key= True)


# class Passport(Base):
#     __tablename__ = 'passport'
#
#     passport_seria = Column(Text, nullable=False)
#     passport_num = Column(Text, nullable=False)
#     p_issued_by = Column(Text, nullable=False)
#     p_issued_date = Column(DATE, nullable=False)
#     p_ident_num = Column(Text, nullable=False, unique= True, primary_key= True)
#     person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
#
    # person = relationship('Person',uselist= False, backref=backref("passport",
    #                                                 cascade="all, "
    #                                                         "delete-orphan",
    #                                                 lazy="select"))


class Cities(Base):
    __tablename__ = 'city'

    city_name = Column(Text, nullable= False, unique= True, primary_key= True)

class MaritalStatus(Base):
    __tablename__ = 'marital_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    marital_type = Column(Text, nullable=False, unique= True)

class Citizenship(Base): #гражданство
    __tablename__ = 'citizenship'

    citizenship_name = Column(Text, nullable=False, unique= True, primary_key= True)

class Disability(Base):
    __tablename__ = 'disability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    disability_name = Column(Text, nullable=False, unique= True)

class PersonContactInfo(Base):
    __tablename__ = 'person_contact_info'

    address_residence = Column(Text, nullable= False)
    home_number = Column(Text, nullable= True)
    mobile_number = Column(Text, nullable= True)
    e_mail = Column(Text, nullable= True,unique= True, primary_key= True )

    city_id = Column(Text, ForeignKey('city.city_name'), nullable=False)
    city = relationship('Cities', uselist=False, backref=backref("person_contact_info",
                                                                   lazy="select"))

    mat_stat_id = Column(Integer, ForeignKey('marital_status.id'), nullable=False)
    mat_stat = relationship('MaritalStatus', uselist=False, backref=backref("person_contact_info",
                                                                 lazy="select"))

    citizenship_id = Column(Text, ForeignKey('citizenship.citizenship_name'))
    citizenship = relationship('Citizenship', uselist=False, backref=backref("person_contact_info",
                                                                     lazy="select"))

    disability_id = Column(Integer, ForeignKey('disability.id'))
    disability = relationship('Disability', uselist=False, backref=backref("person_contact_info",
                                                                     lazy="select"))

    person_id = Column(Text, ForeignKey('person.p_ident_num'))
    person = relationship('Person',uselist= False, backref=backref("person_contact_info",
                                                    cascade="all, "
                                                            "delete-orphan",
                                                    lazy="select"))


def insert_data():
    cities_list = [
        Cities(city_name='Минск'),
        Cities(city_name='Витебск'),
        Cities(city_name='Брест'),
        Cities(city_name='Гомель'),
        Cities(city_name='Гродно'),
        Cities(city_name='Могилёв'),
        Cities(city_name='Несвиж')
    ]

    marital_status_list = [
        MaritalStatus(marital_type = 'женат/замужем'),
        MaritalStatus(marital_type='разведен/разведена'),
        MaritalStatus(marital_type='вдовец/вдова')

    ]

    citizen_list = [
        Citizenship(citizenship_name = 'Беларусь'),
        Citizenship(citizenship_name='Россия'),
        Citizenship(citizenship_name='Казахстан'),
        Citizenship(citizenship_name='Узбекистан'),
        Citizenship(citizenship_name='Молдова'),
        Citizenship(citizenship_name='Другое')

    ]

    disability_list = [
        Disability(disability_name= 'Нет'),
        Disability(disability_name = '1 группа'),
        Disability(disability_name = '2 группа'),
        Disability(disability_name= '3 группа')
    ]

    session.add_all(cities_list)
    session.add_all(marital_status_list)
    session.add_all(citizen_list)
    session.add_all(disability_list)


    session.commit()



def get_mat_stat_id(marital_type:str) -> int:
    status_id = session.query(MaritalStatus.id).filter(MaritalStatus.marital_type == marital_type).one()[0]
    return status_id

def get_disability_id(disability: str) -> int:
    disability_id = session.query(Disability.id).filter(Disability.disability_name == disability).one()[0]
    return disability_id


data_example: dict = {
    # Данные для Person
    "f_name": "Иван",
    "s_name": "Иванович",
    "surname": "Иванов",
    "birthdate": "1990-01-15",
    "passport_seria": "MP",
    "passport_num": "1234567",
    "p_issued_by": "ГУВД г. Минска",
    "p_issued_date": "2020-05-15",
    "p_ident_num": "1234567A001PB1",

    # Данные для PersonContactInfo
    "address_residence": "ул. Ленина, д. 1",
    "home_number": "80172345678",
    "mobile_number": "+375291234567",
    "e_mail": "ivanov@example.com",
    "city": 'Минск',
    "mat_stat": "женат/замужем",
    "citizenship_name": "Беларусь",
    "disability": "Нет"
}

data_example_2: dict = {
    # Данные для Person
    "f_name": "Мария",
    "s_name": "Петровна",
    "surname": "Петрова",
    "birthdate": "1985-07-22",
    "passport_seria": "КМ",
    "passport_num": "9876543",
    "p_issued_by": "ГУВД г. Гродно",
    "p_issued_date": "2015-03-10",
    "p_ident_num": "9876543B002PB2",

    # Данные для PersonContactInfo
    "address_residence": "ул. Советская, д. 45",
    "home_number": "80172345678",
    "mobile_number": "+375297654321",
    "e_mail": "petrova@example.com",
    "city": 'Гродно',
    "mat_stat": "разведен/разведена",
    "citizenship_name": "Россия",
    "disability": "1 группа"
}

def add_new_person_in_database(data:dict) -> None:
    person = Person(
        f_name = data['f_name'],
        s_name = data['s_name'],
        surname = data['surname'],
        # birth_date = datetime.strptime(data['birthdate'], "%Y-%m-%d").date(),
        birth_date = data['birthdate'],
        passport_seria=data['passport_seria'],
        passport_num = data['passport_num'],
        p_issued_by = data['p_issued_by'],
        # p_issued_date = datetime.strptime(data['p_issued_date'], "%Y-%m-%d").date(),
        p_issued_date = data['p_issued_date'],
        p_ident_num = data['p_ident_num']
    )


    # passport = Passport(
    #     passport_seria= data['passport_seria'],
    #     passport_num = data['passport_num'],
    #     p_issued_by = data['p_issued_by'],
    #     p_issued_date = data['p_issued_date'],
    #     p_ident_num = data['p_ident_num'],
    #     # person_id = get_person_id()
    # )
    session.add(person)
    session.commit()
    # print(session.query(Person).all())

    person_contact_info = PersonContactInfo(
        address_residence= data['address_residence'],
        home_number = data['home_number'],
        mobile_number = data['mobile_number'],
        e_mail =  data['e_mail'],
        city_id = data['city'],
        # mat_stat_id = get_mat_stat_id(data['mat_stat']),
        mat_stat_id= data['mat_stat'],
        citizenship_id = data['citizenship_name'],
        # disability_id = get_disability_id(data['disability']),
        disability_id= data['disability'],
        person_id = data['p_ident_num']
    )

    session.add(person_contact_info)
    session.commit()

def delete_person_by_ident_num(ident_num:str)-> None:
    person = session.query(Person).filter(Person.p_ident_num == ident_num).first()
    if person:
        session.delete(person)
        session.commit()

def update_contact_info():
    pass

def update_person_info():
    pass

def get_all_cities() -> List[Cities]:
    all_cities = session.query(Cities).all()
    return all_cities

def get_all_marital_status() -> List[MaritalStatus]:
    status_list = session.query(MaritalStatus).all()
    return status_list

def get_all_dissability() -> List[Disability]:
    d_list = session.query(Disability).all()
    return d_list

def get_all_citizenship() -> List[Citizenship]:
    citizenship_list = session.query(Citizenship)
    return citizenship_list



def get_simple_pers_info():
    info = session.query(Person).all()
    print(info)
    return info

# a = [(city.city_name, city.city_name) for city in get_all_cities()]
# print(a)
# Base.metadata.create_all(bind = engine)
# insert_data()
# add_new_person_in_database(data_example)
# add_new_person_in_database(data_example_2)
delete_person_by_ident_num('9876543B002PB2')