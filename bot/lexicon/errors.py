from dataclasses import dataclass
from enum import Enum


class RegisterDialogErrors:
    invalid_username = 'Вы ввели некорректное имя!'
    user_exist = 'У вас уже есть аккаунт! Вы можете удалить его и создать новый или отредактировать'
    invalid_age = 'Вы ввели некорректный возраст'
    invalid_city = 'Такого города не существует'
    invalid_photo = 'Вы отправили некорректный файл'
    invalid_description = 'Расскажите подробнее о себе(минимум бы 100 символов)'
