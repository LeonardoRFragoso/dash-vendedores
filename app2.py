import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "base-vendedores.xlsx"
    df = pd.read_excel(file_path, sheet_name="Base")
    return df

df = load_data()

# Layout do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Gráfico: Faturamento por vendedor
st.header("Faturamento por Vendedor")
faturamento_vendedor = df.groupby("VENDEDOR")["VALOR"].sum().reset_index()
fig1 = px.bar(faturamento_vendedor, x="VENDEDOR", y="VALOR", title="Faturamento por Vendedor")
st.plotly_chart(fig1)

# Gráfico: Comparação entre Faturamento e Meta Mensal
st.header("Faturamento vs Meta Mensal")
df_meta = df.groupby("VENDEDOR")["VALOR"].sum().reset_index()
df_meta["META MÊS"] = df.groupby("VENDEDOR")["META MÊS"].max().values
fig2 = px.bar(df_meta, x="VENDEDOR", y=["VALOR", "META MÊS"], title="Faturamento vs Meta")
st.plotly_chart(fig2)

# Gráfico: Taxa de conversão de leads
st.header("Taxa de Conversão de Leads")
df_leads = df.groupby("VENDEDOR")[["QUANTIDADE LEADS DIA", "QUANTIDADE NEGOCIAÇÕES DIA"]].sum().reset_index()
fig3 = px.bar(df_leads, x="VENDEDOR", y=["QUANTIDADE LEADS DIA", "QUANTIDADE NEGOCIAÇÕES DIA"],
              title="Leads Recebidos vs Negociações Fechadas")
st.plotly_chart(fig3)

# Gráfico: Vendas por meio de pagamento
st.header("Distribuição das Vendas por Forma de Pagamento")
fig4 = px.pie(df, names="FORMA PAGAMENTO", values="VALOR", title="Vendas por Forma de Pagamento")
st.plotly_chart(fig4)

# Gráfico: Vendas por tipo de produto
st.header("Distribuição das Vendas por Tipo de Produto")
fig5 = px.bar(df.groupby("PRODUTO")["VALOR"].sum().reset_index(), x="PRODUTO", y="VALOR", title="Vendas por Tipo de Produto")
st.plotly_chart(fig5)

# Gráfico: Vendas por região
st.header("Vendas por Região")
fig6 = px.bar(df.groupby("REGIÃO")["VALOR"].sum().reset_index(), x="REGIÃO", y="VALOR", title="Vendas por Região")
st.plotly_chart(fig6)

# Gráfico: Evolução das vendas ao longo do tempo
st.header("Evolução das Vendas Mensais")
df["DATA"] = pd.to_datetime(df["DATA"])
df["MÊS"] = df["DATA"].dt.strftime("%Y-%m")
faturamento_mes = df.groupby("MÊS")["VALOR"].sum().reset_index()
fig7 = px.line(faturamento_mes, x="MÊS", y="VALOR", title="Evolução das Vendas Mensais")
st.plotly_chart(fig7)