# FIAP - Faculdade de Informática e Administração Paulista 

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# 🌿 Construindo Máquina Agrícola Inteligente - Fase 4


## Grupo 6

## 👨‍🎓 Integrantes: 
| Matrícula                 | Aluno               						  |
|---------------------------|---------------------------------------------|
|        RM 565150          | Andre de Oliveira Santos Burger			  |
|        RM 565497          | Vera Maria Chaves de Souza				  | 
|        RM 565286          | Diogo Rebello dos Santos					  |
|        RM 565555          | Marcos Vinícius dos Santos Fernandes		  |


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="#">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="#">André Godoi Chiovato</a>


## 📜 Descrição

Projeto acadêmico dividido em duas fases principais: **coleta de dados ambientais com ESP32** e **armazenamento/processamento via API Flask com banco SQL**. O objetivo é aplicar conceitos de automação, IoT e persistência de dados para ambientes agrícolas.

## 📁 Estrutura de pastas

```
construindo_maquina_agricola/
├── sensores/
│   ├── main.ino
│   └── simulacao_esp32.png
│
├── api_crud/
│   ├── app.py
│   └── requirements.txt
│
├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```


- `sensores/`: Projeto da Fase 1, com o código C/C++ do ESP32 e imagem do circuito Wokwi.
- `api_crud/`: Projeto da Fase 2, com a API Flask documentada com Swagger.
- `dashboard/`: Projeto “Ir Além”, com dashboard interativo em Streamlit.
- `main.ino`: Código-fonte responsável pela leitura dos sensores e envio dos dados via HTTP.
- `simulacao_esp32.png`: Imagem ilustrativa da montagem simulada no Wokwi.
- `app.py`: Código principal da API ou dashboard, dependendo da pasta.
- `requirements.txt`: Dependências de cada módulo.
- `.gitignore`: Arquivos e pastas ignorados pelo Git.
- `README.md`: Este documento com explicações completas do projeto.

## 🚀 Entrega 1: Sistema de Sensores e Controle com ESP32

Nesta primeira fase, desenvolvemos um sistema de monitoramento e automação para plantio inteligente utilizando o ESP32 e sensores simulados.

### ✅ Metas:

- Construção do circuito de sensores no [Wokwi](https://wokwi.com/)
- Código em C/C++ utilizando PlatformIO
- Acionamento automático de um relé (bomba de irrigação)
- Comentários no código explicando a lógica
- Registro e documentação da montagem no README

### 🔌 Componentes simulados:

- Sensor de umidade
- Sensor de pH
- Relé de irrigação
- ESP32 DevKit v1

### 🖼️ Circuito no Wokwi:

<img src="assets/simulacao_esp32.png" alt="Simulação ESP32 no Wokwi" width="600"/>

### 📂 Entregáveis:

- `main.ino` com o código completo e comentado
- `simulacao_esp32.png` com a imagem do circuito
- Documentação explicando o funcionamento

---

## 💾 Entrega 2: Armazenamento de Dados em Banco SQL com Python

A segunda fase consiste em simular o envio dos dados dos sensores para um sistema de banco de dados por meio de uma API RESTful em Python com Flask.

### ✅ Metas:

- Captura de dados do ESP32 por requisições HTTP
- API Flask conectada a um banco MySQL
- CRUD completo: inserção, consulta, atualização e exclusão
- Justificativa das tabelas utilizadas com base no MER da Fase 2
- Documentação com exemplos e justificativas

### 📘 Endpoints disponíveis:

- `/produtores` - Cadastro de produtores
- `/culturas` - Gestão das culturas agrícolas
- `/sensores` - Cadastro dos sensores físicos
- `/sensores-instalados` - Associação de sensores a culturas
- `/leituras` - Registro das leituras de sensores

### ▶️ Como Executar

```bash
cd api_crud
pip install -r requirements.txt
python app.py
```

### 🔍 Documentação Swagger

Acesse a documentação interativa da API em:

👉 http://{base_url_api}:5000/apidocs

### 📂 Entregáveis:

- `app.py` com a API Flask completa
- `requirements.txt` com dependências
- Swagger UI embutido na aplicação para testes dos endpoints
- Tabelas com dados fictícios para simulação

---

## 🌟 Projeto “Ir Além” – Dashboard Interativo com Streamlit

Como parte das atividades opcionais da disciplina, este projeto também inclui um dashboard interativo que permite visualizar em tempo real os dados coletados pelos sensores instalados em campo.

### 🎯 Objetivo

Transformar dados técnicos em representações visuais fáceis de entender, possibilitando que qualquer usuário — mesmo sem conhecimento técnico — possa acompanhar:

- Umidade do solo
- pH
- Níveis de fósforo e potássio
- Nome dos sensores e seus valores ao longo do tempo

### 🧰 Tecnologias Utilizadas

- **Python**
- **Streamlit** (aplicação web interativa)
- **Pandas** (manipulação de dados)
- **Plotly** (visualização gráfica)
- **Integração com API Flask (Fase 2)**

### 🖥️ Funcionalidades do Painel

- Gráficos por sensor com separação por cor
- Tabela de dados com nomes reais dos sensores
- Atualização em tempo real dos dados com base na API
- Interface simples acessível via navegador

### ▶️ Como Executar

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

Depois disso, acesse o painel em: [http://localhost:8501](http://localhost:8501)

### 📂 Entregáveis

- `dashboard/app.py`: Código completo do painel
- `dashboard/requirements.txt`: Dependências necessárias
- Atualização automática com base na API desenvolvida

---

## ☁️ Projeto “Ir Além 2” – Integração com API Meteorológica (OpenWeather)

Este desafio opcional demonstra a capacidade do sistema de irrigação em tomar decisões mais inteligentes, utilizando dados climáticos reais via API pública.

### 🎯 Objetivo

Consultar a previsão do tempo real (próximas 24h) e decidir, de forma automática, se a irrigação deve ser executada ou suspensa para evitar desperdício de água em caso de chuva.

### 🔗 Integração com OpenWeatherMap

- API utilizada: [OpenWeatherMap - Forecast 5 Days](https://openweathermap.org/forecast5)
- Requisição feita no endpoint: `/data/2.5/forecast`
- Cidade consultada: São Paulo (BR)
- A resposta é processada para identificar campos como `rain.3h` nas próximas 8 faixas de 3h (24h totais)

### 💡 Lógica aplicada

```
Se houver previsão de chuva nas próximas 24h → Não irrigar
Senão → Permitir irrigação conforme sensores
```

### 🔧 Implementação

- Um endpoint adicional foi adicionado à API Flask: `POST /clima/prever-irrigacao`
  - Ele consulta a previsão e grava no banco de dados a decisão (permitir ou não irrigar)
- Outro endpoint `GET /status-irrigacao` é consumido pelo ESP32 no loop principal
  - Se `pode_irrigar = true` → os dados são enviados via POST normalmente
  - Se `pode_irrigar = false` → o envio é bloqueado e a bomba permanece desligada

### 📂 Entregáveis

- Código Flask atualizado com os endpoints `/clima/prever-irrigacao` e `/status-irrigacao`
- Integração no código `.ino` com verificação da decisão antes de enviar a leitura
- Lógica pronta para expansão futura com IA, sensores climáticos ou regras avançadas

## 🗃 Histórico de lançamentos

* 0.2.0 - 18/06/2025 (Repositório Atual)
    * 
* 0.1.0 - 20/05/2025 - (https://github.com/drdosan/construindo_maquina_agricola)
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


