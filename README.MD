# 🌤️ Weather App – Python GUI Project

## 📌 About the Project

The Weather App is a desktop-based application developed using Python and Tkinter. It provides real-time weather information for different cities using the OpenWeatherMap API.

The application also displays a 5-day weather forecast with temperature details and weather conditions.

## ✨ Features

- Search weather by city name.
- Display current temperature.
- Show feels-like temperature.
- Display humidity and wind speed.
- 5-day weather forecast.
- Individual weather forecast cards.
- Dynamic weather icons.
- Celsius (°C) and Fahrenheit (°F) conversion.
- Refresh weather information.
- Clear search results.
- Scrollable forecast section.
- Automatic date and time display.
- Error handling for invalid cities and network issues.

## 🛠️ Technologies Used

- Python
- Tkinter (GUI)
- Requests library
- OpenWeatherMap API

## 📂 Project Structure

```text
Weather_app/
│
├── weather_gui.py
├── weather.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation and Setup

**Step 1: Install Python**

Download Python from https://www.python.org/

**Step 2: Install required library**

Open the terminal and execute:

```bash
pip install -r requirements.txt
```

**Step 3: Get an API Key**

Create an account at https://openweathermap.org/ and generate an API key.

**Step 4: Configure API Key**

Add your API key privately in the application configuration before running the project.

**Step 5: Run the Application**

```bash
python weather_gui.py
```

## 🌡️ Temperature Conversion

The application supports Celsius and Fahrenheit conversion.

Formula:

°F = (°C × 9/5) + 32

## 🌐 API Used

OpenWeatherMap API

Website: https://openweathermap.org/api

The application uses:
- Current Weather API
- 5 Day / 3 Hour Forecast API

## 🚀 Future Improvements

- Weather forecast charts.
- Weather notifications.
- Favourite cities.
- Weather-based background themes.
- Automatic location detection.

## 👩‍💻 Author

Developed as a Python GUI learning project.

## 📄 License

This project is created for educational purposes.