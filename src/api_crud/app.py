from flask import Flask, request, jsonify
import pymysql
from datetime import datetime
from flasgger import Swagger, swag_from
import requests

app = Flask(__name__)
template = {
    "swagger": "2.0",
    "info": {
        "title": "API ESP32 + Flask - Irrigação Inteligente",
        "description": "Documentação da API de sensores agrícolas conectados via ESP32.",
        "version": "1.0.0"
    },
    "basePath": "/",  # raiz da API
    "schemes": [
        "http"
    ]
}

swagger = Swagger(app, template=template)

API_KEY = "376b94e3d3f0dab77f7653f5d661c43e"
CIDADE = "São Paulo"
URL_CLIMA = f"https://api.openweathermap.org/data/2.5/forecast?q={CIDADE}&appid={API_KEY}&lang=pt_br&units=metric"

# CONFIGURAÇÕES DO MYSQL
def get_connection():
    return pymysql.connect(
        host='192.185.217.47',
        user='bsconsul_fiap',
        password='Padr@ao321',
        database='bsconsul_fiap',
        cursorclass=pymysql.cursors.DictCursor
    )

def vai_chover():
    resp = requests.get(URL_CLIMA)
    dados = resp.json()
    for previsao in dados["list"][:8]:  # próximas 24h
        if 'rain' in previsao and previsao['rain'].get('3h', 0) > 0:
            return True
    return False    

# ========================= PRODUTOR =========================

@app.route('/produtores', methods=['POST'])
@swag_from({
    'tags': ['Produtor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'properties': {
                'nome': {'type': 'string'},
                'fazenda': {'type': 'string'},
                'localizacao': {'type': 'string'}
            },
            'required': ['nome', 'fazenda', 'localizacao']
        }
    }],
    'responses': {
        201: {'description': 'Produtor criado com sucesso'}
    }
})
def create_produtor():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO PRODUTOR (nome, fazenda, localizacao) VALUES (%s, %s, %s)",
                        (data['nome'], data['fazenda'], data['localizacao']))
        conn.commit()
    return jsonify({'message': 'Produtor criado com sucesso'}), 201

@app.route('/produtores', methods=['GET'])
@swag_from({'tags': ['Produtor'], 'responses': {200: {'description': 'Lista de produtores'}}})
def get_produtores():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM PRODUTOR")
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/produtores/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Produtor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'properties': {
                'nome': {'type': 'string'},
                'fazenda': {'type': 'string'},
                'localizacao': {'type': 'string'}
            }
        }
    }],
    'responses': {200: {'description': 'Produtor atualizado'}}
})
def update_produtor(id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE PRODUTOR SET nome=%s, fazenda=%s, localizacao=%s WHERE cd_produtor=%s",
                        (data['nome'], data['fazenda'], data['localizacao'], id))
        conn.commit()
    return jsonify({'message': 'Produtor atualizado'})

@app.route('/produtores/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Produtor'], 'responses': {200: {'description': 'Produtor deletado'}}})
def delete_produtor(id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PRODUTOR WHERE cd_produtor=%s", (id,))
        conn.commit()
    return jsonify({'message': 'Produtor deletado'})

# ========================= CULTURA =========================

@app.route('/culturas', methods=['POST'])
@swag_from({
    'tags': ['Cultura'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'properties': {
                'cd_cultura': {'type': 'integer'},
                'cd_produtor': {'type': 'integer'},
                'nome': {'type': 'string'},
                'tipo': {'type': 'string'}
            },
            'required': ['cd_cultura', 'cd_produtor', 'nome', 'tipo']
        }
    }],
    'responses': {201: {'description': 'Cultura criada com sucesso'}}
})
def create_cultura():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO CULTURA (cd_cultura, cd_produtor, nome, tipo) VALUES (%s, %s, %s, %s)",
                        (data['cd_cultura'], data['cd_produtor'], data['nome'], data['tipo']))
        conn.commit()
    return jsonify({'message': 'Cultura criada com sucesso'}), 201

