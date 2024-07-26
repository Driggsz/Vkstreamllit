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

# Contar os leads em cada categoria
lead_counts = data['Qualidade'].value_counts().reset_index()
lead_counts.columns = ['Qualidade', 'Contagem']

# Título da aplicação
st.title("Análise de Qualidade dos Leads")

# Mostrar os dados
st.header("Dados dos Leads")
st.write(data)

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

# Análise de Qualidade dos Leads por Criativo
st.header("Análise de Qualidade dos Leads por Criativo")

# Média de Score por Criativo
average_score = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_score.columns = ['Criativo', 'Média do Score']

# Categorizar os criativos em Top 10 e Bottom 10
top_creatives = average_score.nlargest(10, 'Média do Score')
bottom_creatives = average_score.nsmallest(10, 'Média do Score')

# Mostrar os Top 10 criativos
st.subheader("Top 10 Criativos por Média de Score")
st.write(top_creatives)

# Gráfico de Barras Horizontais - Média de Score por Criativo (Top 10)
fig, ax = plt.subplots()
top_creatives.plot(kind='barh', x='Criativo', y='Média do Score', ax=ax, color='skyblue', legend=False)
ax.set_xlabel('Média do Score')
ax.set_title('Média de Score por Criativo (Top 10)')
st.pyplot(fig)

# Mostrar os Bottom 10 criativos
st.subheader("Bottom 10 Criativos por Média de Score")
st.write(bottom_creatives)

# Gráfico de Barras Horizontais - Média de Score por Criativo (Bottom 10)
fig, ax = plt.subplots()
bottom_creatives.plot(kind='barh', x='Criativo', y='Média do Score', ax=ax, color='lightcoral', legend=False)
ax.set_xlabel('Média do Score')
ax.set_title('Média de Score por Criativo (Bottom 10)')
st.pyplot(fig)

# Distribuição dos Scores por Criativo
st.header("Distribuição dos Scores por Criativo")
selected_creative = st.selectbox("Selecione um Criativo", data['data.ad_name'].unique())
filtered_data = data[data['data.ad_name'] == selected_creative]

st.write(f"Distribuição dos Scores para o Criativo: {selected_creative}")
st.write(filtered_data['lead_score'].describe())

# Histograma dos Scores para o Criativo Selecionado
fig, ax = plt.subplots()
filtered_data['lead_score'].hist(ax=ax, bins=20, color='lightgreen')
ax.set_title(f'Distribuição dos Scores para {selected_creative}')
ax.set_xlabel('Score')
ax.set_ylabel('Frequência')
st.pyplot(fig)

# Análise da Distribuição Geral dos Scores
st.header("Distribuição Geral dos Scores")
fig, ax = plt.subplots()
data['lead_score'].hist(ax=ax, bins=30, color='lightcoral')
ax.set_title('Distribuição Geral dos Scores')
ax.set_xlabel('Score')
ax.set_ylabel('Frequência')
st.pyplot(fig)
