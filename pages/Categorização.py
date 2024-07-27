import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# Função para carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo caminho do seu arquivo CSV
    return data

# Carregar os dados
data = load_data()

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

data['Qualidade'] = data['lead_score'].apply(categorize_lead)

# Título da aplicação
st.title("Análise de Qualidade dos Leads")

# Contar os leads em cada categoria
lead_counts = data['Qualidade'].value_counts().reset_index()
lead_counts.columns = ['Qualidade', 'Contagem']

# Gráfico de Barras - Contagem de Leads por Qualidade
st.header("Contagem de Leads por Qualidade")
fig_bar = px.bar(lead_counts, x='Qualidade', y='Contagem', color='Qualidade', title='Contagem de Leads por Qualidade')
st.plotly_chart(fig_bar)

# Gráfico de Pizza - Distribuição de Leads por Qualidade
st.header("Distribuição de Leads por Qualidade")
fig_pie = px.pie(lead_counts, values='Contagem', names='Qualidade', title="Distribuição de Leads por Qualidade")
st.plotly_chart(fig_pie)

# Média de Score por Qualidade
st.header("Média de Score por Qualidade")
average_score = data.groupby('Qualidade')['lead_score'].mean().reset_index()
fig_bar_avg = px.bar(average_score, x='Qualidade', y='lead_score', color='Qualidade', title='Média de Score por Qualidade')
st.plotly_chart(fig_bar_avg)

# Gráfico de Dispersão de Score por Categoria
st.header("Dispersão de Scores por Categoria")
fig_scatter = px.scatter(data, x='Qualidade', y='lead_score', color='Qualidade', title='Dispersão de Scores por Categoria')
st.plotly_chart(fig_scatter)

# Evolução Temporal dos Scores Médios (caso tenha uma coluna de data)
if 'date' in data.columns:
    st.header("Evolução Temporal dos Scores Médios")
    data['date'] = pd.to_datetime(data['date'])  # Substitua 'date' pelo nome da coluna que contém as datas
    data.set_index('date', inplace=True)
    monthly_scores = data.resample('M')['lead_score'].mean().reset_index()

    fig_line = px.line(monthly_scores, x='date', y='lead_score', title='Evolução Temporal dos Scores Médios')
    st.plotly_chart(fig_line)



# Box Plot Interativo
st.header("Distribuição dos Scores por Qualidade")
fig_box = px.box(data, x='Qualidade', y='lead_score', color='Qualidade', title='Distribuição dos Scores por Qualidade')
st.plotly_chart(fig_box)





