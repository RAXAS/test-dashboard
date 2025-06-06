# Test Dashboard

Этот проект представляет собой автоматизированную систему тестирования с использованием `pytest` и генерацией отчётов через `allure`.

## 📦 Стек технологий

- **pytest** — фреймворк для написания и запуска тестов
- **requests** — HTTP-клиент для Python, используется для API-тестов
- **faker** — генератор фиктивных данных для тестов
- **allure** — система генерации подробных HTML-отчетов
- **pydantic** — валидация и сериализация данных

## 🚀 Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите тесты:
   ```bash
   pytest --alluredir=allure_results
   ```
   
3. Сгенерируйте и откройте отчет:
   ```bash
   allure serve allure_results
   ```

### Если возникнут проблемы с разпознованием команды allure, можно установить его через scoop
   ```bash
   irm get.scoop.sh | iex
   scoop install allure
   ```

## 📁 Структура проекта

- `tests/` — каталог с тестами
- `allure_results/` — папка, куда сохраняются результаты выполнения тестов
- `allure-2.33.0/` — встроенный дистрибутив Allure
- `.pytest_cache/` — кеш `pytest`, не подлежит коммиту
- `.idea/` — конфигурации среды разработки (PyCharm)

## ⚙️ Примечания

- В `.gitignore` указана папка `.idea`
- Проект предполагает запуск на Python 3.7+
