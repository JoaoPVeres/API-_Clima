import os
import pandas as pd

def process_weather_data(current_df, hourly_df, daily_df, replace=True):

    array_dfs = [current_df, hourly_df, daily_df]

    current_df['date'] = pd.to_datetime(current_df['date'], unit='s')
    
    for df in array_dfs:
        if 'temperature_2m' in df.columns:
            df['temperature_2m'] = df['temperature_2m'].round(0)
        if 'temperature_2m_max' in df.columns:
            df['temperature_2m_max'] = df['temperature_2m_max'].round(0)
        if 'temperature_2m_min' in df.columns:
            df['temperature_2m_min'] = df['temperature_2m_min'].round(0)
    
    print('Tratamento realizado!')

    base_path = os.path.dirname(os.path.abspath(__file__)) 
    raw_path = os.path.join(base_path, "raw")
    os.makedirs(raw_path, exist_ok=True)

    if replace:
        current_df.to_csv(os.path.join(raw_path, "current_df.csv"), index=False, encoding="utf-8")
        hourly_df.to_csv(os.path.join(raw_path, "hourly_df.csv"), index=False, encoding="utf-8")
        daily_df.to_csv(os.path.join(raw_path, "daily_df.csv"), index=False, encoding="utf-8")
	
    print('Tabelas salvas!')    

    return current_df, hourly_df, daily_df
