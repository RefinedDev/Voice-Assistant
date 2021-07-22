"""
HOW TO SETUP WEATHER MODULE FOR YOUR NEEDINGS.

This module is not setup on it's own, because it requires an API key, that you will make on your own!
To get your API KEY, visit (https://www.weatherbit.io/api) and Sign Up!
After logging in, you will see A number of weird characters lined up with the Name (KEY), that is your api Key!
Copy your API key, and paste it in the function where you initialize the Weather class! 
SetupWeatherForcasting(your_api_key_here) IN THE voiceboi.py script!
Boom! You're good to go.

PS: IT TAKES 1 - 2 Hours for your API KEY To actually work after making the account!
"""

from weatherbit.api import Api

class weatherResultError(Exception):
    pass

class SetupWeatherForcasting():
    def __init__(self,api_key):
        self.apiKey = api_key
        self.weatherApi = Api(self.apiKey)
        self.weatherApi.set_granularity('daily')
        self.csvFilesforWeather = False

    def findWeather(self,city):
        """
        Finds whether for the specified city, will error if City Name is Invalid or No API Key is Registered.
        """
        try:
            weatherForecast = self.weatherApi.get_forecast(city=city)
            weatherResult = weatherForecast.get_series(['temp','precip']) # Subscript the variable to get specific day results [0] = today, [1] = tommorow etc.
            return weatherResult
        except Exception as e:
            raise weatherResultError(e)

    def setCSVfilesforWeathers(self,setCSVFileBOOL : bool = False):
        """
        Enable or disable making CSV files for the weather command, the CSV files have the weather data for a place upto a week, while the Assistant only tells it for the current day.
        """
        self.csvFilesforWeather = setCSVFileBOOL
        print("Setting CSV Files For Weather To ",self.csvFilesforWeather)

    def getCSVFilesPermission(self):
        return self.csvFilesforWeather

# WEATHER RESULTS FOR SOME PLACES CAN BE INACCURATE!


    