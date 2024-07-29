# Дипломная работа "Проект самообучения"

Проект представляет собой backend часть платформы для самообучения студентов.

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/SerjMonstrX/diplom_self-education.git
    ```
2. Установите зависимости, используя Poetry:
       poetry install

3. Настройте PostgreSQL:
Создайте базу данных PostgreSQL, внесите настройки для БД в .env

4. Примените миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

## Структура

Приложение courses содержит модели для разделов и материалов, для управления реализован механизм CRUD.

Пример создания раздела:

        section_data_1 = {
            'title': 'New Section',
            'description': 'This is a test section',
            'is_public': True
        }

        material_data_1= {
            'section': section.id, #id раздела, для которого будет созданы материалы
            'title': 'New Material',
            'content': 'This is new content',
            'is_public': True
        }
Приложение users содержит реализацию модели юзера, для управления реализован механизм CRUD, 
для регистрации используется email и пароль.

        user_data_1= {
         "email": "user@example.com",
          "password": "password123",
        }

Приложение exams содержит реализацию тестов.
        
После создания модели exam

        exam_data = {
            'title': 'New Exam 2',
            'description': 'This is a new exam 2',
            'material': material.id, #id материала, для которого будет создан экзамен(тест)
            'is_public': True
        }

Можно добавлять вопросы и ответы для тестов.
    
        question_data = {
            'exam': exam.id', #id экзамена(теста)
            'text': 'This is a new exam 2',
            'is_multiple_choice': False, #для реализации выбора нескольких ответов
            'is_public': True
        }

        answer_data = {
            'question': question.id', #id вопроса
            'text': 'answer text',
            'is_correct': True #пометка для правильного ответа
        }

## Документация
Для проекта настроен вывод документации через swagger или redoc

      http://127.0.0.1:8000/swagger/

      http://127.0.0.1:8000/redoc/


