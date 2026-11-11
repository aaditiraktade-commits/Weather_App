
import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

# =====================================
# CONFIGURATION
# =====================================

API_KEY = "7f6d4b456f0d6eeb607a6f832d892a19"

BASE_URL = "https://api.openweathermap.org/data/2.5"

BG = "#102A43"
CARD_BG = "#243F5A"
ACCENT = "#00B4D8"
WHITE = "#FFFFFF"
MUTED = "#BCCCDC"

current_unit = "C"
current_weather_data = None
current_forecast_data = None
last_city = ""


# =====================================
# TEMPERATURE CONVERSION
# =====================================

def convert_temperature(celsius):

    if current_unit == "F":
        return (celsius * 9 / 5) + 32

    return celsius


def format_temperature(celsius):

    return f"{convert_temperature(celsius):.1f} °{current_unit}"


# =====================================
# WEATHER ICONS
# =====================================

def get_weather_icon(condition):

    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Drizzle": "🌦️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️"
    }

    return icons.get(condition, "🌤️")


# =====================================
# UPDATE DATE AND TIME
# =====================================

def update_clock():

    date_label.config(
        text=datetime.now().strftime(
            "%A, %d %B %Y  |  %I:%M:%S %p"
        )
    )

    root.after(1000, update_clock)


# =====================================
# DISPLAY CURRENT WEATHER
# =====================================

