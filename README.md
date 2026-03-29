# Dochazka Generator

Telegram-бот для автоматической генерации книги посещаемости (kniha docházky) из таблицы рабочих часов (mzdy).

## Как пользоваться

1. Отправь боту файл `Mzdy_MM.YYYY.xlsx` (например `Mzdy_03.2026.xlsx`)
2. Бот сгенерирует и отправит файл `Dochazka_MM.YYYY.xlsx`

## Формат входного файла

- Имя файла: `Mzdy_MM.YYYY.xlsx`
- Лист с данными: в ячейке B1 должно быть слово "часов"
- Строка 1: заголовки — B = часы кофейни, D и далее = фамилии сотрудников
- Строки 5–35: данные по дням (A = номер дня, B = часы кофейни, D+ = часы сотрудников)
- Опционально: второй лист с полными именами (Jméno, Příjmení)

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Вписать BOT_TOKEN в .env
```

## Запуск

```bash
source venv/bin/activate
python bot.py
```

## Деплой (systemd)

```bash
sudo cp dochazka-generator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dochazka-generator
sudo systemctl start dochazka-generator
```
