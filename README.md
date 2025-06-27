
# 📊 Sales Analyzer — интерактивный анализ продаж на Streamlit

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

> Простой инструмент для анализа CSV-данных о продажах с фильтрами, визуализациями и генерацией Excel-отчётов.

---

## 🔍 Основные функции

- 📥 Загрузка CSV-файла с данными (`Дата`, `Продажи`)
- 📈 Построение графиков трендов и барчартов
- 📊 Фильтрация по дате
- 📤 Генерация Excel-отчёта с визуализациями
- 💾 Загрузка примера CSV для тестирования

---

## 🚀 Демо

👉 Попробуй онлайн: [Streamlit Cloud (ссылка будет здесь)](https://share.streamlit.io/Go0kie/sales_analyzer_streamlit/main/app.py)

---

## 🖥️ Запуск локально

```bash
git clone https://github.com/Go0kie/sales_analyzer_streamlit.git
cd sales_analyzer_streamlit
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Структура проекта

```
sales_analyzer_streamlit/
├── app.py               # Основной Streamlit-приложение
├── requirements.txt     # Зависимости
└── README.md            # Этот файл
```

---

## 📌 Пример CSV-файла

```csv
Дата,Продажи
2025-01-01,1200
2025-01-02,1500
...
```

---

## 📃 Лицензия

Этот проект распространяется под лицензией **MIT**.
