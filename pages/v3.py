import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
fig, ax = plt.subplots()
lead_counts.plot(kind='bar', x='Qualidade', y='Contagem', ax=ax, color='skyblue', legend=False)
ax.set_xlabel('Qualidade')
ax.set_ylabel('Contagem')
ax.set_title('Contagem de Leads por Qualidade')
st.pyplot(fig)

# Gráfico de Pizza - Distribuição de Leads por Qualidade
st.header("Distribuição de Leads por Qualidade")
fig_pie = px.pie(lead_counts, values='Contagem', names='Qualidade', title="Distribuição de Leads por Qualidade")
st.plotly_chart(fig_pie)

# Média de Score por Qualidade
st.header("Média de Score por Qualidade")
average_score = data.groupby('Qualidade')['lead_score'].mean().reset_index()
fig, ax = plt.subplots()
average_score.plot(kind='bar', x='Qualidade', y='lead_score', ax=ax, color='lightgreen', legend=False)
ax.set_xlabel('Qualidade')
ax.set_ylabel('Média do Score')
ax.set_title('Média de Score por Qualidade')
st.pyplot(fig)

# Evolução Temporal dos Scores Médios (caso tenha uma coluna de data)
if 'date' in data.columns:
    st.header("Evolução Temporal dos Scores Médios")
    data['date'] = pd.to_datetime(data['date'])  # Substitua 'date' pelo nome da coluna que contém as datas
    data.set_index('date', inplace=True)
    monthly_scores = data.resample('M')['lead_score'].mean().reset_index()

    fig, ax = plt.subplots()
    monthly_scores.plot(x='date', y='lead_score', ax=ax, color='purple', legend=False)
    ax.set_xlabel('Data')
    ax.set_ylabel('Score Médio')
    ax.set_title('Evolução Temporal dos Scores Médios')
    st.pyplot(fig)

# Distribuição Geral dos Scores
st.header("Distribuição Geral dos Scores")
fig, ax = plt.subplots()
data['lead_score'].hist(ax=ax, bins=30, color='lightcoral')
ax.set_title('Distribuição Geral dos Scores')
ax.set_xlabel('Score')
ax.set_ylabel('Frequência')
st.pyplot(fig)


