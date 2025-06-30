# CodesCommanders API

REST API на Django с PostgreSQL, запущенный через Docker Compose.  
Проект для управления логикой команд и командиров.

---

## 📦 Технологии

- Python 3 / Django
- PostgreSQL
- Nginx (обратный прокси)
- Docker / Docker Compose

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

bash
git clone https://github.com/AnatoliPanas/CodesCommanders-API.git
cd CodesCommanders-API

### 2. Создать .env файл
Создай файл .env в корне проекта с содержимым:

env
Kopieren
Bearbeiten
POSTGRES_DB=codes_db
POSTGRES_USER=codes_user
POSTGRES_PASSWORD=strongpassword
MYSQL_ROOT_PASSWORD=dummy

### 3. Запустить проект
bash
Kopieren
Bearbeiten
docker-compose up --build -d

### 4. Выполнить миграции
bash
Kopieren
Bearbeiten
docker-compose exec web python manage.py migrate

### 5. Создать суперпользователя
bash
Kopieren
Bearbeiten
docker-compose exec web python manage.py createsuperuser
📁 Структура docker-compose
web — Django-приложение

dbPostgres — PostgreSQL

nginx — обратный прокси

volumes — для хранения данных PostgreSQL

app_network — bridge-сеть Docker

⚙️ Полезные команды
Задача	Команда
Перезапустить контейнеры	docker-compose restart
Посмотреть логи Django	docker-compose logs web
Открыть shell Django	docker-compose exec web python manage.py shell
Собрать статику (если нужно)	docker-compose exec web python manage.py collectstatic

❗ Возможные ошибки
Ошибка:
pgsql
Kopieren
Bearbeiten
could not translate host name "dbPostgres" to address
Решение: Убедись, что выполняешь команды внутри контейнера или проверь HOST в настройках Django (settings.py).

🔐 Переменные окружения
Переменные загружаются из .env.
Для продакшена рекомендуется использовать секреты Docker или безопасные хранилища.

🛠 План развития
Добавить документацию API (Swagger, Redoc)

Написать тесты

Настроить CI/CD (GitHub Actions)

Автоматизировать деплой

📄 Лицензия
MIT License.

## 7. Обратная связь

**Автор:** [Anatoli Panas](https://github.com/AnatoliPanas/CodesCommanders-API)
