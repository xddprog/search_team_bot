# Search team and teammate bot 🤝

Часто начинающим или опытным разработчикам хочется найти человека или команду для совместного пет-проекта, возможно даже для стартапа. 
Данный бот поможет в поиске команды или друга-программиста

![image](https://github.com/user-attachments/assets/6981a9ac-108f-4ad9-a189-94584cd5ecbf)

## Установка
Бот имеет простую установку и запуск с помощью Docker
1. **Клонирование репозитория**
 
    ```
    git clone https://github.com/xddprog/search_team_bot.git
    ```
2. **Установка токена telegram бота в docker-compose файл**
    ```
    BOT_TOKEN="ваш токен бота"
    ```
3. **Сборка и запуск docker-compose через консоль**
    ```
    docker-compose up
    ```
## Внешние API
1. **Nominatim**

   Используется для определения существования города пользователя при регистрации/редактировании профиля. Является бесплатным API 

## Команды
Бот имеет лишь 1 команду, ведь все взаимодействие с ним происходит через меню

1. **Открыть меню**

    ```
    /start
    ```
## Возможности бота
1. **Регистрация, редактирование, удаление и просмотр профиля**

2. **Создание, просмотр, администрирование и удаление команды**

3. **Приглашение в команду по ссылке**

4. **Поиск друга**

5. **Поиск команды**
