import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# CSS para estilizar fundo, texto e "cards" do topo
st.markdown(
    """
    <style>
    /* Fundo geral da página */
    .reportview-container, .main, .appview-container, .stApp {
        background: #0CABA8 !important;  /* Cor teal de fundo */
        color: #FFFFFF !important;       /* Texto branco */
        padding-top: 0px !important;     /* Remove o padding do topo */
    }

    /* Remove padding lateral extra em algumas versões do Streamlit */
    .block-container {
        padding: 0rem 1rem 1rem 1rem;
    }

    /* Cartões do topo */
    .card {
        background-color: #08393B;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .card h2 {
        margin: 0;
        font-size: 1.2rem;
    }
    .card p {
        margin: 0;
        font-size: 1.0rem;
        font-weight: bold;
    }

    /* Título principal centralizado */
    .title {
        text-align: center;
        font-weight: bold;
        color: #FFFFFF;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Leitura dos dados
@st.cache
def load_data(path):
    df = pd.read_excel(path)
    df['DATA'] = pd.to_datetime(df['DATA'], format="%Y-%m-%d", errors='coerce')
    return df

df = load_data("Base.xlsx")

# Criação de colunas auxiliares e métricas
df['MÊS'] = df['DATA'].dt.month
df['ANO_NUM'] = df['DATA'].dt.year

# Exemplo de métricas que podem vir da base ou ser calculadas
ano_atual = 2025
venda_direta = "Em aberto"   # Ajuste conforme sua lógica
revenda = "Em aberto"        # Ajuste conforme sua lógica

# Faturamento total (todos os anos, ou somente o ano atual)
faturamento_total = df['VALOR'].sum()

# Título
st.markdown("<h1 class='title'>Dashboard de Vendas</h1>", unsafe_allow_html=True)

# Cards do topo
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="card">
            <h2>Ano</h2>
            <p>{ano_atual}</p>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
            <h2>Venda Direta</h2>
            <p>{venda_direta}</p>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="card">
            <h2>Revenda</h2>
            <p>{revenda}</p>
        </div>
        """, unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="card">
            <h2>Total</h2>
            <p>R$ {faturamento_total:,.2f}</p>
        </div>
        """, unsafe_allow_html=True
    )

st.write("")  # Espaço

# Faturamento por Mês (Gráfico de Linha)
df_current_year = df[df['ANO_NUM'] == ano_atual]
faturamento_mes = (
    df_current_year
    .groupby(["MÊS"])["VALOR"]
    .sum()
    .reset_index()
    .sort_values("MÊS")
)

fig_faturamento_mes = px.line(
    faturamento_mes,
    x="MÊS",
    y="VALOR",
    markers=True,
    title="Faturamento por Mês (Ano Atual)",
    labels={"MÊS": "Mês", "VALOR": "Faturamento (R$)"},
    color_discrete_sequence=["#F5E960"]  # Cor única para a linha
)

fig_faturamento_mes.update_traces(
    text=faturamento_mes["VALOR"],
    textposition="top center",
    mode="lines+markers+text",
    texttemplate="R$ %{text:,.2f}"
)

fig_faturamento_mes.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#FFFFFF",
    title_font_size=18,
    title_x=0.5,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_faturamento_mes.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(255,255,255,0.3)', 
    zeroline=False, 
    tickfont=dict(color="#FFFFFF")
)
fig_faturamento_mes.update_yaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(255,255,255,0.3)', 
    zeroline=False, 
    tickfont=dict(color="#FFFFFF")
)

# Faturamento por Região (Gráfico de Barras Horizontais)
faturamento_regiao = (
    df.groupby("REGIÃO")["VALOR"]
    .sum()
    .reset_index()
    .sort_values("VALOR", ascending=True)  # Ordena para barras de baixo p/ cima
)

fig_regiao = px.bar(
    faturamento_regiao,
    x="VALOR",
    y="REGIÃO",
    orientation='h',
    title="Faturamento por Região",
    labels={"REGIÃO": "Região", "VALOR": "Faturamento (R$)"},
    color_discrete_sequence=["#F5E960"]  # Cor única para as barras
)

fig_regiao.update_traces(
    text=faturamento_regiao["VALOR"],
    texttemplate="R$ %{text:,.2f}",
    textposition='outside',
    cliponaxis=False
)

fig_regiao.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#FFFFFF",
    title_font_size=18,
    title_x=0.5,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_regiao.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(255,255,255,0.3)',
    tickfont=dict(color="#FFFFFF")
)
fig_regiao.update_yaxes(
    showgrid=False, 
    tickfont=dict(color="#FFFFFF")
)

# Faturamento por Vendedor (Gráfico de Barras Horizontais)
faturamento_vendedor = (
    df.groupby("VENDEDOR")["VALOR"]
    .sum()
    .reset_index()
    .sort_values("VALOR", ascending=True)
)

fig_vendedor = px.bar(
    faturamento_vendedor,
    x="VALOR",
    y="VENDEDOR",
    orientation='h',
    title="Faturamento por Vendedor",
    labels={"VENDEDOR": "Vendedor", "VALOR": "Faturamento (R$)"},
    color_discrete_sequence=["#F5E960"]  # Cor única para as barras
)

fig_vendedor.update_traces(
    text=faturamento_vendedor["VALOR"],
    texttemplate="R$ %{text:,.2f}",
    textposition='outside',
    cliponaxis=False
)

fig_vendedor.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#FFFFFF",
    title_font_size=18,
    title_x=0.5,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_vendedor.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(255,255,255,0.3)',
    tickfont=dict(color="#FFFFFF")
)
fig_vendedor.update_yaxes(
    showgrid=False, 
    tickfont=dict(color="#FFFFFF")
)

# Faturamento por Cliente (Gráfico de Barras Horizontais)
faturamento_cliente = (
    df.groupby("CLIENTE")["VALOR"]
    .sum()
    .reset_index()
    .sort_values("VALOR", ascending=True)
)

fig_cliente = px.bar(
    faturamento_cliente.tail(10), # Os 10 maiores clientes
    x="VALOR",
    y="CLIENTE",
    orientation='h',
    title="Faturamento por Cliente",
    labels={"CLIENTE": "Cliente", "VALOR": "Faturamento (R$)"},
    color_discrete_sequence=["#F5E960"]  # Cor única para as barras
)

fig_cliente.update_traces(
    text=faturamento_cliente["VALOR"],
    texttemplate="R$ %{text:,.2f}",
    textposition='outside',
    cliponaxis=False
)

fig_cliente.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#FFFFFF",
    title_font_size=18,
    title_x=0.5,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_cliente.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='rgba(255,255,255,0.3)',
    tickfont=dict(color="#FFFFFF")
)
fig_cliente.update_yaxes(
    showgrid=False, 
    tickfont=dict(color="#FFFFFF")
)

# Exibição dos gráficos
st.plotly_chart(fig_faturamento_mes, use_container_width=True)
st.plotly_chart(fig_regiao, use_container_width=True)
st.plotly_chart(fig_vendedor, use_container_width=True)
st.plotly_chart(fig_cliente, use_container_width=True)
