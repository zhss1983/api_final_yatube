# Документация к API Yatube (v1)

## Как запустить проект:

Если вы собираетесь работать из командной строки в **windows**, вам может
 потребоваться Bash. скачать его можно по ссылке:
 [GitBash](https://gitforwindows.org/) ([Git-2.33.0.2-64-bit.exe](https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe)).

Так же при работе в **windows** необходимо использовать **python** вместо
 **python3**

Последнюю версию **python** ищите на официальном сайте
 [https://www.python.org/](https://www.python.org/downloads/)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/zhss1983/api_final_yatube
```

```
cd api_final_yatube
```

Создать и активировать виртуальное окружение:

```
python -m venv env
```

- linux
>```
>source env/bin/activate
>```
- windows
>```
>source env/Scripts/activate
>```

Установить зависимости из файла **requirements.txt**:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в подкаталог yatube_api и выполнить миграции:

```
cd yatube_api
python manage.py migrate
```

Создать администратора (суперпользователя) БД:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

## Работа с эндпоинтами:

### Работа с публикациями:

**Чтение** доступно *всем пользователям* без исключения, **добавлять** новые 
 записи смогут только *зарегистрированные пользователи*, а **изменять** или
 **удалять** записи смогут только *авторы* этих записей. 

#### Получение публикаций

Получить список всех публикаций. При указании параметров **limit** и **offset**
 результаты будут переданы постранично.

GET: [/api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)

Ответ, статус код 200:

```JSON
[
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2019-08-24T14:15:22Z",
      "image": "string",
      "group": 0
    }
]
```


Параметры передаваемые в запрос:
>**limit**: тип integer, целое положительное число. Соответствует количеству 
> публикаций, выводимых на одну страницу.
>
>**offset**: тип integer, целое положительное число. Номер страницы после
> которой начинать выдачу.

GET: [/api/v1/posts/?offset=400&limit=100](http://127.0.0.1:8000/api/v1/posts/?offset=300&limit=100)

Ответ, статус код 200:

```JSON
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2019-08-24T14:15:22Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

#### Получение одной конкретной публикации

Получить конкретную публикацию возможно используя её **id**.

Параметр пути, передаваемый в GET запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.

GET: api/v1/posts/{id}/

GET: [api/v1/posts/0/](http://127.0.0.1:8000/api/v1/posts/0/)

Ответ, статус код 200:

```JSON
[
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2019-08-24T14:15:22Z",
      "image": "string",
      "group": 0
    }
]
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Создание публикации

Добавление новой публикации в коллекцию публикаций. Анонимные запросы
 запрещены. Для добавления необходимо отправить **POST** запрос, содержащий
 **JSON**.

Параметры **JSON** запроса:
>**text**: тип string, обязательное текстовое поле. Содержит текст публикации.
>
>**image**: не обязательное поле, содержит в себе загружаемый файл или null. 
>
>**group**: тип integer, не обязательное поле целое положительное число или null. Соответствует уникальному 
> идентификатору сообщества.

**JSON** запрос:

```JSON
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

POST: [/api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)

Ответ, статус код 201:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

Ответ, статус код 400:

```JSON
{
  "text": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

####Обновление публикации

Обновление публикации по **id**. Обновить публикацию может только автор
 публикации. Анонимные запросы запрещены.

Параметр пути, передаваемый в **PUT** запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.

Параметры **JSON** запроса:
>**text**: тип string, обязательное текстовое поле. Содержит текст публикации.
>
>**image**: не обязательное поле, содержит в себе загружаемый файл или null. 
>
>**group**: тип integer, не обязательное поле целое положительное число или
> null. Соответствует уникальному идентификатору сообщества.

**JSON** запрос:

```JSON
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

PUT: /api/v1/posts/{id}/

PUT: [http://127.0.0.1:8000/api/v1/posts/0/](http://127.0.0.1:8000/api/v1/posts/0/)

Ответ, статус код 200:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

Ответ, статус код 400:

```JSON
{
  "text": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

Для частичного обновления воспользуйтесь методом **PATCH** с теми же
 параметрами.
 
Ответ, статус код 200:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
 
Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Удаление публикации

Удалить публикацию может только автор публикации по **id**. Анонимные
 запросы запрещены.

Параметр пути, передаваемый в **DELETE** запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.

DELETE: /api/v1/posts/{id}/

DELETE: [http://127.0.0.1:8000/api/v1/posts/0/](http://127.0.0.1:8000/api/v1/posts/0/)

Ответ, статус код 204:

```JSON
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

### Работа с комментариями:

**Чтение** доступно *всем пользователям* без исключения, **добавлять** новые 
 комментарии смогут только *зарегистрированные пользователи*, а **изменять**
 или **удалять** комментарии смогут только *авторы* этих записей. 

#### Получение комментариев

Получить список комментариев к конкретной публикации возможно используя её
 **id**.

Параметр пути, передаваемый в **GET** запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.

GET: /api/v1/posts/{id}/comments/

GET: [/api/v1/posts/0/comments/](http://127.0.0.1:8000/api/v1/posts/0/comments/)

Ответ, статус код 200:

```JSON
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Получение одного конкретного комментария к публикации

Получить комментарий для конкретной публикации возможно используя **id**
 публикации (**post_id**) и **id** комментария.

Параметр пути, передаваемый в **GET** запросе:
>**post_id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.
>
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору комментария.

GET: /api/v1/posts/{post_id}/comments/{id}/

GET: [/api/v1/posts/0/comments/0/](http://127.0.0.1:8000/api/v1/posts/0/comments/0/)

Ответ, статус код 200:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Создание комментария

Добавление нового комментария к публикации. Анонимные запросы
 запрещены. Для добавления необходимо отправить **POST** запрос, содержащий
 **JSON**.

Параметр пути, передаваемый в **POST** запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору публикации.

Параметры **JSON** запроса:
>**text**: тип string, обязательное текстовое поле. Содержит текст комментария.

**JSON** запрос:

```JSON
{
  "text": "string"
}
```

POST: /api/v1/posts/{id}/comments/

POST: [/api/v1/posts/0/comments/](http://127.0.0.1:8000/api/v1/posts/0/comments/)

Ответ, статус код 201:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

Ответ, статус код 400:

```JSON
{
  "text": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Обновление комментария

Обновление комментария по **id** для конкретного поста с **post_id**.
 Обновить комментарий может только автор комментария. Анонимные запросы
 запрещены.

Параметры пути, передаваемые в **PUT** запросе:
>**post_id**: тип integer, целое положительное число. Соответствует уникальному
> идентификатору публикации.
>
>**id**: тип integer, целое положительное число. Соответствует уникальному
> идентификатору комментария.

Параметры **JSON** запроса:
>**text**: тип string, обязательное текстовое поле. Содержит текст комментария.

**JSON** запрос:

```JSON
{
  "text": "string"
}
```

PUT: /api/v1/posts/{post_id}/comments/{id}/

PUT: [/api/v1/posts/0/comments/0/](http://127.0.0.1:8000/api/v1/posts/0/comments/0/)

Ответ, статус код 200:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

Ответ, статус код 400:

```JSON
{
  "text": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

Для частичного обновления воспользуйтесь методом **PATCH** с теми же
 параметрами.

Ответ, статус код 200:

```JSON
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

#### Удаление комментария

Удалить комментарий к публикации может только автор комментария по его **id**
 и по **post_id** публикации. Анонимные запросы запрещены.

Параметр пути, передаваемый в **DELETE** запросе:
>**post_id**: тип integer, целое положительное число. Соответствует уникальному
> идентификатору публикации.
>
>**id**: тип integer, целое положительное число. Соответствует уникальному
> идентификатору комментария.

DELETE: /api/v1/posts/{post_id}/comments/{id}/

DELETE: [http://127.0.0.1:8000/api/v1/posts/0/comments/0/](http://127.0.0.1:8000/api/v1/posts/0/comments/0/)

Ответ, статус код 204:

```JSON
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

Ответ, статус код 403:

```JSON
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

### Работа с сообществами

Работа с сообществами доступна всем в режиме "только чтение". Любые изменения
 не доступны.

#### Получение списка сообществ

GET: [/api/v1/groups/](http://127.0.0.1:8000/api/v1/groups/)

Ответ, статус код 200:

```JSON
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
```

#### Информация о сообществе

Получить конкретную информацю о сообществе возможно используя её **id**.

Параметр пути, передаваемый в GET запросе:
>**id**: тип integer, целое положительное число. Соответствует уникальному 
> идентификатору сообщества.

GET: api/v1/groups/{id}/

GET: [api/v1/groups/0/](http://127.0.0.1:8000/api/v1/groups/0/)

Ответ, статус код 200:

```JSON
{
  "id": 0,
  "title": "string",
  "slug": "string",
  "description": "string"
}
```

Ответ, статус код 404:

```JSON
{
  "detail": "Страница не найдена."
}
```

### Работа с подписками

Позволяет получить все подписки пользователя, сделавшего запрос. Анонимные
 запросы запрещены.
 
Возможен поиск по подпискам с применением параметра **search**.

Поиск осуществляется по авторам на которых есть подписка, регистронезависимый.

GET: [/api/v1/follow/?search=zhss](http://127.0.0.1:8000/api/v1/follow/?search=zhss)

```JSON
[
    {
        "user": "string",
        "following": "zhss"
    }
]
```

#### Получение информации о подписках

Возвращает все подписки пользователя, сделавшего запрос.

GET: [/api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

Ответ, статус код 200:

```JSON
[
  {
    "user": "string",
    "following": "string"
  }
]
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

#### Подписаться на пользователя

Подписка пользователя от имени которого сделан запрос на пользователя
 переданного в теле запроса.

Параметры **JSON** запроса:
>**following**: тип string, обязательное текстовое поле. Содержит имя
> пользователя на которого необходимо подписаться.

**JSON** запрос:

```JSON
{
  "following": "string"
}
```

POST: [/api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

Ответ, статус код 201:

```JSON
{
  "user": "string",
  "following": "string"
}
```

Ответ, статус код 400:

```JSON
{
  "following": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Учетные данные не были предоставлены."
}
```

### Авторизация с применением JWT токена

#### Получить JWT-токен

Для получения JWT-токена необходимо отправить **JSON** запрос, содержащий имя пользователя и пароль.

Параметры **JSON** запроса:
>**username**: тип string, обязательное текстовое поле. Содержит имя
> пользователя.
>
>**password**: тип string, обязательное текстовое поле. Содержит пароль
> пользователя.

**JSON** запрос:

```JSON
{
  "username": "string",
  "password": "string"
}
```

POST: [/api/v1/jwt/create/](http://127.0.0.1:8000/api/v1/jwt/create/)

Ответ, статус код 200:

```JSON
{
  "refresh": "string",
  "access": "string"
}
```

Ответ, статус код 400:

```JSON
{
  "username": [
    "Обязательное поле."
  ],
  "password": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "No active account found with the given credentials"
}
```

#### Обновить JWT-токен

Для обновления JWT-токена необходимо отправить **JSON** запрос, содержащий
 **refresh** токен.

Параметры **JSON** запроса:
>**refresh**: тип string, обязательное текстовое поле. Содержит токен
> полученный при [/api/v1/jwt/create/](http://127.0.0.1:8000/api/v1/jwt/create/).

**JSON** запрос:

```JSON
{
  "refresh": "string"
}
```

POST: [/api/v1/jwt/refresh/](http://127.0.0.1:8000/api/v1/jwt/refresh/)

Ответ, статус код 200:

```JSON
{
  "access": "string"
}
```

Ответ, статус код 400:

```JSON
{
  "refresh": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

#### Проверить JWT-токен

Для проверки JWT-токена необходимо отправить **JSON** запрос, содержащий
 **token** токен.

Параметры **JSON** запроса:
>**token**: тип string, обязательное текстовое поле. Содержит токен
> полученный при [/api/v1/jwt/create/](http://127.0.0.1:8000/api/v1/jwt/create/).

**JSON** запрос:

```JSON
{
  "token": "string"
}
```

POST: [/api/v1/jwt/verify/](http://127.0.0.1:8000/api/v1/jwt/verify/)

Ответ, статус код 200:

```JSON
```

Ответ, статус код 400:

```JSON
{
  "token": [
    "Обязательное поле."
  ]
}
```

Ответ, статус код 401:

```JSON
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```
