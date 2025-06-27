import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from datetime import datetime

st.set_page_config(page_title="Анализ продаж", layout="wide")
st.title("Анализ данных о продажах с визуализацией и Excel-отчётом")

@st.cache_data
def get_sample_csv():
    sample_data = pd.DataFrame({
        'Дата': pd.date_range(start='2025-01-01', periods=15, freq='D'),
        'Продажи': [1200, 1500, 1100, 1800, 1600, 1750, 1400, 1550, 1900, 2100, 2050, 1980, 1700, 1650, 1600]
    })
    return sample_data.to_csv(index=False).encode('utf-8')

with st.expander("📎 Скачать пример CSV-файла"):
    st.download_button(
        label="Скачать sample_sales_data.csv",
        data=get_sample_csv(),
        file_name="sample_sales_data.csv",
        mime="text/csv"
    )

uploaded_file = st.file_uploader("Загрузите CSV-файл с колонками 'Дата' и 'Продажи'", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Дата'])
    df = df.sort_values('Дата')
    st.success("Файл успешно загружен!")

    min_date = df['Дата'].min().date()
    max_date = df['Дата'].max().date()
    start_date = st.date_input("Начальная дата", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Конечная дата", min_value=min_date, max_value=max_date, value=max_date)

    if start_date > end_date:
        st.error("Начальная дата не может быть позже конечной")
    else:
        filtered_df = df[(df['Дата'] >= pd.to_datetime(start_date)) & (df['Дата'] <= pd.to_datetime(end_date))].copy()

        if filtered_df.empty:
            st.warning("Нет данных в выбранном диапазоне")
        else:
            filtered_df['Темп прироста (%)'] = filtered_df['Продажи'].pct_change() * 100

            st.subheader("Ключевые показатели")
            total_sales = filtered_df['Продажи'].sum()
            average_sales = filtered_df['Продажи'].mean()
            max_sales = filtered_df['Продажи'].max()
            min_sales = filtered_df['Продажи'].min()

            st.metric("Общая выручка", f"{total_sales:,.0f}")
            st.metric("Средние продажи", f"{average_sales:,.2f}")
            st.metric("Максимальные продажи", f"{max_sales:,.0f}")
            st.metric("Минимальные продажи", f"{min_sales:,.0f}")

            st.subheader("График продаж с трендом")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=filtered_df, x='Дата', y='Продажи', marker='o', ax=ax, label='Продажи')
            z = np.polyfit(filtered_df['Дата'].map(pd.Timestamp.toordinal), filtered_df['Продажи'], 1)
            p = np.poly1d(z)
            ax.plot(filtered_df['Дата'], p(filtered_df['Дата'].map(pd.Timestamp.toordinal)), "r--", label='Трендовая линия')
            ax.legend()
            st.pyplot(fig)

            st.subheader("Скачать Excel-отчёт")
            with BytesIO() as b:
                wb = Workbook()
                ws = wb.active
                ws.title = "Отчет"
                ws.append(["KPI", "Значение"])
                ws.append(["Общая выручка", total_sales])
                ws.append(["Средние продажи", average_sales])
                ws.append(["Максимальные продажи", max_sales])
                ws.append(["Минимальные продажи", min_sales])
                ws.append([])
                ws.append(["Дата", "Продажи", "Темп прироста (%)"])
                for _, row in filtered_df.iterrows():
                    ws.append([
                        row['Дата'].strftime('%Y-%m-%d'),
                        row['Продажи'],
                        None if pd.isna(row['Темп прироста (%)']) else round(row['Темп прироста (%)'], 2)
                    ])
                wb.save(b)
                st.download_button(
                    label="📥 Скачать Excel-файл",
                    data=b.getvalue(),
                    file_name="sales_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
