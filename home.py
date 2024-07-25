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

# Título da aplicação
st.title("Análise de Qualidade dos Leads por Criativos")

# Mostrar os dados
st.header("Dados dos Leads")
st.write(data)

# Análise de Qualidade dos Leads por Criativo
st.header("Análise de Qualidade dos Leads por Criativo")

# Média de Score por Criativo
average_score = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_score.columns = ['Criativo', 'Média do Score']

# Exibir apenas os 10 principais criativos com maior média de score
top_creatives = average_score.nlargest(10, 'Média do Score')

st.subheader("Média de Score por Criativo (Top 10)")
st.write(top_creatives)

# Gráfico de Barras Horizontais - Média de Score por Criativo (Top 10)
fig, ax = plt.subplots()
top_creatives.plot(kind='barh', x='Criativo', y='Média do Score', ax=ax, color='skyblue')
ax.set_xlabel('Média do Score')
ax.set_title('Média de Score por Criativo (Top 10)')
st.pyplot(fig)

# Boxplot para visualizar a distribuição dos scores por criativo (Top 10)
st.subheader("Distribuição dos Scores por Criativo (Top 10)")
fig, ax = plt.subplots(figsize=(12, 6))
top_creatives_names = top_creatives['Criativo'].tolist()
filtered_data = data[data['data.ad_name'].isin(top_creatives_names)]
filtered_data.boxplot(column='lead_score', by='data.ad_name', ax=ax, grid=False)
ax.set_title('Distribuição dos Scores por Criativo (Top 10)')
ax.set_xlabel('Criativo')
ax.set_ylabel('Lead Score')
plt.suptitle('')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Análise adicional: Distribuição dos Scores por Criativo
st.subheader("Distribuição dos Scores por Criativo")
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

# Distribuição Geral dos Scores
st.subheader("Distribuição Geral dos Scores")
fig, ax = plt.subplots()
data['lead_score'].hist(ax=ax, bins=30, color='lightcoral')
ax.set_title('Distribuição Geral dos Scores')
ax.set_xlabel('Score')
ax.set_ylabel('Frequência')
st.pyplot(fig)

# Análise de Outliers por Criativo
st.subheader("Análise de Outliers por Criativo")
outliers = data[(data['lead_score'] > data['lead_score'].quantile(0.95)) | (data['lead_score'] < data['lead_score'].quantile(0.05))]
outliers_count = outliers.groupby('data.ad_name').size().reset_index(name='Número de Outliers')
top_outliers_creatives = outliers_count.nlargest(10, 'Número de Outliers')

st.write(top_outliers_creatives)

# Gráfico de Barras - Número de Outliers por Criativo (Top 10)
st.subheader("Número de Outliers por Criativo (Top 10)")
fig, ax = plt.subplots()
top_outliers_creatives.plot(kind='barh', x='data.ad_name', y='Número de Outliers', ax=ax, color='salmon')
ax.set_xlabel('Número de Outliers')
ax.set_title('Número de Outliers por Criativo (Top 10)')
st.pyplot(fig)

# Top 10 Criativos por Mediana dos Scores
top_creatives_median = data.groupby('data.ad_name')['lead_score'].median().reset_index()
st.subheader("Top 10 Criativos por Mediana dos Scores")
st.write(top_creatives_median.nlargest(10, 'lead_score'))

# Top 10 Criativos por Desvio Padrão dos Scores
top_creatives_std = data.groupby('data.ad_name')['lead_score'].std().reset_index()
st.subheader("Top 10 Criativos por Desvio Padrão dos Scores")
st.write(top_creatives_std.nlargest(10, 'lead_score'))

# Análise da Moda por Criativo
st.subheader("Moda dos Criativos")
# Contar a frequência dos criativos
creative_counts = data['data.ad_name'].value_counts().reset_index()
creative_counts.columns = ['Criativo', 'Frequência']

# Mostrar a tabela dos criativos mais frequentes
st.write(creative_counts)

