import streamlit as st
import pandas as pd
from PIL import Image

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

# Caminhos para os arquivos de imagem
image_path1 = 'Assets/vk4.png'  # Atualize com o caminho correto se necessário

# Função para ajustar o tamanho da imagem
def resize_image(image_path, width):
    with Image.open(image_path) as img:
        # Ajusta o tamanho mantendo a proporção
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio)
        resized_img = img.resize((width, new_height))
        return resized_img

# Criar duas colunas para as imagens
col1, col2 = st.columns([1, 1])  # Usar colunas com largura igual

# Exibir a primeira imagem
with col1:
    try:
        img1 = resize_image(image_path1, 200)  # Tamanho fixo para a primeira imagem
        st.image(img1)
    except FileNotFoundError:
        st.error(f"Arquivo {image_path1} não encontrado. Certifique-se de que o caminho está correto e o arquivo está na pasta certa.")

# Adicionar um espaçamento vertical usando HTML antes da segunda imagem
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)  # Ajuste a altura conforme necessário

# Título da página
st.title("Home")

st.write("Bem-vindo à aplicação de análise de criativos por lead score. Use o menu para navegar entre as páginas.")

st.header("Tabela Interativa de Média dos Lead Scores por Criativo")

# Calcular a média dos lead scores e a frequência por criativo
average_scores = data.groupby('data.ad_name').agg(
    Média_do_Lead_Score=('lead_score', 'mean'),
    Frequência=('lead_score', 'count')
).reset_index()

# Renomear as colunas
average_scores.columns = ['Criativo', 'Média do Lead Score', 'Frequência']

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

# Filtro de frequência
min_frequency = st.sidebar.slider(
    "Frequência Mínima", 
    min_value=1, 
    max_value=average_scores['Frequência'].max(), 
    value=1,
    step=1,
    key="min_frequency_slider"  # Chave única para o slider
)

# Ordem de exibição
sort_by = st.sidebar.selectbox(
    "Ordenar por", 
    options=["Criativo", "Média do Lead Score", "Frequência"],
    key="sort_by_selectbox"  # Chave única para o selectbox
)
sort_order = st.sidebar.radio(
    "Ordem", 
    options=["Ascendente", "Descendente"],
    key="sort_order_radio"  # Chave única para o radio
)
ascending = sort_order == "Ascendente"

# Filtragem por frequência e ordenação dos dados
filtered_data = average_scores[average_scores['Frequência'] >= min_frequency]
sorted_data = filtered_data.sort_values(by=sort_by, ascending=ascending)

# Exibir apenas o número selecionado de registros
sorted_data_limited = sorted_data.head(num_records)

# Mostrar a tabela interativa sem a coluna de índice
st.dataframe(
    sorted_data_limited, 
    use_container_width=True, 
    hide_index=True  # Ocultar a coluna de índice
)
