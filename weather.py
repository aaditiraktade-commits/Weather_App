import requests
import json
city = input("Enter city name: ").strip()

if city == "":
    print("Please enter a city name.")

api_key="7f6d4b456f0d6eeb607a6f832d892a19" 

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}   
try:
    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    if response.status_code == 200:
        print("\n----- WEATHER REPORT -----")
        print("City:", data["name"])
        print("Temperature:", data["main"]["temp"], "°C")
        print("Feels Like:", data["main"]["feels_like"], "°C")
        print("Weather:", data["weather"][0]["description"])
        print("Humidity:", data["main"]["humidity"], "%")
        print("Wind Speed:", data["wind"]["speed"], "m/s")

    else:
        print("Error:", data.get("message", "Something went wrong"))

except requests.exceptions.RequestException as e:
    print("Error:", e)