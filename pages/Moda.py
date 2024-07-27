import streamlit as st
import pandas as pd
import plotly.express as px

# Função para categorizar os leads conforme a qualidade
def categorize_lead(score):
    if score > 0.60:
        return 'Alta'
    elif score > 0.42:
        return 'Média'
    elif score > 0.28:
        return 'Baixa'
    else:
        return 'Desqualificado'

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

# Calcular frequência, média de lead_score e categoria por criativo
creative_summary = data.groupby('data.ad_name').agg(
    Frequência=('data.ad_name', 'size'),
    Média_Lead_Score=('lead_score', 'mean')
).reset_index()
creative_summary['Categoria'] = creative_summary['Média_Lead_Score'].apply(categorize_lead)

# Título da página
st.title("Análise de Criativos")

# Seção: Moda dos Criativos
st.header("Moda dos Criativos(Top 10)")

# Contar a frequência dos criativos
creative_counts = creative_summary.sort_values(by='Frequência', ascending=False)

# Gráfico de Barras - Moda dos Criativos com Plotly
fig = px.bar(creative_counts.head(10), x='Frequência', y='data.ad_name', orientation='h',
             title='', labels={'Frequência': 'Frequência', 'data.ad_name': 'Criativo'})
st.plotly_chart(fig)

# Seção: Tabela Interativa
st.subheader("Tabela Interativa")

# Adicionar filtros de ordenação e direção
selected_order = st.selectbox('Ordenar por', ['Frequência', 'Média Lead Score'])
selected_direction = st.selectbox('Direção de Ordenação', ['Ascendente', 'Descendente'])

# Definir a direção de ordenação
ascending = selected_direction == 'Ascendente'

if selected_order == 'Frequência':
    sorted_summary = creative_summary.sort_values(by='Frequência', ascending=ascending)
else:
    sorted_summary = creative_summary.sort_values(by='Média_Lead_Score', ascending=ascending)

# Mostrar a tabela interativa
st.dataframe(sorted_summary)
