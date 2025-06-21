import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Настройка страницы
st.set_page_config(page_title="Анализ бактерий", page_icon="🔬")
st.title("🔬 Анализ динамики бактерий")

# Добавляем описание проекта
st.markdown("""
**Здравствуйте! Вас приветствует Варвара Говорухина, и это мой проект под названием 
"Анализ антимикробной активности молочнокислых бактерий в отношении микрофлоры рук". 
На этом сайте представлены результаты моих исследований.**
""")

st.write("Загрузите Excel-файл с данными о количестве бактерий по дням")

def process_file(uploaded_file):
    """Обработка загруженного файла с данными о бактериях"""
    try:
        # Чтение файла
        df = pd.read_excel(uploaded_file)
        
        # Проверка структуры
        if len(df.columns) < 2:
            st.error("Ошибка: Файл должен содержать минимум 2 столбца (названия бактерий и данные по дням)")
            return None
            
        # Обработка данных
        # Первый столбец - названия бактерий
        bacteria_col = df.columns[0]
        
        # Создаем длинный формат данных для визуализации
        melted_df = df.melt(
            id_vars=[bacteria_col],
            var_name='День',
            value_name='Количество'
        )
        
        return melted_df, df
    
    except Exception as e:
        st.error(f"Ошибка обработки файла: {e}")
        return None, None

# Загрузка файла
uploaded_file = st.file_uploader("Выберите файл", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Обработка файла
    melted_df, original_df = process_file(uploaded_file)
    
    if melted_df is not None and original_df is not None:
        # Отображение загруженных данных
        st.subheader("Загруженные данные")
        st.dataframe(original_df)
        
        # Визуализация (только столбчатая диаграмма)
        if not melted_df.empty:
            fig_bar = px.bar(
                melted_df,
                x='День',
                y='Количество',
                color=original_df.columns[0],  # Первый столбец с названиями бактерий
                barmode='group',
                title='Динамика бактерий по дням',
                labels={original_df.columns[0]: 'Тип бактерий'}
            )
            st.plotly_chart(fig_bar)

# Добавление таблицы с ареалом распространения
st.markdown("---")
st.subheader("Ареал распространения бактерий")

# Описание задачи исследования
st.markdown("""
**Главной моей задачей было определение молочнокислых бактерий с наибольшим антимикробным воздействием. 
В этой таблице можно увидеть среднее воздействие бактерий на микробы.**
""")

# Создаем DataFrame с данными из файла
areal_data = {
    "Продукт": [
        "«Пробиотик»",
        "«Бифидум»",
        "«Биойогурт»",
        "«Наринэ»",
        "«Ацидофильный йогурт»"
    ],
    "Характеристика": [
        "Среднее значение воздействия – 4 мм",
        "Среднее значение воздействия – 3,8 мм",
        "Среднее значение воздействия – 2,4 мм",
        "Нет данных (бактерии распространились там же, где микробы)",
        "Нет данных (бактерии распространились там же, где микробы)"
    ]
}

areal_df = pd.DataFrame(areal_data)
st.dataframe(areal_df, hide_index=True)

# Вывод после таблицы
st.markdown("""
**Пробиотик, Бифидум и Биойогурт подавили большое количество микробов, 
а Наринэ и Ацидофильный йогурт не справились с этой задачей.**
""")

# Постоянная диаграмма из файла "Диаграмма_бактерии.xlsx"
st.markdown("---")
st.subheader("Динамика развития бактерий")

# Описание эксперимента
st.markdown("""
**Я использовала 5 разных смесей, в каждой из которых было несколько видов бактерий. 
Здесь можно ознакомиться с количеством выросших штаммов среди смесей за 2 дня наблюдения.**
""")

# Создаем DataFrame с постоянными данными
permanent_data = {
    "Тип бактерий": [
        "Лактобактерии",
        "Стрептококки",
        "Лактококки",
        "Пропионибактерии"
    ],
    "День 1": [4, 3, 2, 1],
    "День 2": [3, 3, 2, 1]
}
permanent_df = pd.DataFrame(permanent_data)

# Преобразуем в длинный формат для визуализации
melted_permanent_df = permanent_df.melt(
    id_vars=["Тип бактерий"],
    var_name="День",
    value_name="Количество"
)

# Создаем и отображаем диаграмму
fig_permanent = px.bar(
    melted_permanent_df,
    x="День",
    y="Количество",
    color="Тип бактерий",
    barmode="group",
    title="Динамика развития бактерий в различных смесях",
    labels={"Тип бактерий": "Тип бактерий"},
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig_permanent)

# Отображаем используемые данные
st.write("Данные для диаграммы:")
st.dataframe(permanent_df, hide_index=True)

# Генерация примера файла
st.markdown("---")
st.subheader("Тестирование")
if st.button("Создать пример файла для тестирования"):
    # Типы бактерий
    bacteria_types = [
        'Лактобактерии', 
        'Стрептококки', 
        'Лактококки', 
        'Пропионибактерии',
        'Бифидобактерии'
    ]
    
    # Создаем DataFrame с данными
    days = 5
    data = {
        'Тип бактерий': bacteria_types
    }
    
    # Добавляем данные для каждого дня
    for day in range(1, days + 1):
        # Генерация случайных значений с разной динамикой для разных бактерий
        day_data = []
        for i, bacteria in enumerate(bacteria_types):
            base = np.random.randint(1, 10)
            trend = np.random.choice([-1, 0, 1])
            value = max(1, base + trend * (day - 1) + np.random.randint(-1, 2))
            day_data.append(value)
        data[f'День {day}'] = day_data
    
    sample_df = pd.DataFrame(data)
    
    # Создание файла в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sample_df.to_excel(writer, index=False)
    
    # Кнопка скачивания
    st.download_button(
        label="📥 Скачать пример файла",
        data=output.getvalue(),
        file_name="sample_bacteria.xlsx",
        mime="application/vnd.ms-excel"
    )
    
    # Показать предпросмотр
    st.write("Пример данных:")
    st.dataframe(sample_df)