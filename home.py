import streamlit as st
import pandas as pd

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

# Caminhos para os arquivos de imagem
image_path1 = 'Assets/vk4.png'  # Atualize com o caminho correto se necessário
image_path2 = 'Assets/vk5.png'  # Atualize com o caminho correto se necessário

# Criar duas colunas para as imagens
col1, col2 = st.columns(2)

# Exibir as imagens nas colunas
with col1:
    try:
        st.image(image_path1, width=200)  # Ajuste o valor de width conforme necessário
    except FileNotFoundError:
        st.error(f"Arquivo {image_path1} não encontrado. Certifique-se de que o caminho está correto e o arquivo está na pasta certa.")

with col2:
    try:
        st.image(image_path2, width=200)  # Ajuste o valor de width conforme necessário
    except FileNotFoundError:
        st.error(f"Arquivo {image_path2} não encontrado. Certifique-se de que o caminho está correto e o arquivo está na pasta certa.")


# Título da página
st.title("Home")


st.write("Bem-vindo à aplicação de análise de criativos por lead score. Use o menu para navegar entre as páginas.")

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
    "Número de Leads", 
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

# Mostrar a tabela interativa sem a coluna de índice
st.dataframe(
    sorted_data_limited, 
    use_container_width=True, 
    hide_index=True  # Ocultar a coluna de índice
)
