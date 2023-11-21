"""Константы для проекта."""

# Максимальная длина био
MAX_LENGTH_TEXT = 254

# Максимальная длина name произведения/категории/жанра
MAX_LENGTH_NAME = 256

# Максимальная длина slug категории/жанра
MAX_LENGTH_SLUG = 50

# Максимальная длина email
MAX_LENGTH_EMAIL = 254

# Максимальная длина username
MAX_LENGTH_USERNAME = 150

# Максимальная длина role
MAX_LENGTH_ROLE = 9

# Выбор пользователя
ROLE_CHOICE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

# Почта для отправки кодов
SEND_CODE_EMAIL = 'testapi21331@mail.ru'
