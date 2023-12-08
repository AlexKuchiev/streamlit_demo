import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff



st.title('Разведочный анализ данных рекламы банковских продуктов')
df = pd.read_csv('data/clients.csv')
st.dataframe(df)
st.subheader('Основные описательные статистики вещественных показателей')
st.table(df.drop(columns=['ID']).describe())

st.subheader('Графики распределения вещественных показателей')
num_cols = ['AGE','WORK_TIME','PERSONAL_INCOME','CREDIT','OWN_AUTO','LOAN_COUNT','CHILD_TOTAL']
filtered_data = df[num_cols]
column = st.selectbox('Выберите колонку', num_cols)
fig = px.histogram(filtered_data,x=column)
st.plotly_chart(fig)

df['Пол'] = df.GENDER.apply(lambda x: 'Male' if x == 1 else 'Female')
df['Отклик на рекламу'] = df.TARGET.apply(lambda x: 'Да' if x == 1 else 'Нет')
df['Наличие квартиры'] = df.FL_PRESENCE_FL.apply(lambda x: 'Да' if x == 1 else 'Нет')
df['Пенсионер'] = df.SOCSTATUS_PENS_FL.apply(lambda x: 'Да' if x == 1 else 'Нет')
df['Работает'] = df.SOCSTATUS_WORK_FL.apply(lambda x: 'Да' if x == 1 else 'Нет')
cat_cols = ['Пол','EDUCATION','MARITAL_STATUS','Работает','Пенсионер',
            'REG_ADDRESS_PROVINCE', 'Наличие квартиры','Отклик на рекламу','GEN_INDUSTRY']
st.subheader('Графики категориальных признаков и целевой переменной')
selected_column = st.selectbox("Выберите колонку", cat_cols)
fig = px.bar(df, x=selected_column)
st.plotly_chart(fig)

st.subheader('Зависимость целевой переменной от признаков')
cols = ['Пол','EDUCATION','MARITAL_STATUS','Работает','Пенсионер', 'CHILD_TOTAL',
        'REG_ADDRESS_PROVINCE', 'Наличие квартиры','GEN_INDUSTRY','LOAN_COUNT']
selected_column = st.selectbox("Выберите признак", cols)
fig = px.histogram(df, x=selected_column, color="Отклик на рекламу", barmode="group")
st.plotly_chart(fig)

a = df.groupby('TARGET', as_index=False).PERSONAL_INCOME.mean()
st.write('Средний доход тех кто откликнулся на рекламу и нет')
st.table(a)

corr_df = df[['AGE','CHILD_TOTAL','DEPENDANTS','TARGET','LOAN_COUNT','PERSONAL_INCOME']].corr()
fig = ff.create_annotated_heatmap(
    z=corr_df.values,
    x=corr_df.columns.tolist(),
    y=corr_df.index.tolist(),
    colorscale="Viridis"
)
fig.update_layout(title="Матрица корреляций")
st.plotly_chart(fig)


st.subheader('Анализ выбросов')
columns = ['AGE','WORK_TIME','PERSONAL_INCOME','CREDIT','OWN_AUTO','LOAN_COUNT','CHILD_TOTAL','DEPENDANTS']

# Создание ниспадающего списка для выбора колонки
selected_column = st.selectbox("Выберите колонку", columns)

# Построение боксплота с помощью Plotly
fig = px.box(df, y=selected_column)
st.plotly_chart(fig)

