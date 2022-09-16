import pycountry
import requests
import json
from bs4 import BeautifulSoup


class WeatherAPI:

    @staticmethod
    def getWeather(country, province, city):
        soup = WeatherAPI.getSoup(country, province, city)
        code = WeatherAPI.getCode(soup)
        return WeatherAPI.getData(code)

    @staticmethod
    def getSoup(country, province, city):
        url = WeatherAPI.getUrl(country, province, city)
        return BeautifulSoup(requests.get(url).text, "lxml")

    @staticmethod
    def getUrl(country, province, city):
        base_url = "https://www.theweathernetwork.com/"
        alpha_2 = pycountry.countries.get(name=country).alpha_2
        url = f"{base_url}{alpha_2}/weather/{province}/{city}"
        return url

    @staticmethod
    def getCode(soup):
        data = soup.find("body", {"class": "no-default-background"}).find("script").text
        index = data.find("7Days: ")
        return data[index + 7:-2].strip()

    @staticmethod
    def getData(code):
        url = f"https://weatherapi.pelmorex.com/api/v1/observation/placecode/{code}"
        received_data = json.loads(requests.get(url).text)

        data = dict()
        units = received_data["display"]["unit"]
        observation = received_data["observation"]
        data["temperature"] = f"{observation['temperature']} °{units['temperature']}"
        data["feelsLike"] = f"{observation['feelsLike']} °{units['temperature']}"
        data["visibility"] = f"{observation['visibility']} {units['visibility']}"
        data["wind"] = f"{observation['wind']['speed']} {observation['wind']['direction']} {units['wind']}"
        data["humidity"] = f"{observation['relativeHumidity']}{units['relativeHumidity']}"
        data["pressure"] = f"{observation['pressure']['value']} {units['pressure']}"

        return data


# Weather.getWeather("Iran, Islamic Republic of", "azarbayjan-e-sharqi", "tabriz")
# Weather.getWeather("canada", "ontario", "toronto")



