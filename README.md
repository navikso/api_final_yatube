# api_final

### Описание 
API для социальной сети, в которой публикуются личные дневники на личных страницах. Зарегистрированные пользователи могут размещать посты на своей странице, подписываться на других авторов, оставлять комментарии. Незарегистрированным пользователям список постов доступен только для чтения без права размещения собственных.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Доступные запросы к API
GET.
POST.
PUT.
PATCH.
DELETE.
