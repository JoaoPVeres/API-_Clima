# 🌦️ API_Clima

Um projeto em **Python + Streamlit + Plotly** para consultar dados meteorológicos da **API Open-Meteo**, processar e visualizar em um **dashboard interativo**.

## 📌 Estrutura do Projeto

API_CLIMA/
│
├── api_request.py        # Faz requisição à API Open-Meteo e retorna DataFrames
├── tratament.py           # Processa e salva os dados (tratamento de datas e arredondamento)
├── dashboard.py           # Cria o dashboard interativo com Streamlit e Plotly
├── main.py                # Ponto de entrada do projeto
├── requirements.txt       # Dependências do projeto
├── raw/                  # Pasta para imagens e CSVs gerados
│   ├── background.jpg
│   ├── clima.png
│   ├── current_df.csv
│   ├── hourly_df.csv
│   └── daily_df.csv
└── venv/                 # Ambiente virtual (ignorado pelo git)

📊 Funcionalidades
- Consulta dados atuais, horários e diários da API Open-Meteo
- Processamento e arredondamento dos valores de temperatura e precipitação
- Dashboard interativo com:
- Data atual
- Temperatura atual
- Temperatura máxima/mínima
- Ícone ilustrativo de clima
- Gráfico de temperatura nas próximas 24h
- Gráfico de probabilidade de chuva nas próximas 24h
- Tabela com previsão dos próximos 7 dias

🛠️ Tecnologias utilizadas
- Python
- Streamlit
- Plotly
- Pandas
- Open-Meteo API

✨ Autor
- Projeto desenvolvido por João 🚀