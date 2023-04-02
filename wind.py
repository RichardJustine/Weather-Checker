class Wind:

  def __init__(self, degree_direction, speed, gust):
    self.degree_direction = degree_direction
    self.direction = 0
    self.compass_sectors = [
      "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW",
      "WSW", "W", "WNW", "NW", "NWN", "N"
    ]
    self.speed = round(speed, 1)
    self.gust = round(self.get_mile_per_hour(gust))

  def get_direction(self):
    modulus = self.degree_direction % 360
    sectors = 360 / (len(self.compass_sectors) - 1)
    index = int(round(modulus / sectors, 0))
    self.direction = self.compass_sectors[index]
    return self.direction

  def get_speed(self):
    return self.speed

  def get_gust(self):
    return self.gust

  def get_mile_per_hour(self, meter_per_second):
    meter_per_hour = meter_per_second * 3600
    mile_per_hour = meter_per_hour / 1609.3
    return mile_per_hour