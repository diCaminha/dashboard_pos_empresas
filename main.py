import pandas as pd
import streamlit as st

from plot_util import plot_time_series, plot_state_frequency, plot_status_frequency, \
    plot_description_length_distribution


def load_data():
    hapvida_data = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
    nagem_data = pd.read_csv('RECLAMEAQUI_NAGEM.csv')
    ibyte_data = pd.read_csv('RECLAMEAQUI_IBYTE.csv')

    hapvida_data['Empresa'] = 'Hapvida'
    nagem_data['Empresa'] = 'Nagem'
    ibyte_data['Empresa'] = 'Ibyte'

    empresas_data = pd.concat([hapvida_data, nagem_data, ibyte_data])
    return empresas_data


def get_user_filters(empresas_data):
    st.sidebar.header("Filtros")

    empresa_selecionada = st.sidebar.selectbox(
        "Selecione a empresa", ["Todas", "Hapvida", "Nagem", "Ibyte"]
    )

    estados_disponiveis = empresas_data['LOCAL'].unique().tolist()
    estado_selecionado = st.sidebar.selectbox(
        "Selecione o estado", ["Todos"] + estados_disponiveis
    )

    status_disponiveis = empresas_data['STATUS'].unique().tolist()
    status_selecionado = st.sidebar.selectbox(
        "Selecione o status", ["Todos"] + status_disponiveis
    )

    return {
        'empresa': empresa_selecionada,
        'estado': estado_selecionado,
        'status': status_selecionado
    }


def filter_data(empresas_data, filters):
    filtered_data = empresas_data.copy()

    if filters['empresa'] != "Todas":
        filtered_data = filtered_data[filtered_data['Empresa'] == filters['empresa']]

    if filters['estado'] != "Todos":
        filtered_data = filtered_data[filtered_data['LOCAL'] == filters['estado']]

    if filters['status'] != "Todos":
        filtered_data = filtered_data[filtered_data['STATUS'] == filters['status']]

    return filtered_data


def create_time_series(filtered_data):
    valid_dates = filtered_data.dropna(subset=['ANO', 'MES', 'DIA'])

    date_columns = valid_dates[['ANO', 'MES', 'DIA']].rename(
        columns={'ANO': 'year', 'MES': 'month', 'DIA': 'day'}
    )
    valid_dates['Data'] = pd.to_datetime(date_columns)
    time_series = valid_dates.groupby('Data').size()
    return time_series


empresas_data = load_data()
st.title("Dashboard Reclame Aqui - Análise de Reclamações")

filters = get_user_filters(empresas_data)
filtered_data = filter_data(empresas_data, filters)

if not filtered_data.empty:
    time_series = create_time_series(filtered_data)
    if not time_series.empty:
        plot_time_series(time_series)
    else:
        st.write("Nenhum dado disponível para a série temporal.")

    plot_state_frequency(filtered_data)
    plot_status_frequency(filtered_data)
    plot_description_length_distribution(filtered_data)
else:
    st.write("Nenhum dado encontrado com os filtros selecionados.")
