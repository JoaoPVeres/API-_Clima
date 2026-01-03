from api_request import get_weather_data
from dashboard import dashboard
from tratament import process_weather_data

def main():
    current_df, hourly_df, daily_df = get_weather_data()
    current_df, hourly_df, daily_df = process_weather_data(current_df, hourly_df, daily_df)
    dashboard(current_df, hourly_df, daily_df)

if __name__ == "__main__":
    main()