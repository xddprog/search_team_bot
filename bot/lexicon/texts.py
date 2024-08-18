class ProfileAndTeamItemsTexts:
    username = 'Имя'
    name = 'Название команды'
    city = 'Город'
    sex = 'Пол'
    description = 'Описание'
    photo = 'Фото'
    age = 'Возраст'
    languages = 'Языки программирования'


class BaseInputTexts:
    username = 'Введите имя'
    name = 'Введите название команды'
    age = 'Введите возраст'
    sex = 'Выберите пол'
    city = 'Введите город'
    languages = 'Выберите языки программирования'
    user_description = 'Расскажите о себе'
    team_description = 'Расскажите подробнее о команде'
    photo = 'Загрузите фото профиля'


class StartDialogTexts(BaseInputTexts):
    username = 'Привет! Для начала работы бота нужно пройти регистрацию. Введите свое имя'
    success = ('Вы успешно зарегистрировались! Вот ваш профиль:\n '
               '<b>Имя</b>: {username}\n<b>Возраст</b>: {age}\n<b>Пол</b>: {sex}\n'
               '<b>Город</b>: {city}\n<b>Описание</b>: {user_description}\n<b>Языки</b>: {languages}')


class MainMenuTexts:
    main = 'Вы находитесь в главном меню'


class ProfileTexts:
    profile = ('<b>Имя</b>: {username}\n<b>Возраст</b>: {age}\n<b>Пол</b>: {sex}\n'
               '<b>Город</b>: {city}\n<b>Описание</b>: {user_description}\n<b>Языки</b>: {languages}')


class DeleteProfileTexts:
    delete = 'Вы точно хотите удалить профиль? Профиль будет полностью удален без возможности восстановления!'
    accept = 'Вы успешно удалили профиль!'


class EditProfileTexts(BaseInputTexts):
    main = ('Выберите пункт профиля, который хотите отредактировать.'
            'Вы можете отредактировать сразу несколько пунктов.\n\n'
            'Измененные пункты:\n{editable_data}')


class EditTeamTexts(BaseInputTexts):
    main = ('Выберите пункт профиля команды, который хотите отредактировать.'
            ' Вы можете отредактировать сразу несколько пунктов.\n\n'
            'Измененные пункты:\n {editable_data}')


class TeamTexts:
    team = '<b>Название команды</b>: {name}\n<b>Описание</b>: {team_description}\n<b>Языки</b>: {languages}'
    teams = '<b>Количество команд, в которых вы находитесь</b>: {teams_numbers}\n Максимальное число команд - 10'
    success = ('Вы успешно создали команду!\n<b>Название команды</b>: {name}\n'
               '<b>Описание</b>: {team_description}\n<b>Языки</b>: {languages}')
    invite_link = '<b>Ссылка для приглашения в команду</b>: {invite_to_team_link}'
    users = '<b>Количество участников в команде</b>: {team_users_number}\nВы можете посмотреть профиль любого участника'


class AcceptToInviteTeamDialogs:
    invite = "Вас пригласили в команду: {team_name}"
    success_accept_invite_to_team = "Теперь вы являетесь участником команды: {team_name}"
    accept_invite_error = 'Вы не можете вступить в команду, так как уже находитесь в 10 командах!'


class DeleteTeamTexts:
    delete = 'Вы уверены, что хотите удалить команду?'
    accept = 'Вы успешно удалили команду!'
    message_to_user_deleted_team = 'Команда {} была удалена!\nСвязаться с создателем: '


class RemoveTeamUserTexts:
    remove = 'Вы уверены, что хотите исключить участника из команды?'
    accept = 'Участник был успешно исключен из команды!'
    message_to_user_after_remove = 'Вы были исключены из команды {}\nСвязаться с создателем: '


class SearchTexts:
    send_message_to_liked_user = (
        'Ваш профиль понравился пользователю\n' + ProfileTexts.profile
    )
    send_message_to_liked_team = (
        'Пользователь хочет вступить в команду:{name}\n' + ProfileTexts.profile
    )
    users_ended = 'Вы просмотрели всех пользователей!'
    teams_ended = 'Вы просмторели все команды!'
    accept_user_to_team = 'Вы были приняты в команду {}'
