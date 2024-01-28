#!/usr/bin/env python3

import python_weather
import argparse
import json
import asyncio
from datetime import datetime
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--location")

    args = parser.parse_args()

    if not args.location:
        exit()

    asyncio.run(getweather(args.location))

async def getweather(location):
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client() as client:
        # fetch a weather forecast from a city
        weather = await client.get(location)
        
        # Get the current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.strftime("%H:%M")

        # Filter forecasts based on the specified date
        target_daily_forecasts = [daily for daily in weather.forecasts if daily.date == current_date]

        # Print the forecast for the specified time within the date
        daily_forecast = target_daily_forecasts[0]

        # Find the closest available hourly forecast to the specified time
        closest_hourly_forecast = min(daily_forecast.hourly, key=lambda h: abs((current_datetime.replace(hour=h.time.hour, minute=h.time.minute) - current_datetime).total_seconds()))

        print(json.dumps({'text': f"{daily_forecast.astronomy.moon_phase.emoji} | {closest_hourly_forecast.kind.emoji} | {closest_hourly_forecast.temperature}°C", "tooltip": f"{str(daily_forecast.astronomy.moon_phase)} | {str(closest_hourly_forecast.description)} | {closest_hourly_forecast.temperature}°C" }))

if __name__ == "__main__":
    main()
