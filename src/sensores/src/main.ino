#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

#define PIN_FOSFORO 13
#define PIN_POTASSIO 12
#define PIN_PH A0
#define PIN_UMIDADE 4
#define DHTTYPE DHT22

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* serverUrl = "http://192.168.0.151:5000/leituras";
const char* statusUrl = "http://192.168.0.151:5000/status-irrigacao";

DHT dht(PIN_UMIDADE, DHTTYPE);
unsigned long ultimoToggle = 0;
bool fosforo = false;
bool potassio = false;

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(PIN_FOSFORO, INPUT_PULLUP);
  pinMode(PIN_POTASSIO, INPUT_PULLUP);

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("✅ Conectado!");
}

bool verificarPodeIrrigar() {
  HTTPClient http;
  http.begin(statusUrl);
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();
    StaticJsonDocument<128> doc;
    DeserializationError erro = deserializeJson(doc, payload);

    if (!erro) {
      bool pode = doc["pode_irrigar"];
      Serial.print("🔍 Status de irrigação: ");
      Serial.println(pode ? "Permitido ✅" : "Bloqueado 🚫");
      return pode;
    } else {
      Serial.println("❌ Erro ao interpretar resposta JSON");
    }
  } else {
    Serial.print("❌ Erro ao consultar status: ");
    Serial.println(httpCode);
  }

  http.end();
  return false;  // se der erro, previne irrigação
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimoToggle >= 5000) {
    fosforo = !fosforo;
    potassio = !potassio;
    ultimoToggle = agora;
  }

  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();
  int leituraPH = analogRead(PIN_PH);
  float ph = map(leituraPH, 0, 4095, 0, 140) / 10.0;

  if (!isnan(umidade) && !isnan(temperatura)) {
    if (WiFi.status() == WL_CONNECTED) {
      if (verificarPodeIrrigar()) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        StaticJsonDocument<256> json;
        json["cd_sensor_instalado"] = 1;
        json["valor_umidade"] = umidade;
        json["valor_ph"] = ph;
        json["valor_fosforo"] = fosforo ? 1 : 0;
        json["valor_potassio"] = potassio ? 1 : 0;

        String jsonString;
        serializeJson(json, jsonString);

        int httpResponseCode = http.POST(jsonString);
        Serial.print("POST enviado → Código: ");
        Serial.println(httpResponseCode);

        if (httpResponseCode > 0) {
          String resposta = http.getString();
          Serial.println("✔️ Resposta: " + resposta);
        } else {
          Serial.println("❌ Falha no envio");
        }

        http.end();
      } else {
        Serial.println("🌧️ Irrigação suspensa por previsão de chuva.");
      }
    } else {
      Serial.println("⚠️ Wi-Fi desconectado");
    }
  } else {
    Serial.println("⚠️ Leitura inválida dos sensores");
  }

  delay(5000);
}
