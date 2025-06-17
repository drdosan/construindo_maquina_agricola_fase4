import joblib
import pandas as pd

def prever(amostra):
    # Carrega o modelo treinado
    modelo = joblib.load("modelo_irrigacao.pkl")

    # Define os nomes das colunas esperadas
    colunas = ["valor_umidade", "valor_ph", "valor_fosforo", "valor_potassio"]

    # Transforma a amostra em DataFrame com nomes das features
    entrada_df = pd.DataFrame([amostra], columns=colunas)

    # Realiza a predição
    resultado = modelo.predict(entrada_df)
    prob = modelo.predict_proba(entrada_df)[0]

    print("🔍 Resultado:", "Irrigar" if resultado[0] else "Não irrigar")
    print("Probabilidade:", prob)

# Exemplo de uso:
if __name__ == "__main__":
    entrada = [28.5, 6.8, 1, 1]  # umidade, ph, fósforo, potássio
    prever(entrada)
