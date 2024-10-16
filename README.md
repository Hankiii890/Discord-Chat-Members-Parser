# Бот discord для парсинга участников проекта

## Обзор
Это бот Discord, который парсит участников из списка проектов и хранит данные в базе данных, а так же создает csv файл с данными при запуске скрипта.
Бот использует API Discord для получения членов сервера Discord и библиотеку dotenv для загрузки переменных окружения.


### Переменные окружения

Создайте файл .env в корневом каталоге проекта с следующими переменными:

DISCORD_TOKEN: Токен вашего бота Discord

DB_HOST: Хост вашей БД

DB_NAME: Название БД

DB_USER: Имя пользователя для доступа к БД

DB_PASSWORD: Пароль самой БД

### База данных
Создайте базу данных PostgreSQL и обновите файл database.py с вашими учетными данными базы данных.

### Запуск бота
1. Установите необходимые пакеты, запустив pip install -r requirements.txt
2. Запустите бота, выполнив python bot.py

### Команды
Бот отвечает на следующие команды:

!start_parsing: Начинает процесс парсинга для всех проектов в БД


### Как это работает
Бот подключается к API Discord с помощью предоставленного токена.
Когда команда !start_parsing получена, бот получает список проектов из базы данных.
Для каждого проекта бот получает ссылку на приглашение Discord и использует ее для получения членов соответствующего сервера Discord.
Бот затем хранит данные о членах в базе данных, включая имя проекта, логин члена и роль.

## Примечание
Этот бот требует включения intent'ов members и message_content в панели разработчика Discord !

# Не забудьте добавить файл .env в файл .gitignore, чтобы предотвратить утечку конфиденциальных данных в репозиторий.