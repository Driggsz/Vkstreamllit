import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

st.header("Análise de Outliers por Criativo")

# Identificar outliers
outliers = data[(data['lead_score'] > data['lead_score'].quantile(0.95)) | (data['lead_score'] < data['lead_score'].quantile(0.05))]
outliers_count = outliers.groupby('data.ad_name').size().reset_index(name='Número de Outliers')

# Seção: Tabela de Outliers com Filtros de Ordenação
st.subheader("Tabela de Outliers por Criativo")

# Adicionar filtros de direção de ordenação
selected_direction = st.selectbox('Direção de Ordenação(Apenas para Outliers)', ['Ascendente', 'Descendente'])

# Definir a direção de ordenação
ascending = selected_direction == 'Ascendente'

# Ordenar a tabela com base na direção selecionada
sorted_outliers_count = outliers_count.sort_values(by='Número de Outliers', ascending=ascending)

# Mostrar a tabela interativa
st.dataframe(sorted_outliers_count)

# Top 10 Outliers por Criativo
top_outliers_creatives = outliers_count.nlargest(10, 'Número de Outliers')

# Gráfico de Barras - Número de Outliers por Criativo (Top 10)
st.subheader("Número de Outliers por Criativo (Top 10)")

# Criar o gráfico de barras com Plotly Express
fig = px.bar(
    top_outliers_creatives,
    x='Número de Outliers',
    y='data.ad_name',
    orientation='h',
    title='Número de Outliers por Criativo (Top 10)',
    labels={'data.ad_name': 'Criativo', 'Número de Outliers': 'Número de Outliers'},
    color='Número de Outliers',
    color_continuous_scale='reds'
)

# Atualizar layout do gráfico
fig.update_layout(xaxis_title='Número de Outliers', yaxis_title='Criativo', coloraxis_showscale=False)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)


# Adicionar filtro para quantidade de criativos a serem comparados
num_creatives = st.slider('Selecione o número de criativos para comparar', min_value=1, max_value=len(outliers_count), value=10)

# Top Criativos com Mais Outliers
top_creatives = outliers_count.nlargest(num_creatives, 'Número de Outliers')['data.ad_name']

# Filtrar dados para apenas os top criativos
filtered_data = data[data['data.ad_name'].isin(top_creatives)]

# Gráfico Comparativo de Box Plots
st.subheader(f"Box Plot Comparativo dos Top {num_creatives} Criativos com Mais Outliers")

fig_box = px.box(
    filtered_data,
    x='data.ad_name',
    y='lead_score',
    title=f'Comparação de Lead Scores dos Top {num_creatives} Criativos com Mais Outliers',
    points='all'
)

# Atualizar layout do gráfico
fig_box.update_layout(
    xaxis_title='Criativo',
    yaxis_title='Lead Score',
    xaxis_tickangle=-45,
    boxmode='group'  # Agrupa as caixas
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_box)