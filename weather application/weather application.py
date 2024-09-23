import datetime as dt
import requests
import tkinter as tk
from PIL import Image, ImageTk
import creds 

BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather?"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast?"

# Converts temperature from Kelvin to Celsius and Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    celsius = round(celsius, 2)
    fahrenheit = celsius * (9 / 5) + 32
    fahrenheit = round(fahrenheit, 2)
    return celsius, fahrenheit

# Function to fetch and display weather on the second page
def SecondPage():
    global photo

    # Get the city from the entry widget
    CITY = entry.get()

    # Construct the API URLs with the entered city for both current and forecast data
    url_current = BASE_URL_CURRENT + "appid=" + (creds.API_KEY) + "&q=" + CITY
    url_forecast = BASE_URL_FORECAST + "appid=" + (creds.API_KEY) + "&q=" + CITY

    # Send the HTTP request and store the response in JSON format
    response_current = requests.get(url_current).json()
    response_forecast = requests.get(url_forecast).json()

    # If the city is found in the API
    if response_current["cod"] == 200:
        # Convert temperatures for current weather
        temp_kelvin = response_current["main"]["temp"]
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

        feels_like_kelvin = response_current["main"]["feels_like"]
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

        wind_speed = response_current["wind"]["speed"]
        humidity = response_current["main"]["humidity"]
        description = response_current["weather"][0]["description"]

        sunrise_time = dt.datetime.utcfromtimestamp(response_current["sys"]["sunrise"] + response_current["timezone"])
        sunset_time = dt.datetime.utcfromtimestamp(response_current["sys"]["sunset"] + response_current["timezone"])

        # Display the second page
        colorbg.forget()  # Remove the first page
        colorbg2 = tk.Frame(root, bg="dodgerblue", height=600, width=350)
        colorbg2.pack()

        frame1 = tk.Frame(colorbg2, bg="white", height=300, width=250)
        frame1.place(x=175, y=150, anchor="center")

        # Display city name
        citylabel = tk.Label(colorbg2, text=CITY, font="Georgia", bg="dodgerblue", fg="white")
        citylabel.place(x=175, y=25, anchor="center")

        # Display temperature info
        tempcity = tk.Label(frame1, bg="white", text=f"Temperature: {temp_celsius}°C / {temp_fahrenheit}°F", wraplength=250)
        tempcity.place(x=125, y=60, anchor="center")

        # Display feels-like temperature
        feelcity = tk.Label(frame1, bg="white", text=f"Feels like: {feels_like_celsius}°C / {feels_like_fahrenheit}°F", wraplength=250)
        feelcity.place(x=125, y=90, anchor="center")

        # Display humidity info
        humiditylabel = tk.Label(frame1, bg="white", text=f"Humidity: {humidity}%", wraplength=250)
        humiditylabel.place(x=125, y=120, anchor="center")

        # Display wind speed
        windlabel = tk.Label(frame1, bg="white", text=f"Wind Speed: {wind_speed} m/s", wraplength=250)
        windlabel.place(x=125, y=150, anchor="center")

        # Display general weather description
        weatherlabel = tk.Label(frame1, bg="white", text=f"Weather: {description.capitalize()}", wraplength=250)
        weatherlabel.place(x=125, y=180, anchor="center")

        # Display sunrise and sunset times
        sunriselabel = tk.Label(frame1, bg="white", text=f"Sunrise: {sunrise_time}", wraplength=250)
        sunriselabel.place(x=125, y=210, anchor="center")

        sunsetlabel = tk.Label(frame1, bg="white", text=f"Sunset: {sunset_time}", wraplength=250)
        sunsetlabel.place(x=125, y=240, anchor="center")

        # Display future forecast (temperatures for the next 5 days)
        forecast_label = tk.Label(colorbg2, text="5-Day Forecast:", font=("Georgia", 12), bg="dodgerblue", fg="white")
        forecast_label.place(x=175, y=330, anchor="center")

        # Extract forecast temperatures (5 data points, 3-hour intervals)
        for i in range(0, 40, 8):  # Every 8th entry is approximately 1 day later (24 hours / 3-hour intervals)
            forecast_data = response_forecast["list"][i]
            date_time = dt.datetime.utcfromtimestamp(forecast_data["dt"])
            temp_kelvin_forecast = forecast_data["main"]["temp"]
            temp_celsius_forecast, temp_fahrenheit_forecast = kelvin_to_celsius_fahrenheit(temp_kelvin_forecast)

            # Display the forecast day and temperature
            day_label = tk.Label(colorbg2, text=f"{date_time.strftime('%Y-%m-%d %H:%M')}: {temp_celsius_forecast}°C / {temp_fahrenheit_forecast}°F", font="Georgia", bg="dodgerblue", fg="white", wraplength=350)
            day_label.place(x=175, y=360 + (i // 8) * 30, anchor="center")

    else:
        # If city is not found
        error_label = tk.Label(root, text="City not found. Please enter a valid city.", font="Georgia", bg="red", fg="white", wraplength=300)
        error_label.place(x=175, y=450, anchor="center")

# ---- GUI Portion ----

root = tk.Tk()
root.title("Weather Application")
root.geometry("350x600")  # Increased height to fit forecast

# First page frame
colorbg = tk.Frame(root, bg="dodgerblue", height=600, width=350)
colorbg.pack()

# Opens the image with Pillow, resize it, and then convert it to PhotoImage
image = Image.open("Images/weather.png")
resized_image = image.resize((70, 70), Image.LANCZOS)  # Resize the image
photo = ImageTk.PhotoImage(resized_image)  # Convert to PhotoImage

photolabel = tk.Label(colorbg, image=photo, bg="dodgerblue")
photolabel.place(x=175, y=160, anchor="center")

label2 = tk.Label(colorbg, text="Please enter a city", font="Georgia", bg="dodgerblue", fg="white")
label2.place(x=175, y=215, anchor="center")

# Entry widget to input city
entry = tk.Entry(colorbg, font="Georgia")
entry.place(x=175, y=250, anchor="center")

# Button to view weather, triggers SecondPage function
button = tk.Button(colorbg, text="View Weather", font="Georgia", command=SecondPage)
button.place(x=175, y=295, anchor="center")

root.mainloop()
