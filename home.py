# home.py
import streamlit as st
import pandas as pd

st.title("Home")
st.write("Bem-vindo à aplicação de análise de criativos por lead score. Use o menu para navegar entre as páginas.")


# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

st.header("Tabela Interativa de Criativos e Lead Scores")

# Obter o número total de registros
total_records = len(data)

# Configurações de filtros e ordenação
st.sidebar.header("Configurações")

# Seleção do número de registros a serem exibidos
num_records = st.sidebar.slider("Número de Registros", min_value=5, max_value=total_records, value=10, step=1)

# Ordem de exibição
sort_by = st.sidebar.selectbox("Ordenar por", options=["data.ad_name", "lead_score"])
sort_order = st.sidebar.radio("Ordem", options=["Ascendente", "Descendente"])
ascending = sort_order == "Ascendente"

# Filtragem e ordenação dos dados
sorted_data = data[['data.ad_name', 'lead_score']].sort_values(by=sort_by, ascending=ascending)

# Exibir apenas o número selecionado de registros
sorted_data_limited = sorted_data.head(num_records)

# Mostrar a tabela interativa
st.dataframe(sorted_data_limited, use_container_width=True)



st.header("Tabela Interativa de Média dos Lead Scores por Criativo")

# Calcular a média dos lead scores por criativo
average_scores = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_scores.columns = ['Criativo', 'Média do Lead Score']

# Obter o número total de registros (criativos)
total_records = len(average_scores)

# Configurações de filtros e ordenação
st.sidebar.header("Configurações")

# Seleção do número de registros a serem exibidos
num_records = st.sidebar.slider(
    "Número de Registros", 
    min_value=5, 
    max_value=total_records, 
    value=10, 
    step=1,
    key="num_records_slider"  # Chave única para o slider
)

# Ordem de exibição
sort_by = st.sidebar.selectbox(
    "Ordenar por", 
    options=["Criativo", "Média do Lead Score"],
    key="sort_by_selectbox"  # Chave única para o selectbox
)
sort_order = st.sidebar.radio(
    "Ordem", 
    options=["Ascendente", "Descendente"],
    key="sort_order_radio"  # Chave única para o radio
)
ascending = sort_order == "Ascendente"

# Filtragem e ordenação dos dados
sorted_data = average_scores.sort_values(by=sort_by, ascending=ascending)

# Exibir apenas o número selecionado de registros
sorted_data_limited = sorted_data.head(num_records)

# Mostrar a tabela interativa
st.dataframe(sorted_data_limited, use_container_width=True)