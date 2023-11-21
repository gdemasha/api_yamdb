# Проект YaMDb

### Участники:
Медникова Мария
Дмитрий Котляров
Андрей Хлиманенков

## Описание:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

- Произведения делятся на категории, список категорий может быть расширен. 
- Произведению может быть присвоен жанр из списка предустановленных. 
- Добавлять произведения, категории и жанры может только администратор.
- Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка - произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
- Пользователи могут оставлять комментарии к отзывам.
- Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

По адресу [http://127.0.0.1:8000/redoc/](url) доступна документация для Проекта YaMDb.


## Установка:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:gdemasha/api_yamdb.git
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```

## Некоторые примеры запросов к API:

### Для неаутентифицированных пользователей доступен режим чтения и регистрации:

- Регистрация нового пользователя.
```
POST /api/v1/auth/signup/
```
Пример запроса:
```
{
"email": "user@example.com",
"username": "string"
}
```
- Получение JWT-токена в обмен на username и confirmation code.
```
GET /api/v1/auth/token/
```
Пример запроса:
```
{
"username": "string",
"confirmation_code": "string"
}
```
- Получить список всех категорий и жанров.
```
GET /api/v1/categories/
GET /api/v1/genres/
```
- Получение списка всех произведений и информации о произведении.
```
GET /api/v1/titles/
GET /api/v1/titles/{titles_id}/
```
- Получение списка всех отзывов и отзыва по id для указанного произведения.
```
GET /api/v1/titles/{title_id}/reviews/
GET /api/v1/titles/{title_id}/reviews/{review_id}/
```
- Получение списка всех комментариев к отзыву по id и отдельного комментария для отзыва по id.
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
- Получение списка всех пользователей и отдельного пользователя по username.
```
GET /api/v1/users/
GET /api/v1/users/{username}/
```

### Для аутентифицированных пользователей (авторизация через jwt-token):

- Добавление и удаление категории. Права доступа: Администратор.
```
POST /api/v1/categories/
DELETE /api/v1/categories/{slug}/
```
Пример POST-запроса:
```
{
"name": "string",
"slug": "string"
}
```
- Добавление и удаление жанра. Права доступа: Администратор.
```
POST /api/v1/genres/
DELETE /api/v1/genres/{slug}/
```
Пример POST-запроса:
```
{
"name": "string",
"slug": "string"
}
```
- Добавление, частичное обновление и удаление произведения. Права доступа: Администратор.
```
POST /api/v1/titles/
PATCH /api/v1/titles/{titles_id}/
DELETE /api/v1/titles/{titles_id}/
```
Пример POST-запроса:
```
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
    "string"
],
"category": "string"
}
```
- Добавление (права доступа: аутентифицированные пользователи),
  частичное обновление и удаление отзыва (права доступа: автор отзыва, модератор или администратор). 
```
POST /api/v1/titles/{title_id}/reviews/
PATCH /api/v1/titles/{titles_id}/reviews/{review_id}/
DELETE /api/v1/titles/{titles_id}/reviews/{review_id}/
```
Пример POST-запроса:
```
{
"text": "string",
"score": 1
}
```
- Добавление (права доступа: аутентифицированные пользователи),
  частичное обновление и удаление комментария к отзыву (права доступа: автор комментария, модератор или администратор).
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
PATCH /api/v1/titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
DELETE /api/v1/titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример POST-запроса:
```
{
"text": "string"
}
```
- Получение и обновление данных своей учетной записи. Права доступа: Любой авторизованный пользователь.
  Поля email и username должны быть уникальными.
```
GET /api/v1/users/me/
PATCH /api/v1/users/me/
```
Пример GET-запроса:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
- Получение списка всех пользователей. Права доступа: Администратор.
```
GET /api/v1/users/
```
Пример запроса:
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
- Добавление пользователя. Права доступа: Администратор. Поля email и username должны быть уникальными.
```
POST /api/v1/users/
```
Пример запроса:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
- Получение, изменение и удаление пользователя по username. Права доступа: Администратор.
```
GET /api/v1/users/{username}/
PATCH /api/v1/users/{username}/
DELETE /api/v1/users/{username}/
```
