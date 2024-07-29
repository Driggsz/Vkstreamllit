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



# Gráfico de Pizza - Distribuição de Leads por Qualidade
st.header("Distribuição de Leads por Qualidade")
fig_pie = px.pie(lead_counts, values='Contagem', names='Qualidade', title="Distribuição de Leads por Qualidade")
st.plotly_chart(fig_pie)

# Gráfico de Barras Empilhado para Criativos e Contagem de Leads
st.header("Análise dos Criativos e Contagem de Leads")



# Assumindo que `data` é o seu DataFrame original
creative_scores = data.groupby(['data.ad_name', 'Qualidade']).size().reset_index(name='Contagem')

# Seletor para número de anúncios
num_ads = st.slider('Selecione o número de anúncios para visualizar', min_value=1, max_value=len(creative_scores['data.ad_name'].unique()), value=5)

st.write("(Foi usado o critério do número de leads por anúncio para a ordem de exibição no gráfico).")

# Filtrando os anúncios com mais contagens
top_creatives = creative_scores.groupby('data.ad_name').sum().nlargest(num_ads, 'Contagem').index
creative_scores = creative_scores[creative_scores['data.ad_name'].isin(top_creatives)]

# Normalizando as contagens para percentual
creative_scores['Percentual'] = creative_scores.groupby('data.ad_name')['Contagem'].transform(lambda x: x / x.sum() * 100)

# Ordenando criativos por contagem total (de maior para menor)
ordered_creatives = creative_scores.groupby('data.ad_name').sum().sort_values('Contagem', ascending=True).index
creative_scores['data.ad_name'] = pd.Categorical(creative_scores['data.ad_name'], categories=ordered_creatives, ordered=True)
creative_scores = creative_scores.sort_values('data.ad_name')

# Definindo o esquema de cores e a ordem das categorias
colors = {
    'Desqualificado': '#000000',
    'Baixa': '#EE4266',
    'Média': '#FFD23F',
    'Alta': '#337357'
}

# Garantir a ordem das categorias
category_order = ['Desqualificado', 'Baixa', 'Média', 'Alta']

# Gráfico de barras horizontal empilhado
fig_creative = px.bar(creative_scores, y='data.ad_name', x='Percentual', color='Qualidade', orientation='h',
                      title='Análise dos Criativos e Contagem de Leads', color_discrete_map=colors, 
                      labels={'Percentual': 'Percentual de Leads', 'data.ad_name': 'Criativo'},
                      category_orders={'Qualidade': category_order},
                      text='Contagem')

# Ajustando o eixo x para ir de 0 a 100%
fig_creative.update_layout(xaxis=dict(range=[0, 100]))

# Atualizar as barras para remover os textos das barras
fig_creative.update_traces(texttemplate='', textposition='none', 
                           selector=dict(type='bar'))

# Atualizar o layout para posicionar a legenda fora das barras
fig_creative.update_layout(legend=dict(x=1, y=1))

st.plotly_chart(fig_creative)



# Seletor de Criativos para Comparação
st.header("Comparação de Criativos")

# Obter a lista de criativos
creatives_list = data['data.ad_name'].unique()

# Seletor múltiplo para escolher criativos para comparação
selected_creatives = st.multiselect('Selecione os criativos para comparação', options=creatives_list, default=creatives_list[:1])

# Filtrando os dados para os criativos selecionados
comparison_data = data[data['data.ad_name'].isin(selected_creatives)]

# Contar o número de leads por criativo e qualidade
comparison_scores = comparison_data.groupby(['data.ad_name', 'Qualidade']).size().reset_index(name='Contagem')

# Normalizando as contagens para percentual
comparison_scores['Percentual'] = comparison_scores.groupby('data.ad_name')['Contagem'].transform(lambda x: x / x.sum() * 100)

# Gráfico de barras horizontal empilhado para comparação
fig_comparison = px.bar(comparison_scores, y='data.ad_name', x='Percentual', color='Qualidade', orientation='h',
                       title='Comparação de Criativos', color_discrete_map=colors, 
                       labels={'Percentual': 'Percentual de Leads', 'data.ad_name': 'Criativo'},
                       category_orders={'Qualidade': category_order},
                       text='Contagem')

# Ajustando o eixo x para ir de 0 a 100%
fig_comparison.update_layout(xaxis=dict(range=[0, 100]))

# Atualizar as barras para remover os textos das barras
fig_comparison.update_traces(texttemplate='', textposition='none', 
                             selector=dict(type='bar'))

# Atualizar o layout para posicionar a legenda fora das barras
fig_comparison.update_layout(legend=dict(x=1, y=1))

st.plotly_chart(fig_comparison)