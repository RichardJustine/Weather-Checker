# import discord
import requests, os
from datetime import datetime
from city import City
from weather import Weather
from constants import Constants
from wind import Wind
# from keep_alive import keep_alive

# intent = discord.Intents.default()
# intent.members = True
# intent.message_content = True

# client = discord.Client(intents=intent)
# TOKEN = os.environ["TOKEN"]

# @client.event
# async def on_ready():
#   print("We have logged in as {0.user}".format(client))

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return

#   msg = message.content

#   if msg.startswith("$weather"):
#     city = msg.lower().split("$weather ", 1)[1]

#     app = WeatherApp(city, message)
#     await app.start()


class WeatherApp:

  # def __init__(self, city, message):
  def __init__(self):
    self.constants = Constants()
    # self.city_input = city
    # self.message = message
    self.city_input = ""
    self.message = ""
    self.base_url = ""
    self.current_day_query = ""
    self.hourly_forecast_query = ""
    self.current_weather_data = ""
    self.hourly_forecast_data = ""
    self.city = ""
    self.weather = ""
    self.wind = ""

  # async def start(self):
  def start(self):
    self.input_city()
    # await self.message.channel.send(
    #   "=====================================================================")
    # await self.message.channel.send("Let's check the Weather")
    # await self.message.channel.send(
    #   "=====================================================================")

    try:
      self.base_url = "http://api.openweathermap.org/data/2.5/"
      # get current weather data by city
      self.current_day_query = self.base_url + "weather?appid=" + self.constants.API_KEY + "&q=" + self.city_input
      self.current_weather_data = requests.get(self.current_day_query).json()

      # weather class initialization
      self.weather = Weather(
        self.current_weather_data["main"]["temp"],  # temperature
        self.current_weather_data["main"]["feels_like"],  # feels_like
        self.current_weather_data["weather"][0]["main"],  # name
        self.current_weather_data["weather"][0]["description"],  # description
        self.current_weather_data["weather"][0]["icon"],  # icon
        self.current_weather_data["main"]["pressure"],  # pressure
        self.current_weather_data["main"]["humidity"],  # humidity
        self.current_weather_data["visibility"]  # visibility
      )

      # wind class initialization
      self.wind = Wind(
        self.current_weather_data["wind"]["deg"],  # direction
        self.current_weather_data["wind"]["speed"],  # speed
        self.current_weather_data["wind"]["gust"])  # gust

      # city class initialization
      self.city = City(
        self.current_weather_data["dt"],  # unix
        self.current_weather_data["timezone"],  # timezone
        self.current_weather_data["name"],  # name
        self.current_weather_data["sys"]["country"],  # country
        self.weather,  # weather
        self.wind)  # wind

      # get 5 day / 3 hour weather forecast data by city
      self.hourly_forecast_query = self.base_url + "forecast?appid=" + self.constants.API_KEY + "&q=" + self.city_input
      self.hourly_forecast_data = requests.get(
        self.hourly_forecast_query).json()

      # await self.get_weather_data()
      self.get_weather_data()
    except:
      print("City not found...")
      self.ask_user()

  def input_city(self):
    print("*" * 30)
    print("Let's check the Weather")
    print("*" * 30)

    # ask user for city input
    self.city_input = input("\nEnter a city: ")
    while not self.city_input.isalpha() and not self.city_input.find(",") >= 0:
      self.city_input = input("Invalid city. Enter a different one: ")

  def get_datetime_from_unix(self, unix):
    timestamp = int(unix)
    return datetime.utcfromtimestamp(timestamp).strftime("%d %B %Y_%H:%M")

  def get_spacing_by_str_len(self, str_len, max_str_len):
    space_count = max_str_len - str_len
    if str_len > 0:
      return " " * space_count

  def ask_user(self):
    print()
    print("*" * 30)
    print("Do you want to check the Weather again? ")
    print("[1] Yes")
    print("[2] No")
    user_choice = input("Which one? ")
    print("*" * 30)
    while not user_choice.isdigit() or int(user_choice) > 2 or int(
        user_choice) < 1:
      user_choice = input("\nNo option selected. Choose again: ")
    user_choice = int(user_choice)
    if user_choice == 1:
      clear = lambda: os.system("clear")
      clear()
      new_app = WeatherApp()
      new_app.start()
    else:
      print("Goodbye! Thanks for checking the Weather.")

  # async def get_current_weather_data(self):
  def get_current_weather_data(self):
    # city
    self.city.get_date_time()
    self.city.get_name()
    self.city.get_country()

    # weather
    self.city.weather.get_temperature()
    self.city.weather.get_feels_like()
    self.city.weather.get_name()
    self.city.weather.get_description()
    self.city.weather.get_icon()
    self.city.weather.get_pressure()
    self.city.weather.get_humidity()
    self.city.weather.get_dew_point()
    self.city.weather.get_visibility()

    # wind
    self.city.wind.get_speed()
    self.city.wind.get_direction()
    self.city.wind.get_gust()

    # await self.display_current_weather_data()
    self.display_current_weather_data()

  # async def display_current_weather_data(self):
  def display_current_weather_data(self):
    print()
    print(
      self.city.date_time.split("_")[0] + " " +
      self.city.date_time.split("_")[1].lower())
    print(f"{self.city.name}, {self.city.country}")
    print(f"{self.city.weather.icon} {self.city.weather.temperature}°C")
    print(
      f"Feels like {self.city.weather.feels_like}°C. {self.city.weather.name}. {self.city.weather.description}."
    )
    print("=" * 69)
    print(
      f"|\t🍃 {self.city.wind.speed}m/s {self.city.wind.direction}\t🧭 {self.city.weather.pressure}hPa"
    )
    print(
      f"|\tHumidity: {self.city.weather.humidity}%\tDew point: {self.city.weather.dew_point}°C"
    )
    print(
      f"|\tVisibility: {self.city.weather.visibility}km\tGust: {self.city.wind.gust}mph"
    )
    print("=" * 69)

    # await self.send_current_weather_data()

  # async def send_current_weather_data(self):
  #   await self.message.channel.send(
  #     self.city.date_time.split("_")[0] + " " +
  #     self.city.date_time.split("_")[1].lower())
  #   await self.message.channel.send(self.city.name + ", " + self.city.country)
  #   await self.message.channel.send(
  #     str(self.city.weather.icon) + " " + str(self.city.weather.temperature) +
  #     "°C")
  #   await self.message.channel.send("Feels like " +
  #                                   str(self.city.weather.feels_like) +
  #                                   "°C. " + self.city.weather.name + ". " +
  #                                   self.city.weather.description.title() +
  #                                   ".")
  #   await self.message.channel.send(
  #     "=====================================================================")
  #   await self.message.channel.send("|\t🍃 " + str(self.city.wind.speed) +
  #                                   "m/s " + str(self.city.wind.direction) +
  #                                   "\t🧭 " + str(self.city.weather.pressure) +
  #                                   "hPa")
  #   await self.message.channel.send("|\tHumidity: " +
  #                                   str(self.city.weather.humidity) +
  #                                   "%\tDew point: " +
  #                                   str(self.city.weather.dew_point) + "°C")
  #   await self.message.channel.send("|\tVisibility: " +
  #                                   str(self.city.weather.visibility) +
  #                                   "km\tGust: " + str(self.city.wind.gust) +
  #                                   "mph")
  #   await self.message.channel.send(
  #     "=====================================================================")

  # async def get_hourly_forecast_data(self):
  def get_hourly_forecast_data(self):
    # await self.format_table()
    # await self.display_hourly_forecast_data()
    self.format_table()
    self.display_hourly_forecast_data()

  # async def format_table(self):
  def format_table(self):
    print()
    print("3-hour Forecast 5 days")
    print("-" * 69)
    print(
      f"| Date/Time (PST) |{' ' * 2}Temp. (°C){' ' * 2}|{' ' * 8}Weather Conditions{' ' * 8}|"
    )

    # await self.message.channel.send("3-hour Forecast 5 days")
    # await self.message.channel.send(
    #   "-----------------------------------------------------------------------------------"
    # )
    # await self.message.channel.send(
    #   "| Date/Time (PST) |  Temp. (°C)  |            Weather Conditions")

  # async def display_hourly_forecast_data(self):
  def display_hourly_forecast_data(self):
    date = ""
    for hfd_index, hfd_item in enumerate(self.hourly_forecast_data["list"]):
      if date == self.get_datetime_from_unix(hfd_item['dt']).split("_")[0]:
        t_str_for_spacing = str(round(hfd_item['main']['temp'] - 273.15))
        wc_str_for_spacing = hfd_item['weather'][0]['main'] + ". " + hfd_item[
          'weather'][0]['description']
        t_spacing = self.get_spacing_by_str_len(len(t_str_for_spacing), 7)
        wc_spacing = self.get_spacing_by_str_len(len(wc_str_for_spacing), 28)
        print(
          f"|{' ' * 6}{self.get_datetime_from_unix(hfd_item['dt']).split('_')[1]}{' ' * 6}|{' ' * 5}{round(hfd_item['main']['temp'] - 273.15)}°C{t_spacing}|{' ' * 6}{hfd_item['weather'][0]['main']}. {hfd_item['weather'][0]['description'].title()}{wc_spacing}|"
        )
      else:
        print("-" * 69)
        date = self.get_datetime_from_unix(hfd_item['dt']).split("_")[0]
        spacing = self.get_spacing_by_str_len(len(date.split(" ")[1]), 9)
        print("| " + date + spacing + ("\t" * 12) + (' ' * 4) + "|")
        print("-" * 69)
    print("-" * 69)
    print()
    print("=" * 69)

    # await self.send_hourly_forecast_data()

  async def send_hourly_forecast_data(self):
    date = ""
    for hfd_index, hfd_item in enumerate(self.hourly_forecast_data["list"]):
      if date == self.get_datetime_from_unix(hfd_item['dt']).split("_")[0]:
        t_str_for_spacing = str(round(hfd_item['main']['temp'] - 273.15))
        wc_str_for_spacing = hfd_item['weather'][0]['main'] + ". " + hfd_item[
          'weather'][0]['description']
        t_spacing = self.get_spacing_by_str_len(len(t_str_for_spacing), 7)
        wc_spacing = self.get_spacing_by_str_len(len(wc_str_for_spacing), 28)
        await self.message.channel.send(
          "|      " +
          str(self.get_datetime_from_unix(hfd_item['dt'])).split('_')[1] +
          "      |      " + str(round(hfd_item['main']['temp'] - 273.15)) +
          "°C" + t_spacing + "|      " + str(hfd_item['weather'][0]['main']) +
          ". " + hfd_item['weather'][0]['description'].title())
      else:
        await self.message.channel.send(
          "-----------------------------------------------------------------------------------"
        )
        date = self.get_datetime_from_unix(hfd_item['dt']).split("_")[0]
        spacing = self.get_spacing_by_str_len(len(date.split(" ")[1]), 9)
        await self.message.channel.send("| " + date + spacing)
        await self.message.channel.send(
          "-----------------------------------------------------------------------------------"
        )
    await self.message.channel.send(
      "-----------------------------------------------------------------------------------"
    )
    await self.message.channel.send(
      "=====================================================================")

  # async def get_weather_data(self):
  def get_weather_data(self):
    # await self.get_current_weather_data()
    # await self.get_hourly_forecast_data()
    self.get_current_weather_data()
    self.get_hourly_forecast_data()
    self.ask_user()


app = WeatherApp()
app.start()

# keep_alive()
# client.run(TOKEN)
