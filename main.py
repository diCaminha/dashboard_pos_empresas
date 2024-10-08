import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

hapvida_data = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
nagem_data = pd.read_csv('RECLAMEAQUI_NAGEM.csv')
ibyte_data = pd.read_csv('RECLAMEAQUI_IBYTE.csv')

hapvida_data['Empresa'] = 'Hapvida'
nagem_data['Empresa'] = 'Nagem'
ibyte_data['Empresa'] = 'Ibyte'

empresas_data = pd.concat([hapvida_data, nagem_data, ibyte_data])

st.title("Dashboard Reclame Aqui - Análise de Reclamações")
st.sidebar.header("Filtros")

empresa_selecionada = st.sidebar.selectbox("Selecione a empresa", ["Todas", "Hapvida", "Nagem", "Ibyte"])

estados_disponiveis = empresas_data['LOCAL'].unique().tolist()
estado_selecionado = st.sidebar.selectbox("Selecione o estado", ["Todos"] + estados_disponiveis)

status_disponiveis = empresas_data['STATUS'].unique().tolist()
status_selecionado = st.sidebar.selectbox("Selecione o status", ["Todos"] + status_disponiveis)

# Aplicação dos filtros
filtered_data = empresas_data.copy()

if empresa_selecionada != "Todas":
    filtered_data = filtered_data[filtered_data['Empresa'] == empresa_selecionada]

if estado_selecionado != "Todos":
    filtered_data = filtered_data[filtered_data['LOCAL'] == estado_selecionado]

if status_selecionado != "Todos":
    filtered_data = filtered_data[filtered_data['STATUS'] == status_selecionado]


st.subheader("Série Temporal de Reclamações")


valid_dates = filtered_data.dropna(subset=['ANO', 'MES', 'DIA'])  # Remover linhas com valores ausentes

# Renomear as colunas para que o datetime funcione
date_columns = valid_dates[['ANO', 'MES', 'DIA']].rename(
    columns={'ANO': 'year', 'MES': 'month', 'DIA': 'day'}
)

valid_dates['Data'] = pd.to_datetime(date_columns)
time_series = valid_dates.groupby('Data').size()


st.subheader("Frequência de Reclamações por Estado")
estado_freq = filtered_data['LOCAL'].value_counts()
st.bar_chart(estado_freq)

st.subheader("Frequência de Reclamações por STATUS")
status_freq = filtered_data['STATUS'].value_counts()
st.bar_chart(status_freq)

st.subheader("Distribuição do Tamanho do Texto (DESCRIÇÃO)")
plt.figure(figsize=(10, 6))
plt.hist(filtered_data['DESCRICAO'].str.len(), bins=30)
st.pyplot(plt)
