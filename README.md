# gazprominfo testtask

# Задание
Развернуть веб-приложение на Django с общедоступными микросервисами
Микросервис 1 принимает запрос через url следующей структуры:
…/service1/{ключ}&{данные}
{ключ} – проверка ключа (123456789) для выполнения запроса
{данные} – url-адрес интересующей страницы.
Пользователю возвращается список найденных на странице адресов эл.почт в формате json.
Найденные адреса эл.почт записываются в таблицу в SQLite (url-адрес|адрес  эл.почты)
Микросервис 2 принимает запрос через url следующей структуры: …/service2/{ключ}&{данные}
{ключ} – проверка ключа (123456789) для выполнения запроса
{данные} – адрес эл.почты
Если указанный в запросе адрес эл.почты присутствует в базе, пользователю возвращается список url-адресов страниц, где ранее были найдены данные адреса эл.почт.

# Запуск
## Подготовка
1. Создать файл .env с следующим наполнением:
- SECRET_KEY - Секретный ключ django. (Подброное поисание см документацию). Пример django-insecure-3z%b3rf1a8ob5xklms25z+g6fsvk=-wpj*#*=+jr#3tvgw0#0&
- GETPARAMETER_TOKEN - Токен который будет требоваться в качестве гет параметра token при каждом запросе. Значение по умолчанию 123456789.
Собрать контейнер
2. Собрать контейнер:  
`docker build -t gazprominfo .` (gazprominfo - имя образа, можно поставить произвольное)
# Запуск контейнера
`docker run --rm --env-file ./.env --volume ./gazprominfo/storage/:/code/gazprominfo/storage -p 8000:8000 --name gazprominfo_1 gazprominfo`
# Запуск тестов
`docker exec  gazprominfo_1 /bin/bash -c " cd ./gazprominfo && pytest -v"`
# Запуск миграции ***обязательно при первом запуске, это создаст новую бд в ./gazprominfo/storage/***
`docker exec  gazprominfo_1 /bin/bash -c "cd ./gazprominfo && python manage.py migrate"`

# Доступные методы
### Роут
- GET /services/service1
### Параметры
- token - см GETPARAMETER_TOKEN
- url-to-parse - страница для парсинга
### Пример cURL
`curl --location --request GET 'localhost:8000/services/service1?token=10987654321&url-to-parse=https://www.gazprom.ru/contacts/'`

### Роут
- GET /services/service2
### Параметры
- token - см GETPARAMETER_TOKEN
- email - email по которому будет произведен поиск в бд
### Пример cURL
`curl --location --request GET 'localhost:8000/services/service2?token=123456789&email=gazprom@gazprom.ru'`
