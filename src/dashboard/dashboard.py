import streamlit as st
import pandas as pd
import pymysql
import joblib
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh


# === Conexão com o banco ===
def get_engine():
    return create_engine("mysql+pymysql://bsconsul_fiap:Padr%40ao321@192.185.217.47/bsconsul_fiap")

# === Carrega os dados mais recentes do banco ===
def carregar_dados():
    engine = get_engine()
    query = """
        SELECT data_hora, valor_umidade, valor_ph, valor_fosforo, valor_potassio
        FROM LEITURA_SENSOR
        WHERE valor_umidade IS NOT NULL
        ORDER BY data_hora DESC
        LIMIT 100
    """
    df = pd.read_sql(query, engine)

    # Remove possível linha suja
    df = df[df['data_hora'].astype(str).str.lower() != "data_hora"]

    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
    for col in ["valor_umidade", "valor_ph", "valor_fosforo", "valor_potassio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)
    df = df.sort_values("data_hora")
    return df


# === Aplica modelo ===
def aplicar_modelo(df):
    modelo = joblib.load("../machine_learning/modelo_irrigacao.pkl")
    X = df[["valor_umidade", "valor_ph", "valor_fosforo", "valor_potassio"]]
    df["previsao"] = modelo.predict(X)
    return df

# === Streamlit ===
def dashboard():
    st.set_page_config(page_title="Dashboard Irrigação", layout="wide")
    st_autorefresh(interval=10000, limit=None, key="realtime")
    st.title("🌱 Dashboard - Sistema de Irrigação Inteligente")

    df = carregar_dados()
    if df.empty:
        st.warning("Nenhum dado disponível no banco.")
        return

    df = aplicar_modelo(df)

    # Métricas principais
    col1, col2 = st.columns(2)
    col1.metric("📉 Umidade Média", f"{df['valor_umidade'].mean():.1f}%")
    col2.metric("💧 Irrigar Recomendado", f"{df['previsao'].sum()} / {len(df)}")

    # Gráfico de umidade
    st.subheader("Variação da Umidade do Solo")
    st.line_chart(df.set_index("data_hora")["valor_umidade"])

    # Parâmetros do solo
    st.subheader("📊 Parâmetros do Solo (pH, Fósforo, Potássio)")
    st.line_chart(df.set_index("data_hora")[["valor_ph", "valor_fosforo", "valor_potassio"]])

    # Gráfico de decisão do modelo
    st.subheader("🔍 Decisão do Modelo de Machine Learning")
    chart_data = df["previsao"].value_counts().rename({0: "Não Irrigar", 1: "Irrigar"})
    st.bar_chart(chart_data)

    st.caption("🔄 Atualizado com dados reais do banco MySQL.")

    st.caption("🔄 Os dados são atualizados automaticamente a cada 10 segundos.")

# Executar
if __name__ == '__main__':
    dashboard()