@app.route('/culturas', methods=['GET'])
@swag_from({'tags': ['Cultura'], 'responses': {200: {'description': 'Lista de culturas'}}})
def get_culturas():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM CULTURA")
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/culturas/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Cultura'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_produtor': {'type': 'integer'},
                'nome': {'type': 'string'},
                'tipo': {'type': 'string'}
            }
        }
    }],
    'responses': {200: {'description': 'Cultura atualizada'}}
})
def update_cultura(id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE CULTURA SET cd_produtor=%s, nome=%s, tipo=%s WHERE cd_cultura=%s",
                        (data['cd_produtor'], data['nome'], data['tipo'], id))
        conn.commit()
    return jsonify({'message': 'Cultura atualizada'})

@app.route('/culturas/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Cultura'], 'responses': {200: {'description': 'Cultura deletada'}}})
def delete_cultura(id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM CULTURA WHERE cd_cultura=%s", (id,))
        conn.commit()
    return jsonify({'message': 'Cultura deletada'})

# ========================= SENSOR =========================

@app.route('/sensores', methods=['POST'])
@swag_from({
    'tags': ['Sensor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_sensor': {'type': 'integer'},
                'tipo': {'type': 'string'},
                'nome': {'type': 'string'}
            }
        }
    }],
    'responses': {201: {'description': 'Sensor criado com sucesso'}}
})
def create_sensor():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO SENSOR (cd_sensor, tipo, nome) VALUES (%s, %s, %s)",
                        (data['cd_sensor'], data['tipo'], data['nome']))
        conn.commit()
    return jsonify({'message': 'Sensor criado com sucesso'})

@app.route('/sensores', methods=['GET'])
@swag_from({'tags': ['Sensor'], 'responses': {200: {'description': 'Lista de sensores'}}})
def get_sensores():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM SENSOR")
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/sensores/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Sensor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'tipo': {'type': 'string'},
                'nome': {'type': 'string'}
            }
        }
    }],
    'responses': {200: {'description': 'Sensor atualizado'}}
})
def update_sensor(id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE SENSOR SET tipo=%s, nome=%s WHERE cd_sensor=%s",
                        (data['tipo'], data['nome'], id))
        conn.commit()
    return jsonify({'message': 'Sensor atualizado'})

@app.route('/sensores/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Sensor'], 'responses': {200: {'description': 'Sensor deletado'}}})
def delete_sensor(id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM SENSOR WHERE cd_sensor=%s", (id,))
        conn.commit()
    return jsonify({'message': 'Sensor deletado'})

# ================= SENSOR INSTALADO =================

@app.route('/sensores-instalados', methods=['POST'])
@swag_from({
    'tags': ['Sensor Instalado'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_sensor_instalado': {'type': 'integer'},
                'cd_cultura': {'type': 'integer'},
                'cd_sensor': {'type': 'integer'},
                'data_instalacao': {'type': 'string', 'format': 'date'}
            }
        }
    }],
    'responses': {201: {'description': 'Sensor instalado com sucesso'}}
})
def create_sensor_instalado():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO SENSOR_INSTALADO (cd_sensor_instalado, cd_cultura, cd_sensor, data_instalacao) VALUES (%s, %s, %s, %s)",
                        (data['cd_sensor_instalado'], data['cd_cultura'], data['cd_sensor'], data['data_instalacao']))
        conn.commit()
    return jsonify({'message': 'Sensor instalado com sucesso'})

@app.route('/sensores-instalados', methods=['GET'])
@swag_from({'tags': ['Sensor Instalado'], 'responses': {200: {'description': 'Lista de sensores instalados'}}})
def get_sensores_instalados():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM SENSOR_INSTALADO")
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/sensores-instalados/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Sensor Instalado'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_cultura': {'type': 'integer'},
                'cd_sensor': {'type': 'integer'},
                'data_instalacao': {'type': 'string', 'format': 'date'}
            }
        }
    }],
    'responses': {200: {'description': 'Sensor instalado atualizado'}}
})
def update_sensor_instalado(id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE SENSOR_INSTALADO SET cd_cultura=%s, cd_sensor=%s, data_instalacao=%s WHERE cd_sensor_instalado=%s",
                        (data['cd_cultura'], data['cd_sensor'], data['data_instalacao'], id))
        conn.commit()
    return jsonify({'message': 'Sensor instalado atualizado'})

