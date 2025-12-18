import streamlit as st
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", page_icon="🌦️", layout="centered")

st.title(" Weather Dashboard")
st.caption("weather data — powered by Open-Meteo API")

city = st.text_input("Enter a city name:", "New York")

if city:
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)

    if location:
        lat, lon = location.latitude, location.longitude
        st.write(f" Location: **{location.address}**")
        st.write(f" Coordinates: {lat:.2f}, {lon:.2f}")

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            weather = data.get("current_weather", {})

            if weather:
                st.subheader(f"Weather at {datetime.now().strftime('%I:%M %p')}")
                st.metric(" Temperature (°C)", f"{weather['temperature']}°C")
                st.metric(" Wind Speed (m/s)", f"{weather['windspeed']}")
                st.metric(" Wind Direction (°)", f"{weather['winddirection']}")
                st.metric(" Time", weather['time'])
            else:
                st.warning("Weather data not available for this location.")
        else:
            st.error("Failed to fetch weather data. Try again later.")
    else:
        st.error("City not found. Please check the name.")
