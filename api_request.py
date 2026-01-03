import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

def get_weather_data():
	# Configurar o cliente da API Open-Meteo com cache e repetição em caso de erro
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Certifique-se de que todas as variaveis meteorologicas necessarias estejam listadas aqui
	# A ordem das varaivies em horarios ou diarios é importante para atribui-las corretamente abaixo
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": -25.183,
		"longitude": -50.9236,
		"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "precipitation_sum"],
		"hourly": ["temperature_2m", "precipitation", "precipitation_probability"],
		"current": ["temperature_2m", "precipitation"],
		"timezone": "auto",
	}
	response = openmeteo.weather_api(url, params=params)[0]

	# Processar dados atuais.
	current = response.Current()
	current_df = {
		"date": [current.Time()],
		"temperature_2m": current.Variables(0).Value(),
		"precipitation": current.Variables(1).Value(),
	}
	current_df = pd.DataFrame(data=current_df)

	# Processar dados horarios.
	hourly = response.Hourly()
	hourly_df = {
		"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		),
		"temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
		"precipitation": hourly.Variables(1).ValuesAsNumpy(),
		"precipitation_probability": hourly.Variables(2).ValuesAsNumpy(),
	}

	hourly_df = pd.DataFrame(data = hourly_df)

	# Processar dados diarios.
	daily = response.Daily()
	daily_df = {
		"date": pd.date_range(
			start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		),
		"temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
		"temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
		"precipitation_probability_max": daily.Variables(2).ValuesAsNumpy(),
		"precipitation_sum": daily.Variables(3).ValuesAsNumpy()
	}
	daily_df = pd.DataFrame(data = daily_df)

	print("Requisicoes concluidas")
	return current_df, hourly_df, daily_df 
