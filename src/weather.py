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
import pandas
import matplotlib.pyplot as mp

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

    def createCSVFile(self,RawData,cityName):
        """
        Creates a .csv file from the data given by raw weather data. If there is already a .csv file with the same name as weatherData.csv, it will be overwritten.
        """
        del RawData[7 :]
        dataList = []

        for i in RawData:
            dateStr = str(i['datetime'].strftime("%d %b"))
            temp = str(i['temp'])
            pre = str(i['precip'])

            partialDataFrame = {
                'Date': dateStr,
                'Temp': temp,
                'Chance Of Precipitation': pre
            }

            dataList.append(partialDataFrame)
        
        weatherTable = pandas.DataFrame(dataList)
        weatherTable.set_index('Date')
        weatherTable.to_csv('weatherData.csv')
        df = pandas.read_csv('weatherData.csv',index_col=0)
        print('Here is the data for the weather up to a week\n',df)

        # Show data in graph form
        ax = mp.gca()
        df.plot(kind='bar',x='Date',y='Temp',ax=ax,title=f'Weather data of {cityName} up to a week')
        df.plot(kind='bar',x='Date',y='Chance Of Precipitation', color='red',ax=ax,title=f'Weather data of {cityName} up to a week')
        mp.show()
# WEATHER RESULTS FOR SOME PLACES CAN BE INACCURATE!


    