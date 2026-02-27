# Инструкция по публикации на GitHub

## Шаги для выкладывания репозитория

### 1. Инициализация Git репозитория

```bash
cd "/Users/qwe123/Downloads/Архив"
git init
```

### 2. Добавление файлов

```bash
git add .
git commit -m "Initial commit: PolyTool copy-trading bot"
```

### 3. Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Название: `polytool-bot` (или другое по вашему выбору)
4. Описание: "Open-source copy-trading bot for Polymarket"
5. Выберите Public или Private
6. **НЕ** добавляйте README, .gitignore или license (они уже есть)
7. Нажмите "Create repository"

### 4. Подключение к GitHub

```bash
# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/polytool-bot.git
git branch -M main
git push -u origin main
```

### 5. Обновление ссылок в README (если нужно)

Если URL репозитория отличается от `https://github.com/polytool/polytool-bot`, обновите ссылки в:
- `README.md` (все ссылки на GitHub)
- `pyproject.toml` (поле `Repository`)

### 6. Настройка GitHub Pages (опционально)

Если хотите добавить GitHub Actions для автоматического деплоя:

1. Создайте `.github/workflows/deploy.yml`
2. Настройте автоматический деплой при push

### 7. Добавление тегов релиза

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Проверка

После публикации проверьте:
- ✅ README отображается корректно
- ✅ Все бейджи работают
- ✅ Ссылки ведут на правильные страницы
- ✅ LICENSE файл виден
- ✅ .gitignore работает (не видно .env файлов)

## Дополнительные настройки

### Topics (теги репозитория)
Добавьте на странице репозитория:
- `polymarket`
- `copy-trading`
- `trading-bot`
- `python`
- `fastapi`
- `polygon`
- `prediction-markets`

### Описание репозитория
```
Open-source copy-trading bot for Polymarket. Automatically copy trades from tracked wallets with customizable filters and risk management.
```
