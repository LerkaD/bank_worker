from sqlalchemy import create_engine, Column, ForeignKey, Boolean, Float  #
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Text, DATE, inspect
from typing import List
from data_example import person_list
from sqlalchemy import UniqueConstraint

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
    sex = Column(Text, nullable= False, default= 'ж')
    passport_seria = Column(Text, nullable=False)
    passport_num = Column(Text, nullable=False)
    p_issued_by = Column(Text, nullable=False)
    p_issued_date = Column(DATE, nullable=False)
    p_ident_num = Column(Text, nullable=False, unique= True, primary_key= True)

    __table_args__ = (
        UniqueConstraint('passport_seria', 'passport_num', name='unique_passport'),
    )

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

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_residence = Column(Text, nullable= False)
    home_number = Column(Text, nullable= True)
    mobile_number = Column(Text, nullable= True)
    e_mail = Column(Text, nullable= True )
    pensioner = Column(Boolean, nullable=False, default=False)
    military_duty = Column(Boolean, nullable=False, default=False)
    amount = Column(Float, nullable=True, default= None)

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
        MaritalStatus(marital_type='не женат/не замужем'),
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

def check_tables():
    inspector = inspect(engine)
    return bool(inspector.get_table_names())

def init_database():
    if not check_tables():
        Base.metadata.create_all(bind=engine)
        insert_data()

def get_mat_stat_id(marital_type:str) -> int:
    status_id = session.query(MaritalStatus.id).filter(MaritalStatus.marital_type == marital_type).one()[0]
    return status_id

def get_disability_id(disability: str) -> int:
    disability_id = session.query(Disability.id).filter(Disability.disability_name == disability).one()[0]
    return disability_id

def add_new_person_in_database(data:dict) -> None:
    person = Person(
        f_name = data['f_name'],
        s_name = data['s_name'],
        surname = data['surname'],
        birth_date = data['birthdate'],
        sex = data['sex'],
        passport_seria=data['passport_seria'],
        passport_num = data['passport_num'],
        p_issued_by = data['p_issued_by'],
        p_issued_date = data['p_issued_date'],
        p_ident_num = data['p_ident_num']
    )

    person_contact_info = PersonContactInfo(
        address_residence= data['address_residence'],
        home_number = data['home_number'],
        mobile_number = data['mobile_number'],
        e_mail =  data['e_mail'],
        pensioner=data['pensioner'],
        military_duty=data['military_duty'],
        amount=data['amount'],
        city_id = data['city'],
        mat_stat_id= data['mat_stat'],
        citizenship_id = data['citizenship_name'],
        disability_id= data['disability'],
        person_id = data['p_ident_num']
    )

    session.add(person)
    session.add(person_contact_info)
    session.commit()


def check_by_p_ident_num(ident_num:str) -> bool:
    person = session.query(Person).filter(Person.p_ident_num == ident_num).first()
    if person:
        return True

def delete_person_by_ident_num(ident_num:str)-> None:
    person = session.query(Person).filter(Person.p_ident_num == ident_num).first()
    session.delete(person)
    session.commit()


def update_person_in_database(ident_num:str, data:dict )-> None:
    person = session.query(Person).filter_by(p_ident_num=ident_num).first()
    person.f_name = data['f_name']
    person.s_name = data['s_name']
    person.surname = data['surname']
    person.birth_date = data['birthdate']
    person.sex = data['sex']
    person.passport_seria = data['passport_seria']
    person.passport_num = data['passport_num']
    person.p_issued_by = data['p_issued_by']
    person.p_issued_date = data['p_issued_date']

    person_info = session.query(PersonContactInfo).filter_by(person_id = ident_num).first()
    person_info.address_residence = data['address_residence']
    if data['home_number']:
        person_info.home_number = data['home_number']
    if data['mobile_number']:
        person_info.mobile_number = data['mobile_number']
    if data['e_mail']:
        person_info.e_mail = data['e_mail']
    person_info.pensioner = data['pensioner']
    person_info.military_duty = data['military_duty']
    if data['amount']:
        person_info.amount = data['amount']
    person_info.city_id = data['city']
    person_info.mat_stat_id = data['mat_stat']
    person_info.citizenship_id = data['citizenship_name']
    person_info.disability_id = data['disability']

    session.commit()

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
    return info

# Base.metadata.create_all(bind=engine)
# insert_data()
# for pers in person_list:
#     add_new_person_in_database(pers)