# Gráfico de Barras - Moda dos Criativos
fig, ax = plt.subplots(figsize=(12, 8))
creative_counts.head(10).plot(kind='barh', x='Criativo', y='Frequência', ax=ax, color='skyblue', legend=False)
ax.set_xlabel('Frequência')
ax.set_ylabel('Criativo')
ax.set_title('Moda dos Criativos')
for i in ax.containers:
    ax.bar_label(i, label_type="edge")
st.pyplot(fig)

# Isolando os criativos mais frequentes e pegando as informações de lead score
st.subheader("Informações de Lead Score para os Criativos Mais Frequentes")

# Selecionar os criativos mais frequentes
top_creatives_list = creative_counts.head(10)['Criativo'].tolist()

# Filtrar os dados para esses criativos
top_creatives_data = data[data['data.ad_name'].isin(top_creatives_list)]

# Mostrar a tabela filtrada
st.write(top_creatives_data)

# Gráfico de Boxplot - Lead Scores dos Criativos Mais Frequentes
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='data.ad_name', y='lead_score', data=top_creatives_data, ax=ax, palette='Set3')
ax.set_title('Distribuição dos Lead Scores para os Criativos Mais Frequentes')
ax.set_xlabel('Criativo')
ax.set_ylabel('Lead Score')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)


# Isolando os criativos menos frequentes
st.subheader("Informações de Lead Score para os Criativos Menos Frequentes")

# Selecionar os criativos menos frequentes
bottom_creatives_list = creative_counts.tail(10)['Criativo'].tolist()

# Filtrar os dados para esses criativos
bottom_creatives_data = data[data['data.ad_name'].isin(bottom_creatives_list)]

# Mostrar a tabela filtrada
st.write(bottom_creatives_data)

# Gráfico de Boxplot - Lead Scores dos Criativos Menos Frequentes
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='data.ad_name', y='lead_score', data=bottom_creatives_data, ax=ax, palette='Set3')
ax.set_title('Distribuição dos Lead Scores para os Criativos Menos Frequentes')
ax.set_xlabel('Criativo')
ax.set_ylabel('Lead Score')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Gráfico de Barras - Média de Lead Scores dos Criativos Menos Frequentes
average_score_bottom_creatives = bottom_creatives_data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_score_bottom_creatives.columns = ['Criativo', 'Média do Score']

fig, ax = plt.subplots()
average_score_bottom_creatives.plot(kind='barh', x='Criativo', y='Média do Score', ax=ax, color='skyblue')
ax.set_xlabel('Média do Score')
ax.set_title('Média de Lead Scores para os Criativos Menos Frequentes')
st.pyplot(fig)

# Grupo dos piores lead_scores e o anúncio linkado a eles
st.subheader("Piores Lead Scores e os Anúncios Linkados a Eles")

# Selecionar os piores lead_scores (por exemplo, os 10% menores scores)
worst_scores_threshold = data['lead_score'].quantile(0.1)
worst_scores_data = data[data['lead_score'] <= worst_scores_threshold]

# Mostrar a tabela dos piores lead_scores e seus anúncios
st.write(worst_scores_data)

# Gráfico de Boxplot - Lead Scores dos Criativos Menos Frequentes
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='data.ad_name', y='lead_score', data=bottom_creatives_data, ax=ax, palette='Set3')
ax.set_title('Distribuição dos Lead Scores para os Criativos Menos Frequentes')
ax.set_xlabel('Criativo')
ax.set_ylabel('Lead Score')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)


# Seleção dos Piores Lead Scores
st.subheader("Pior Lead Scores entre Criativos Menos Frequentes")

# Quantil para selecionar os piores lead scores
worst_scores_threshold = data['lead_score'].quantile(0.1)
worst_scores_bottom_creatives_data = bottom_creatives_data[bottom_creatives_data['lead_score'] <= worst_scores_threshold]

st.write(worst_scores_bottom_creatives_data)

