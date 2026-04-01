import json
import requests
import pandas as pd
import numpy as np
import psycopg2


def fetch_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()
    return data


result = fetch_weather("Amsterdam")


def parse_weather(data):
    current = data["current_condition"][0]
    return {
        "temperature_c": current["temp_C"],
        "feels_like_c": current["FeelsLikeC"],
        "humidity": current["humidity"],
        "description": current["weatherDesc"][0]["value"],
        "wind_kmph": current["windspeedKmph"]
    }


def save_to_db(weather, city):
    conn = psycopg2.connect(
        dbname="weather_db",
        user="victorrotaras",
        host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather_readings 
        (city, temperature_c, feels_like_c, humidity, description, wind_kmph)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        city,
        int(weather["temperature_c"]),
        int(weather["feels_like_c"]),
        int(weather["humidity"]),
        weather["description"],
        int(weather["wind_kmph"])
    ))
    conn.commit()
    cursor.close()
    conn.close()


def export_report(df):
    df.to_csv("weather_report.csv", index=False)
    print("Report saved to weather_report.csv")


cities = ["Amsterdam", "London", "Berlin", "Barcelona"]

rows = []
for city in cities:
    raw = fetch_weather(city)
    weather = parse_weather(raw)
    weather["city"] = city
    rows.append(weather)
    save_to_db(weather, city)
    print(f"Saved {city} to database")

df = pd.DataFrame(rows)
df["temperature_c"] = pd.to_numeric(df["temperature_c"])
df["humidity"] = pd.to_numeric(df["humidity"])

print(df)
print(f"\nWarmest city: {df.loc[df['temperature_c'].idxmax(), 'city']}")
print(f"Average humidity: {df['humidity'].mean():.1f}%")

temps = df["temperature_c"].values
print(f"\nTemperature analysis:")
print(f"  Min: {np.min(temps)}°C")
print(f"  Max: {np.max(temps)}°C")
print(f"  Mean: {np.mean(temps):.1f}°C")
print(f"  Std deviation: {np.std(temps):.1f}°C")

export_report(df)
