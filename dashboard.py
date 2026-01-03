import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def dashboard(current_df, hourly_df, daily_df):

    # Configuração de página 
    st.set_page_config(layout='wide')

    st.markdown("<h1 style='text-align: center; font-size: 60px; '>Dashboard Clima</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,2])
    with col2:
        st.metric('Data', f'{current_df['date'].iloc[0].strftime('%d/%m/%Y')}')
        st.metric('Temperatura Atual', f'{round(current_df['temperature_2m'].iloc[0])} °')
        st.metric('Temperatura Max\Min', f'{round(daily_df['temperature_2m_max'].iloc[0])} ° / {round(daily_df['temperature_2m_min'].iloc[0])} °')
    with col3:
        st.image("raw/clima.png", width=200)

    # Filtrar próximas 24h
    start_time = hourly_df['date'].iloc[0]
    end_time = start_time + pd.Timedelta(hours=24)
    df_24h = hourly_df[(hourly_df['date'] >= start_time) & (hourly_df['date'] < end_time)]

    st.markdown("<h2 style='text-align: center;'>Previsão para as próximas 24h</h2>", unsafe_allow_html=True)

    # Criar gráfico
    fig_temperature = go.Figure()

    # Linha da temperatura
    fig_temperature.add_trace(go.Scatter(
        x=df_24h['date'],
        y=df_24h['temperature_2m'],
        mode='lines+markers+text', 
        line=dict(color='red'),
        text=[f'{t:.0f}°' for t in df_24h['temperature_2m']],
        textposition='top center'
    ))

    # Layout
    fig_temperature.update_layout(
        title='Temperatura (°C)',
        legend=dict(orientation='h', y=-0.2)
    )

    fig_precipitation = go.Figure()
    # Linha da probabilidade de precipitação
    fig_precipitation.add_trace(go.Scatter(
        x=df_24h['date'],
        y=df_24h['precipitation_probability'],
        mode='lines+markers+text',
        line=dict(color='blue', dash='dot'),
        text=[f'{p:.0f}%' for p in df_24h['precipitation_probability']],
        textposition='bottom center'
    ))

        # Layout
    fig_precipitation.update_layout(
        title='Probabilidade de chuva (%)',
        legend=dict(orientation='h', y=-0.2)
    )

    # Mostrar no Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_temperature, use_container_width=True)
    with col2:
        st.plotly_chart(fig_precipitation, use_container_width=True)
    
    # Tabela temperaturas max/min e probabilidade precipitacao:
    tabela = daily_df[['date', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_probability_max']]

    tabela['date'] = pd.to_datetime(tabela['date']).dt.strftime('%d/%m/%Y')
    
    tabela['temperature_2m_max'] = tabela['temperature_2m_max'].round(0).astype(int).astype(str) + '°' 
    tabela['temperature_2m_min'] = tabela['temperature_2m_min'].round(0).astype(int).astype(str) + '°' 
    tabela['precipitation_probability_max'] = tabela['precipitation_probability_max'].round(0).astype(int).astype(str) + '%'
    
    tabela = tabela.rename(columns={
        'date': 'Data', 
        'temperature_2m_max': 'Temp. Máxima',
        'temperature_2m_min': 'Temp. Mínima',
        'precipitation_probability_max': 'Prob. Chuva' })

    # Estilizar a tabela 
    html_table = tabela.to_html(index=False, justify='center')

    html_table = f'''
    <div style='display: flex; justify-content: center;'>
        <style>
            table {{
                text-align: center;
                font-size: 14px;
            }}
            th, td {{
                text-align: center;
                padding: 6px;
            }}
        </style> 
        {html_table} 
    </div> 
    '''

    st.markdown("<h2 style='text-align: center;'>Previsão dos próximos 7 dias</h2>", unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
