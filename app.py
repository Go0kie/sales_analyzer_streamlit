import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

# Настройки страницы
st.set_page_config(page_title="Анализ продаж", layout="wide")
st.title("📊 Анализ данных о продажах")

# 📁 Генерация тестового CSV-файла
@st.cache_data
def get_sample_csv() -> bytes:
    sample_data = pd.DataFrame({
        'Дата': pd.date_range(start='2025-01-01', periods=15, freq='D'),
        'Продажи': [1200, 1500, 1100, 1800, 1600, 1750, 1400, 1550, 1900, 2100, 2050, 1980, 1700, 1650, 1600]
    })
    return sample_data.to_csv(index=False).encode('utf-8')

# 📥 Интерфейс загрузки
def upload_interface() -> pd.DataFrame:
    with st.expander("📎 Скачать пример CSV-файла"):
        st.download_button("Скачать sample_sales_data.csv", data=get_sample_csv(), file_name="sample_sales_data.csv", mime="text/csv")

    uploaded_file = st.file_uploader("Загрузите CSV-файл с колонками 'Дата' и 'Продажи'", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, parse_dates=['Дата'])
        df.sort_values('Дата', inplace=True)
        st.success("✅ Файл успешно загружен!")
        return df
    return pd.DataFrame()

# 📆 Интерфейс выбора даты
def filter_by_date(df: pd.DataFrame) -> pd.DataFrame:
    min_date, max_date = df['Дата'].min().date(), df['Дата'].max().date()
    start_date = st.date_input("Начальная дата", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Конечная дата", min_value=min_date, max_value=max_date, value=max_date)

    if start_date > end_date:
        st.error("❌ Начальная дата не может быть позже конечной")
        return pd.DataFrame()
    
    filtered = df[(df['Дата'] >= pd.to_datetime(start_date)) & (df['Дата'] <= pd.to_datetime(end_date))].copy()
    filtered['Темп прироста (%)'] = filtered['Продажи'].pct_change() * 100
    return filtered

# 📈 Визуализация графика
def plot_trend(df: pd.DataFrame):
    st.subheader("📉 График продаж с трендом")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='Дата', y='Продажи', marker='o', ax=ax, label='Продажи')
    
    # Построение трендовой линии
    z = np.polyfit(df['Дата'].map(datetime.toordinal), df['Продажи'], 1)
    trend = np.poly1d(z)
    ax.plot(df['Дата'], trend(df['Дата'].map(datetime.toordinal)), "r--", label='Трендовая линия')
    ax.legend()
    st.pyplot(fig)

# 📊 Показ ключевых метрик
def show_kpis(df: pd.DataFrame):
    st.subheader("📌 Ключевые показатели")
    st.metric("Общая выручка", f"{df['Продажи'].sum():,.0f}")
    st.metric("Средние продажи", f"{df['Продажи'].mean():,.2f}")
    st.metric("Максимальные продажи", f"{df['Продажи'].max():,.0f}")
    st.metric("Минимальные продажи", f"{df['Продажи'].min():,.0f}")

# 💾 Генерация Excel-отчёта
def generate_excel(df: pd.DataFrame) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Отчет"

    ws.append(["KPI", "Значение"])
    ws.append(["Общая выручка", df['Продажи'].sum()])
    ws.append(["Средние продажи", df['Продажи'].mean()])
    ws.append(["Максимальные продажи", df['Продажи'].max()])
    ws.append(["Минимальные продажи", df['Продажи'].min()])
    ws.append([])
    ws.append(["Дата", "Продажи", "Темп прироста (%)"])

    for _, row in df.iterrows():
        ws.append([
            row['Дата'].strftime('%Y-%m-%d'),
            row['Продажи'],
            None if pd.isna(row['Темп прироста (%)']) else round(row['Темп прироста (%)'], 2)
        ])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()

# 🚀 Основной поток работы
def main():
    df = upload_interface()
    if not df.empty:
        filtered = filter_by_date(df)
        if not filtered.empty:
            show_kpis(filtered)
            plot_trend(filtered)
            st.subheader("📤 Скачать Excel-отчёт")
            excel_data = generate_excel(filtered)
            st.download_button(
                label="📥 Скачать Excel-файл",
                data=excel_data,
                file_name="sales_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()