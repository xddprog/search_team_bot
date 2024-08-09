class ProfileItemsTexts:
    username = 'Имя'
    city = 'Город'
    sex = 'Пол'
    description = 'Описание'
    photo = 'Фото'
    age = 'Возраст'
    languages = 'Языки программирования'


class BaseProfileInputTexts:
    username = 'Введите свое имя'
    age = 'Введите свой возраст'
    sex = 'Выберите пол'
    city = 'Введите свой город'
    languages = 'Выберите языки программирования'
    description = 'Расскажите о себе'
    photo = 'Загрузите фото профиля'


class StartDialogTexts(BaseProfileInputTexts):
    username = 'Привет! Для начала работы бота нужно пройти регистрацию. Введите свое имя'
    success = ('Вы успешно зарегистрировались! Вот ваш профиль:\n '
               '<b>Имя</b>: {username}\n<b>Возраст</b>: {age}\n<b>Пол</b>: {sex}\n'
               '<b>Город</b>: {city}\n<b>Описание</b>: {description}\n<b>Языки</b>: {languages}')


class MainMenuTexts:
    main = 'Вы находитесь в главном меню'


class ProfileTexts:
    profile = ('<b>Имя</b>: {username}\n<b>Возраст</b>: {age}\n<b>Пол</b>: {sex}\n'
               '<b>Город</b>: {city}\n<b>Описание</b>: {description}\n<b>Языки</b>: {languages}')


class DeleteProfileTexts:
    delete = 'Вы точно хотите удалить профиль? Профиль будет полностью удален без возможности восстановления!'
    accept = 'Вы успешно удалили профиль!'


class EditProfileTexts(BaseProfileInputTexts):
    main = ('Выберите пункт профиля, который хотите отредактировать.'
            ' Вы можете отредактировать сразу несколько пунктов.\n\n'
            'Измененные пункты:\n {editable_data}')