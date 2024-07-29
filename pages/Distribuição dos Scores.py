import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carregar dados
data = pd.read_csv('final_lead_scores.csv')  # Substitua pelo nome do seu arquivo



# Média de Score por Criativo
average_score = data.groupby('data.ad_name')['lead_score'].mean().reset_index()
average_score.columns = ['Criativo', 'Média do Score']

# Exibir apenas os 10 principais criativos com maior média de score
top_creatives = average_score.nlargest(10, 'Média do Score')


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



# Seção de Comparação
st.header("Comparação de Distribuição dos Scores entre Criativos")

# Seleção de múltiplos criativos para comparação
selected_creatives = st.multiselect(
    "Selecione os Criativos para Comparação",
    options=data['data.ad_name'].unique(),
    default=top_creatives['Criativo'].head(2).tolist()  # Valor default é 2 criativos
)

if len(selected_creatives) > 0:
    st.subheader("Distribuição dos Scores para os Criativos Selecionados")

    # Criar DataFrames para os criativos selecionados
    comparison_data = {creative: data[data['data.ad_name'] == creative]['lead_score'] for creative in selected_creatives}

    # Calcular as estatísticas descritivas para os criativos selecionados
    comparison_stats = {}
    for creative, scores in comparison_data.items():
        stats = scores.describe(percentiles=[.25, .5, .75]).to_frame().T
        stats.index = [creative]
        comparison_stats[creative] = stats

    # Concatenar as estatísticas em um único DataFrame
    comparison_stats_df = pd.concat(comparison_stats.values(), keys=comparison_stats.keys())

    # Exibir tabelas com estatísticas descritivas verticalmente
    st.write("Estatísticas Descritivas para os Criativos Selecionados:")

    # Criar colunas para exibir as tabelas lado a lado
    cols = st.columns(len(selected_creatives))
    
    for idx, creative in enumerate(selected_creatives):
        with cols[idx]:
            st.write(f"**{creative}**")
            # Exibir tabela transposta
            st.dataframe(comparison_stats_df.loc[creative].T, use_container_width=True)

    # Criar gráficos de comparação lado a lado
    st.subheader("Distribuição dos Scores - Comparação dos Criativos Selecionados")

    # Criação das figuras de histogramas
    fig_hist_comparisons = go.Figure()

    for creative in selected_creatives:
        fig_hist_comparisons.add_trace(
            go.Histogram(
                x=comparison_data[creative],
                nbinsx=20,
                name=creative,
                opacity=0.75
            )
        )
    
    fig_hist_comparisons.update_layout(
        title='Distribuição dos Scores para os Criativos Selecionados',
        xaxis_title='Score',
        yaxis_title='Frequência',
        barmode='overlay',
        bargap=0.2
    )

    st.plotly_chart(fig_hist_comparisons, use_container_width=True)

else:
    st.write("Selecione pelo menos um criativo para comparação.")
