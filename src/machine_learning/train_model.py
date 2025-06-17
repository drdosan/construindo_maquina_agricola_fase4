import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pymysql
import joblib
from sqlalchemy import create_engine

def get_engine():
    return create_engine("mysql+pymysql://bsconsul_fiap:Padr%40ao321@192.185.217.47/bsconsul_fiap")

def carregar_dados():
    engine = get_engine()
    query = """
        SELECT valor_umidade, valor_ph, valor_fosforo, valor_potassio
        FROM LEITURA_SENSOR
        WHERE valor_umidade IS NOT NULL
          AND valor_ph IS NOT NULL
          AND valor_fosforo IS NOT NULL
          AND valor_potassio IS NOT NULL
    """
    df = pd.read_sql(query, engine)

    print(f"✅ Registros recebidos: {len(df)}")
    print(df.head())

    return df

def treinar_modelo(df):
    # Aqui ainda não tratamos o tipo para debug puro
    if df.empty:
        print("⚠️ Nenhum dado válido para treinar o modelo.")
        return

    # Se estiver tudo certo, convertemos:
    for col in ["valor_umidade", "valor_ph", "valor_fosforo", "valor_potassio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    if df.empty:
        print("⚠️ Todos os dados foram descartados após a conversão para float.")
        return

    df["pode_irrigar"] = df["valor_umidade"] < 30

    X = df[["valor_umidade", "valor_ph", "valor_fosforo", "valor_potassio"]]
    y = df["pode_irrigar"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
    modelo.fit(X_train, y_train)

    print("=== Avaliação ===")
    print(classification_report(y_test, modelo.predict(X_test)))
    print("Matriz de confusão:")
    print(confusion_matrix(y_test, modelo.predict(X_test)))

    joblib.dump(modelo, "modelo_irrigacao.pkl")
    print("✅ Modelo salvo como 'modelo_irrigacao.pkl'")

if __name__ == "__main__":
    df = carregar_dados()
    treinar_modelo(df)
