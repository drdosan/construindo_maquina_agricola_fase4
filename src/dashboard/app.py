import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Dashboard Irrigação", layout="wide")
st.title("🌿 Dashboard do Sistema de Irrigação Inteligente")

# ====================
# 🔌 Funções de carga
# ====================
@st.cache_data
def carregar_leituras():
    url = "http://192.168.0.151:5000/leituras"
    response = requests.get(url)
    return pd.DataFrame(response.json())

@st.cache_data
def carregar_sensores_instalados():
    url = "http://192.168.0.151:5000/sensores-instalados"
    response = requests.get(url)
    return pd.DataFrame(response.json())

@st.cache_data
def carregar_sensores():
    url = "http://192.168.0.151:5000/sensores"
    response = requests.get(url)
    return pd.DataFrame(response.json())

# ====================
# 📥 Carregar dados
# ====================
df = carregar_leituras()
sensores_instalados = carregar_sensores_instalados()
sensores = carregar_sensores()

# ====================
# 🔗 Mesclar nomes dos sensores
# ====================
df = df.merge(sensores_instalados[['cd_sensor_instalado', 'cd_sensor']], on='cd_sensor_instalado', how='left')
df = df.merge(sensores[['cd_sensor', 'nome']], on='cd_sensor', how='left')

# ====================
# 🧼 Renomear e reorganizar
# ====================
df = df.rename(columns={
    'nome': 'Sensor',
    'data_hora': 'Data/Hora',
    'valor_umidade': 'Umidade',
    'valor_ph': 'pH',
    'valor_fosforo': 'Fósforo',
    'valor_potassio': 'Potássio'
})

df = df[['Sensor', 'Data/Hora', 'Umidade', 'pH', 'Fósforo', 'Potássio']]

# ====================
# 📈 Gráficos
# ====================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Umidade do Solo")
    fig = px.line(df, x="Data/Hora", y="Umidade", color="Sensor", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("pH do Solo")
    fig = px.line(df, x="Data/Hora", y="pH", color="Sensor", markers=True)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Nutrientes (Fósforo e Potássio)")
fig = px.line(df, x="Data/Hora", y=["Fósforo", "Potássio"], color="Sensor", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ====================
# 📋 Tabela
# ====================
st.subheader("📋 Leituras completas")
st.dataframe(df)
