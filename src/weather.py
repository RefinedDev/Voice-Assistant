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

    def findWeather(self,city):
        try:
            weatherForecast = self.weatherApi.get_forecast(city=city)
            weatherResult = weatherForecast.get_series(['temp','precip']) # Subscript the variable to get specific day results [0] = today, [1] = tommorow etc.
            return weatherResult
        except Exception as e:
            raise weatherResultError(e)

# WEATHER RESULTS FOR SOME PLACES CAN BE INACCURATE!


    