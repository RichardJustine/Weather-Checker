from datetime import datetime


class City:

  def __init__(self, unix, timezone, name, country, weather, wind):
    self.unix = unix
    self.timezone = timezone
    self.date_time = datetime.utcfromtimestamp(
      self.unix + self.timezone).strftime("%h %d,_%I:%M%p")
    self.name = name
    self.country = country
    self.weather = weather
    self.wind = wind

  def get_date_time(self):
    return self.date_time

  def get_name(self):
    return self.name

  def get_country(self):
    return self.country