@app.route('/sensores-instalados/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Sensor Instalado'], 'responses': {200: {'description': 'Sensor instalado deletado'}}})
def delete_sensor_instalado(id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM SENSOR_INSTALADO WHERE cd_sensor_instalado=%s", (id,))
        conn.commit()
    return jsonify({'message': 'Sensor instalado deletado'})

# ================= LEITURA SENSOR =================

@app.route('/leituras', methods=['POST'])
@swag_from({
    'tags': ['Leitura Sensor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_sensor_instalado': {'type': 'integer'},
                'valor_umidade': {'type': 'number'},
                'valor_ph': {'type': 'number'},
                'valor_fosforo': {'type': 'number'},
                'valor_potassio': {'type': 'number'}
            }
        }
    }],
    'responses': {201: {'description': 'Leitura registrada com sucesso'}}
})
def create_leitura():
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO LEITURA_SENSOR (cd_sensor_instalado, data_hora, valor_umidade, valor_ph, valor_fosforo, valor_potassio)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['cd_sensor_instalado'], datetime.now(), data['valor_umidade'],
                  data['valor_ph'], data['valor_fosforo'], data['valor_potassio']))
        conn.commit()
    return jsonify({'message': 'Leitura registrada com sucesso'})

@app.route('/leituras', methods=['GET'])
@swag_from({'tags': ['Leitura Sensor'], 'responses': {200: {'description': 'Lista de leituras'}}})
def get_leituras():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM LEITURA_SENSOR")
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/leituras/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Leitura Sensor'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'properties': {
                'cd_sensor_instalado': {'type': 'integer'},
                'data_hora': {'type': 'string', 'format': 'date-time'},
                'valor_umidade': {'type': 'number'},
                'valor_ph': {'type': 'number'},
                'valor_fosforo': {'type': 'number'},
                'valor_potassio': {'type': 'number'}
            }
        }
    }],
    'responses': {200: {'description': 'Leitura atualizada'}}
})
def update_leitura(id):
    data = request.json
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE LEITURA_SENSOR SET cd_sensor_instalado=%s, data_hora=%s, valor_umidade=%s, valor_ph=%s, valor_fosforo=%s, valor_potassio=%s
                WHERE cd_leitura=%s
            """, (data['cd_sensor_instalado'], data['data_hora'], data['valor_umidade'],
                  data['valor_ph'], data['valor_fosforo'], data['valor_potassio'], id))
        conn.commit()
    return jsonify({'message': 'Leitura atualizada'})

@app.route('/leituras/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Leitura Sensor'], 'responses': {200: {'description': 'Leitura deletada'}}})
def delete_leitura(id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM LEITURA_SENSOR WHERE cd_leitura=%s", (id,))
        conn.commit()
    return jsonify({'message': 'Leitura deletada'})


# ================= INTEGRAÇÃO OPEN WEATHER =================
def vai_chover():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Sao Paulo,br&appid={API_KEY}&units=metric&lang=pt_br"
    resp = requests.get(url)
    dados = resp.json()

    for previsao in dados["list"][:8]:  # próximas 24h (~8 blocos de 3h)
        if 'rain' in previsao and previsao['rain'].get('3h', 0) > 0:
            return True
    return False

@app.route("/clima/prever-irrigacao", methods=["POST"])
@swag_from({
    'tags': ['Clima'],
    'responses': {
        201: {'description': 'Decisão de irrigação baseada na previsão do tempo foi salva'}
    }
})
def prever_irrigacao():
    pode_irrigar = not vai_chover()
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO DECISAO_IRRIGACAO (pode_irrigar) VALUES (%s)", (pode_irrigar,))
        conn.commit()
    return jsonify({
        "pode_irrigar": pode_irrigar,
        "mensagem": "Decisão salva com sucesso"
    }), 201

@app.route("/status-irrigacao", methods=["GET"])
@swag_from({
    'tags': ['Clima'],
    'responses': {
        200: {'description': 'Status atual da irrigação baseado na última previsão climática'}
    }
})
def status_irrigacao():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pode_irrigar FROM DECISAO_IRRIGACAO ORDER BY data_hora DESC LIMIT 1")
            row = cur.fetchone()
    return jsonify({"pode_irrigar": row["pode_irrigar"] if row else True})


# ================= RUN APP =================

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
