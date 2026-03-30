# a dictionary is a collection of key:value pairs
stock = {
    "ticker": "AAPL",
    "price": 182.50,
    "sector": "tech",
    "in_watchlist": True
}

# access values by key
print(stock["ticker"])
print(stock["price"])

# add a new key
stock["iv rank"] = 45

# loop through key/value pairs
for key, value in stock.items():
    print(f"{key}: {value}")

import requests

response = requests.get("https://wttr.in/San+Diego?format=j1")
data = response.json()

temp = data["current_condition"][0]["temp_F"]
feels_like = data["current_condition"][0]["FeelsLikeF"]
description = data["current_condition"][0]["weatherDesc"][0]["value"]
latitude = data["nearest_area"][0]["latitude"]
longitude = data["nearest_area"][0]["longitude"]
city = data["nearest_area"][0]["areaName"][0]["value"]
country = data["nearest_area"][0]["country"][0]["value"]
moon_illumination = data["weather"][0]["astronomy"][0]["moon_illumination"]
moon_phase = data["weather"][0]["astronomy"][0]["moon_phase"]

print(f"\nSan Diego right now:")
print(f"    Temp: {temp} F")
print(f"    Feels like: {feels_like} F")
print(f"    Conditions: {description}")
print(f"    Latitude: {latitude}")
print(f"    Longitude: {longitude}")
print(f"    City: {city}")
print(f"    Country: {country}")
print(f"    Moon Illumination: {moon_illumination}")
print(f"    Moon Phase: {moon_phase}")
