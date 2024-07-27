import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

st.header("Análise de Qualidade dos Leads por Criativo")

# Média de Score por Criativo
average_score = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_score.columns = ['Criativo', 'Média do Score']

# Exibir apenas os 10 principais criativos com maior média de score
top_creatives = average_score.nlargest(10, 'Média do Score')

# Análise adicional: Distribuição dos Scores por Criativo
st.subheader("Distribuição dos Scores por Criativo")
selected_creative = st.selectbox("Selecione um Criativo", data['data.ad_name'].unique())

filtered_data = data[data['data.ad_name'] == selected_creative]

st.write(f"Distribuição dos Scores para o Criativo: {selected_creative}")
st.write(filtered_data['lead_score'].describe())

# Histograma dos Scores para o Criativo Selecionado com Plotly
fig_hist_creative = go.Figure(data=[go.Histogram(x=filtered_data['lead_score'], nbinsx=20, marker_color='lightgreen')])
fig_hist_creative.update_layout(
    title=f'Distribuição dos Scores para {selected_creative}',
    xaxis_title='Score',
    yaxis_title='Frequência',
    bargap=0.2
)
st.plotly_chart(fig_hist_creative)

# Distribuição Geral dos Scores
st.header("Distribuição Geral dos Scores")

fig_hist_general = go.Figure(data=[go.Histogram(x=data['lead_score'], nbinsx=30, marker_color='lightcoral')])
fig_hist_general.update_layout(
    title='Distribuição Geral dos Scores',
    xaxis_title='Lead Score',
    yaxis_title='Contagem',
    bargap=0.2
)
st.plotly_chart(fig_hist_general)