def display_current_weather(data):

    city_name = data["name"]

    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]

    weather = data["weather"][0]["description"]
    condition = data["weather"][0]["main"]

    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    icon_label.config(
        text=get_weather_icon(condition)
    )

    result_label.config(
        text=(
            f"{city_name}\n"
            f"{format_temperature(temperature)}\n"
            f"Feels Like: {format_temperature(feels_like)}\n"
            f"{weather.title()}\n\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        ),
        fg=WHITE
    )


# =====================================
# CLEAR FORECAST CARDS
# =====================================

def clear_forecast_cards():

    for widget in forecast_inner_frame.winfo_children():
        widget.destroy()


# =====================================
# DISPLAY FORECAST
# =====================================

def display_forecast(data):

    clear_forecast_cards()

    daily_data = {}

    for item in data["list"]:

        date = item["dt_txt"].split(" ")[0]

        temperature = item["main"]["temp"]
        condition = item["weather"][0]["main"]

        if date not in daily_data:

            daily_data[date] = {
                "temperatures": [],
                "conditions": []
            }

        daily_data[date]["temperatures"].append(
            temperature
        )

        daily_data[date]["conditions"].append(
            condition
        )

    heading = tk.Label(
        forecast_inner_frame,
        text="5-DAY WEATHER FORECAST",
        font=("Arial", 16, "bold"),
        bg=BG,
        fg=WHITE
    )

    heading.pack(pady=12)

    for date, details in list(daily_data.items())[:5]:

        temperatures = details["temperatures"]

        min_temp = min(temperatures)
        max_temp = max(temperatures)

        condition = max(
            set(details["conditions"]),
            key=details["conditions"].count
        )

        icon = get_weather_icon(condition)

        date_object = datetime.strptime(
            date, "%Y-%m-%d"
        )

        day_name = date_object.strftime("%A")

        card = tk.Frame(
            forecast_inner_frame,
            bg=CARD_BG,
            padx=15,
            pady=12,
            highlightbackground="#426581",
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=12,
            pady=7
        )

        tk.Label(
            card,
            text=f"{day_name} | {date}",
            font=("Arial", 12, "bold"),
            bg=CARD_BG,
            fg=WHITE
        ).pack(anchor="w")

        tk.Label(
            card,
            text=icon,
            font=("Arial", 30),
            bg=CARD_BG,
            fg=WHITE
        ).pack(pady=4)

        tk.Label(
            card,
            text=condition,
            font=("Arial", 12),
            bg=CARD_BG,
            fg=MUTED
        ).pack()

        tk.Label(
            card,
            text=(
                f"Min: {format_temperature(min_temp)}"
                f"     Max: {format_temperature(max_temp)}"
            ),
            font=("Arial", 12, "bold"),
            bg=CARD_BG,
            fg=WHITE
        ).pack(pady=7)

    forecast_canvas.configure(
        scrollregion=forecast_canvas.bbox("all")
    )

    forecast_canvas.yview_moveto(0)


# =====================================
# FETCH FORECAST
# =====================================

def get_forecast(city):

    global current_forecast_data

    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
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

            current_forecast_data = data
            display_forecast(data)

        else:

            current_forecast_data = None
            clear_forecast_cards()

            tk.Label(
                forecast_inner_frame,
                text="Forecast unavailable: "
                + data.get("message", "Unknown error"),
                bg=BG,
                fg="yellow"
            ).pack(pady=15)

    except requests.exceptions.RequestException:

        current_forecast_data = None
        clear_forecast_cards()

        tk.Label(
            forecast_inner_frame,
            text="Network error while fetching forecast!",
            bg=BG,
            fg="yellow"
        ).pack(pady=15)


# =====================================
# FETCH CURRENT WEATHER
# =====================================

def get_weather():

    global current_weather_data
    global current_forecast_data
    global last_city

    city = city_entry.get().strip()

    if not city:

        result_label.config(
            text="Please enter a city name!",
            fg="yellow"
        )

        icon_label.config(text="🌤️")
        clear_forecast_cards()
        return

    if API_KEY == "PASTE_YOUR_NEW_API_KEY_HERE":

        result_label.config(
            text="Please add your OpenWeatherMap API key.",
            fg="yellow"
        )

        return

    search_btn.config(
        state="disabled",
        text="Loading..."
    )

    refresh_btn.config(state="disabled")

    result_label.config(
        text="Fetching weather...",
        fg=WHITE
    )

    current_weather_data = None
    current_forecast_data = None

    clear_forecast_cards()

    root.update_idletasks()

    url = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": API_KEY,
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

            current_weather_data = data
            last_city = city

            display_current_weather(data)

            get_forecast(city)

        elif response.status_code == 404:

            result_label.config(
                text="City not found! Try another city.",
                fg="yellow"
            )

            icon_label.config(text="❓")

        elif response.status_code == 401:

            result_label.config(
                text="Invalid API key. Check your API key.",
                fg="yellow"
            )

        else:

            result_label.config(
                text=data.get(
                    "message",
                    "Unable to fetch weather."
                ),
                fg="yellow"
            )

    except requests.exceptions.Timeout:

        result_label.config(
            text="Request timed out! Try again.",
            fg="yellow"
        )

    except requests.exceptions.RequestException:

        result_label.config(
            text="Network error! Check your internet.",
            fg="yellow"
        )

    finally:

        search_btn.config(
            state="normal",
            text="Search Weather"
        )

        refresh_btn.config(state="normal")


# =====================================
# TOGGLE CELSIUS / FAHRENHEIT
# =====================================

def toggle_temperature():

    global current_unit

    if current_unit == "C":

        current_unit = "F"

        unit_btn.config(text="Switch to °C")

    else:

        current_unit = "C"

        unit_btn.config(text="Switch to °F")

    if current_weather_data is not None:

        display_current_weather(current_weather_data)

    if current_forecast_data is not None:

        display_forecast(current_forecast_data)


# =====================================
# REFRESH WEATHER
# =====================================

def refresh_weather():

    if last_city:

        city_entry.delete(0, tk.END)
        city_entry.insert(0, last_city)

        get_weather()


# =====================================
# CLEAR APP
# =====================================

def clear_weather():

    global current_weather_data
    global current_forecast_data
    global last_city

    city_entry.delete(0, tk.END)

    result_label.config(text="")
    icon_label.config(text="🌤️")

    current_weather_data = None
    current_forecast_data = None
    last_city = ""

    clear_forecast_cards()

    forecast_canvas.yview_moveto(0)


# =====================================
# MAIN WINDOW
# =====================================

root = tk.Tk()

root.title("Weather App")
root.geometry("550x850")
root.configure(bg=BG)
root.resizable(False, False)


# =====================================
# DATE AND TIME
# =====================================

date_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
)

