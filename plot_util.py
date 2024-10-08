import streamlit as st
import matplotlib.pyplot as plt
def plot_time_series(time_series):
    st.subheader("Série Temporal de Reclamações")
    st.line_chart(time_series)


def plot_state_frequency(filtered_data):
    st.subheader("Frequência de Reclamações por Estado")
    estado_freq = filtered_data['LOCAL'].value_counts()
    st.bar_chart(estado_freq)


def plot_status_frequency(filtered_data):
    st.subheader("Frequência de Reclamações por STATUS")
    status_freq = filtered_data['STATUS'].value_counts()
    st.bar_chart(status_freq)


def plot_description_length_distribution(filtered_data):
    st.subheader("Distribuição do Tamanho do Texto (DESCRIÇÃO)")
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_data['DESCRICAO'].str.len(), bins=30)
    st.pyplot(plt)