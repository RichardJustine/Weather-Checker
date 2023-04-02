import numpy as np
from constants import Constants


class Weather:

  def __init__(self, temperature, feels_like, name, description, icon,
               pressure, humidity, visibility):
    self.constants = Constants()
    self.temperature = round(temperature - self.constants.TEMP_SUB)
    self.feels_like = round(feels_like - self.constants.TEMP_SUB)
    self.name = name
    self.description = description
    self.icon = self.set_icon(icon)
    self.pressure = pressure
    self.humidity = humidity
    self.dew_point = self.set_dew_point(temperature, humidity)
    self.visibility = round(visibility / 1000, 1)

  def get_temperature(self):
    return self.temperature

  def get_feels_like(self):
    return self.feels_like

  def get_name(self):
    return self.name

  def get_description(self):
    return self.description

  def set_icon(self, icon):
    if icon == "01d":
      return "☀"
    elif icon == "01n":
      return "🌑"
    elif icon == "02d" or icon == "02n":
      return "⛅"
    elif icon == "03d" or icon == "04d" or icon == "03n" or icon == "04n":
      return "☁"
    elif icon == "09d" or icon == "09n":
      return "🌧"
    elif icon == "10d" or icon == "10n":
      return "🌦"
    elif icon == "11d" or icon == "11n":
      return "🌩"
    elif icon == "13d" or icon == "13n":
      return "❄"
    elif icon == "50d" or icon == "50n":
      return "💦"

  def get_icon(self):
    return self.icon

  def get_pressure(self):
    return self.pressure

  def get_humidity(self):
    return self.humidity

  def set_dew_point(self, temperature, humidity):
    primary_value = (self.constants.DEW_POINT_PRI * temperature) / (
      temperature + self.constants.DEW_POINT_SEC)
    secondary_value = (np.log(humidity) / 100) + primary_value
    return round(((secondary_value * self.constants.DEW_POINT_SEC) /
                  self.constants.DEW_POINT_PRI) - secondary_value)

  def get_dew_point(self):
    return self.dew_point

  def get_visibility(self):
    return self.visibility
