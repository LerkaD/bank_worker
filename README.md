Flask-приложение для управления персональными данными и контактной информацией через веб-интерфейс. Интегрировано с базой данных через SQLAlchemy
## Основные функции
- **CRUD операции**:
  - Добавление новых записей (`/person/add`)
  - Просмотр всех записей (`/persons`)
  - Удаление записей (`/person/delete`)
  - Обновление данных (`/person/update`)
## Структура проекта
project/

├── app.py # Основной файл приложения

├── database.py # Модуль работы с базой данных

├── forms.py # Формы WTForms

├── templates/ # HTML шаблоны

│ ├── base.html

│ ├── add_person.html

│ ├── delete_person.html

│ ├── update_person.html

│ ├── update_person_info_by_ident.html

│ └── person_info.html

└── README.md


## Особенности реализации
1. **Валидация данных**:
*   `validate_surname`, `validate_f_name`, `validate_s_name`: Проверка, что поля содержат только буквы и дефис (для фамилии и имени).
*   `validate_passport_seria`, `validate_number`: Проверка, что поля содержат только цифры.
*   `validate_birth_date`: Проверка, что дата рождения не в будущем и возраст не менее 16 лет.
*   `validate_p_issued_date`: Проверка, что дата выдачи паспорта не в будущем и не раньше даты рождения.
*   `validate`: Общая валидация, проверяющая уникальность серии и номера паспорта.

2. **Безопасность**:
   - CSRF-защита отключена только для тестирования (`app.config['WTF_CSRF_ENABLED'] = False`)
   - Валидация всех входящих данных через WTForms

3. **Шаблоны**:
   - Наследование от базового шаблона `base.html`
   - Динамическое отображение ошибок валидации
   - Условные блоки для отображения статусных сообщений

  **Схема БД**:
  
Таблица Person

![image](https://github.com/user-attachments/assets/3a74f1fe-d74b-438a-a3a5-987b16aa79cc)

Уникальное ограничение:

(passport_seria, passport_num) — уникальная пара

Таблица city

![image](https://github.com/user-attachments/assets/20baeae5-dde4-4a4e-a694-501025481aa5)

Таблица marital_status

![image](https://github.com/user-attachments/assets/abec4ebc-5be3-4ccb-ad3b-d6c49d8d4950)

Таблица citizenship

![image](https://github.com/user-attachments/assets/98b84e66-fcf7-4f26-b4cc-e3a2f5122071)

Таблица disability

![image](https://github.com/user-attachments/assets/9cf5e232-854e-4254-ba20-e14f05474dfa)

Таблица person_contact_info

![image](https://github.com/user-attachments/assets/1270fe27-098c-4ca2-9d7e-7d1e09105446)


## Связи между таблицами
   - PersonContactInfo связана с:
   - Person по person_id (один к одному, каскадное удаление)
   - Cities по city_id
   - MaritalStatus по mat_stat_id
   - Citizenship по citizenship_id
   - Disability по disability_id


