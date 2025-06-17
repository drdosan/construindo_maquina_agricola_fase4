#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// === Definições de pinos e sensores ===
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
LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long ultimoToggle = 0;
bool fosforo = false;
bool potassio = false;

// === Setup ===
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

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("FarmTech Init...");
  delay(1500);
  lcd.clear();
}

// === Verifica se pode irrigar via API ===
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

// === Atualiza informações no LCD ===
void atualizarLCD(float umidade, float ph, bool fosforo, bool potassio, bool irrigando) {
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Umid:");
  lcd.print((int)umidade);
  lcd.print("% PH:");
  lcd.print(ph, 1);

  lcd.setCursor(0, 1);
  lcd.print("F:");
  lcd.print(fosforo ? "1" : "0");
  lcd.print(" P:");
  lcd.print(potassio ? "1" : "0");
  lcd.print(" IRR:");
  lcd.print(irrigando ? "SIM" : "NAO");
}

// === Loop principal ===
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

        atualizarLCD(umidade, ph, fosforo, potassio, true);
        http.end();
      } else {
        Serial.println("🌧️ Irrigação suspensa por previsão de chuva.");
        atualizarLCD(umidade, ph, fosforo, potassio, false);
      }
    } else {
      Serial.println("⚠️ Wi-Fi desconectado");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Wi-Fi Desconectado");
    }
  } else {
    Serial.println("⚠️ Leitura inválida dos sensores");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Erro sensores");
  }

  delay(5000);
}