date_label.pack(pady=8)

update_clock()


# =====================================
# APP TITLE
# =====================================

title = tk.Label(
    root,
    text="🌤 WEATHER APP",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=WHITE
)

title.pack(pady=10)


# =====================================
# CITY INPUT
# =====================================

city_label = tk.Label(
    root,
    text="Enter City Name",
    font=("Arial", 14),
    bg=BG,
    fg=WHITE
)

city_label.pack(pady=5)


city_entry = tk.Entry(
    root,
    font=("Arial", 16),
    width=22,
    justify="center"
)

city_entry.pack(pady=8)


# =====================================
# BUTTON FRAME
# =====================================

button_frame = tk.Frame(
    root,
    bg=BG
)

button_frame.pack(pady=7)


search_btn = tk.Button(
    button_frame,
    text="Search Weather",
    font=("Arial", 11, "bold"),
    bg=ACCENT,
    fg=WHITE,
    width=16,
    command=get_weather,
    cursor="hand2"
)

search_btn.grid(
    row=0,
    column=0,
    padx=5
)


refresh_btn = tk.Button(
    button_frame,
    text="Refresh",
    font=("Arial", 11, "bold"),
    bg="#2D9CDB",
    fg=WHITE,
    width=10,
    command=refresh_weather,
    cursor="hand2"
)

refresh_btn.grid(
    row=0,
    column=1,
    padx=5
)


unit_btn = tk.Button(
    button_frame,
    text="Switch to °F",
    font=("Arial", 11, "bold"),
    bg="#6C63FF",
    fg=WHITE,
    width=12,
    command=toggle_temperature,
    cursor="hand2"
)

unit_btn.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=7
)


# =====================================
# CURRENT WEATHER ICON
# =====================================

icon_label = tk.Label(
    root,
    text="🌤️",
    font=("Arial", 40),
    bg=BG,
    fg=WHITE
)

icon_label.pack(pady=3)


# =====================================
# WEATHER DETAILS
# =====================================

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    bg=BG,
    fg=WHITE,
    justify="center"
)

result_label.pack(pady=5)


# =====================================
# SCROLLABLE FORECAST
# =====================================

forecast_frame = tk.Frame(
    root,
    bg=BG
)

forecast_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=5
)

forecast_canvas = tk.Canvas(
    forecast_frame,
    bg=BG,
    highlightthickness=0
)

forecast_scrollbar = ttk.Scrollbar(
    forecast_frame,
    orient="vertical",
    command=forecast_canvas.yview
)

forecast_inner_frame = tk.Frame(
    forecast_canvas,
    bg=BG
)

forecast_window = forecast_canvas.create_window(
    (0, 0),
    window=forecast_inner_frame,
    anchor="nw"
)


def update_scroll_region(event=None):

    forecast_canvas.configure(
        scrollregion=forecast_canvas.bbox("all")
    )


def update_forecast_width(event):

    forecast_canvas.itemconfigure(
        forecast_window,
        width=event.width
    )


forecast_inner_frame.bind(
    "<Configure>",
    update_scroll_region
)

forecast_canvas.bind(
    "<Configure>",
    update_forecast_width
)

forecast_canvas.configure(
    yscrollcommand=forecast_scrollbar.set
)

forecast_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

forecast_scrollbar.pack(
    side="right",
    fill="y"
)


# =====================================
# MOUSE WHEEL SCROLLING
# =====================================

def mouse_scroll(event):

    forecast_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


forecast_canvas.bind(
    "<MouseWheel>",
    mouse_scroll
)

forecast_inner_frame.bind(
    "<MouseWheel>",
    mouse_scroll
)


# =====================================
# ENTER KEY SUPPORT
# =====================================

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


# =====================================
# CLEAR BUTTON
# =====================================

clear_btn = tk.Button(
    root,
    text="Clear",
    font=("Arial", 12, "bold"),
    bg="#EF5350",
    fg=WHITE,
    width=12,
    command=clear_weather,
    cursor="hand2"
)

clear_btn.pack(pady=8)


# =====================================
# RUN APPLICATION
# =====================================

root.mainloop()
