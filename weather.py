import pycountry
import requests
import json
from bs4 import BeautifulSoup
from typing import Dict


class WeatherAPI:
    @staticmethod
    def getWeather(country: str, province: str, city: str) -> Dict[str, str]:
        soup = WeatherAPI.getSoup(country, province, city)
        code = WeatherAPI.getCode(soup)
        return WeatherAPI.getData(code)

    @staticmethod
    def getSoup(country: str, province: str, city: str) -> BeautifulSoup:
        url = WeatherAPI.getUrl(country, province, city)
        return BeautifulSoup(requests.get(url).text, "lxml")

    @staticmethod
    def getUrl(country: str, province: str, city: str) -> str:
        base_url = "https://www.theweathernetwork.com/"
        alpha_2 = pycountry.countries.get(name=country).alpha_2
        url = f"{base_url}{alpha_2}/weather/{province}/{city}"
        return url

    @staticmethod
    def getCode(soup: BeautifulSoup) -> str:
        data = soup.find("body", {"class": "no-default-background"}).find(
            "script").text
        index = data.find("7Days: ")
        return data[index + 7:-2].strip()

    @staticmethod
    def getData(code) -> Dict[str, str]:
        url = f"https://weatherapi.pelmorex.com/api/v1/observation/placecode/{code}"
        received_data = json.loads(requests.get(url).text)

        data = dict()
        units = received_data["display"]["unit"]
        observation = received_data["observation"]
        data["temperature"] = (f"{observation['temperature']} "
                               f"°{units['temperature']}")

        data["feelsLike"] = (f"{observation['feelsLike']} "
                             f"°{units['temperature']}")

        data["visibility"] = (f"{observation['visibility']} "
                              f"{units['visibility']}")

        data["wind"] = (f"{observation['wind']['speed']} "
                        f"{observation['wind']['direction']} {units['wind']}")

        data["humidity"] = (f"{observation['relativeHumidity']}"
                            f"{units['relativeHumidity']}")

        data["pressure"] = (f"{observation['pressure']['value']} "
                            f"{units['pressure']}")

        return data
