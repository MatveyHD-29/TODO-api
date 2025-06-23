# TODO API
Мини-сервис управления задачами <!-- описание репозитория -->

<!--Установка-->
## Установка (Linux)
У вас должны быть установлены [зависимости проекта](https://github.com/OkulusDev/Oxygen#зависимости)

1. Клонирование репозитория 

```git clone https://github.com/OkulusDev/Oxygen.git```

2. Переход в директорию Oxygen

```cd Oxygen```

3. Создание виртуального окружения

```python3 -m venv venv```

4. Активация виртуального окружения

```source venv/bin/activate```

5. Установка зависимостей

```pip3 install -r requirements.txt```

6. Запуск скрипта для демонстрации возможностей Oxygen

```python3 oxygen.py --help```

<!--Маршруты API-->
## Маршруты API
| Метод | Путь              | Описание                   |
|-------|-------------------|----------------------------|
| GET   | /tasks            | Получить все задачи        |
| GET   | /tasks/<id>       | Получить задачу по ID      |
| POST  | /tasks            | Создать новую задачу       |
| PUT   | /tasks/<id>       | Обновить задачу по ID      |
| DELETE| /tasks/<id>       | Удалить задачу по ID       |

[API-документация](https://documenter.getpostman.com/view/41188224/2sB2xCh9Ly)