# average_scores.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo

st.header("Média dos Scores por Criativo")
top_n_avg = st.slider("Selecione o número de criativos para análise", 5, 52, 10)  # Slider para escolher o top N
top_creatives = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
top_creatives.columns = ['Criativo', 'Média do Score']
top_creatives = top_creatives.nlargest(top_n_avg, 'Média do Score')  # Limitar aos N melhores

fig_avg = px.bar(top_creatives, x='Criativo', y='Média do Score',
                 title=f'Top {top_n_avg} Criativos por Média dos Scores',
                 labels={'Criativo': 'Criativo', 'Média do Score': 'Média do Score'})
fig_avg.update_layout(xaxis_title='Criativo', yaxis_title='Média do Score')
st.plotly_chart(fig_avg)
st.write("Este gráfico mostra os criativos com a maior média de scores de lead. Ajuda a identificar quais criativos têm o melhor desempenho médio.")

