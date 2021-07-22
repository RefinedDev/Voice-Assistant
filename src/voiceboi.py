"""
 RESULTS MAY BE INACCURATE! PARDON ME.
"""

import speech_recognition as SR
from gtts import gTTS
from datetime import datetime
import playsound
import wikipedia
import urllib
import re
import webbrowser
from weather import SetupWeatherForcasting
from math import ceil
import json
import numpy
import itertools
import pandas
from csv import writer

class VoiceAssistant():
    def __init__(self,lang : str,username : str):
        self.SR =  SR.Recognizer()
        self.Microphone = SR.Microphone()
        self.lang = lang
        self.username = username
        self.wikiParams = numpy.array(['who is', 'what is'])
        self.csvFilesforWeather = False

    def run(self):
        """
        Runs the Assistant.
        """
        with self.Microphone as source:
            speech = gTTS(text=f'Hello {self.username}, how can i help you?', lang=self.lang,slow=False)
            speech.save('Welcome.mp3')
            playsound.playsound('Welcome.mp3')

            self.SR.adjust_for_ambient_noise(source) # If there's alot of noice in the background, this method will help to compensate for it.
            query = self.SR.listen(source) # Listening for the voice.
            try:
                print('Transcribing, please wait...')
                result = self.SR.recognize_google(query) # Transcribes the voice
                print(result)
                questionAsked = False
                if 'time' in str.lower(result):
                    unformTIME = datetime.now()
                    formattedtime = unformTIME.strftime('%I:%M %p')
                    speech = gTTS(text=f'Current time is {formattedtime}.', lang=self.lang,slow=False)
                    speech.save('Time.mp3')
                    playsound.playsound('Time.mp3')
                    questionAsked = True
                elif any(i in str.lower(result) for i in self.wikiParams):
                    res = wikipedia.summary(result,sentences = 2)
                    speech = gTTS(text=f'{res}', lang=self.lang,slow=False)
                    speech.save('wiki.mp3')
                    playsound.playsound('wiki.mp3')
                    questionAsked = True
                elif 'play' in str.lower(result):
                    formatresult = result.replace(" ", "+")
                    url = f'https://www.youtube.com/results?search_query={formatresult}'
                    YoutubeResult = urllib.request.urlopen(url)
                    videos_results = re.findall(r"watch\?v=(\S{11})",YoutubeResult.read().decode()) # Parsing to an array of youtuber video_ids
                    VidResult = 'https://www.youtube.com/watch?v=' + videos_results[0] # Setting video Url from the best result of the search.
                    webbrowser.get().open_new(VidResult)
                    questionAsked = True
                elif 'weather' in str.lower(result):
                    splittedResult = result.split()
                    del splittedResult[0:len(splittedResult) - 1]
                    initWeather = SetupWeatherForcasting('1de9336927f54116acb6a189842a9ccf') # YOU NEED TO WRITE YOUR API KEY HERE, READ THE README.MD FILE FOR MORE INFORMATION ABOUT GETTING YOUR API KEY!
                    weatherResultRaw = initWeather.findWeather(splittedResult[0])
                    weatherResult = weatherResultRaw[0]
                    temp = weatherResult['temp']
                    precepChance = weatherResult['precip']
                    speech = gTTS(text=f'In {splittedResult[0]} it is {ceil(int(temp))} celcius with {ceil(int(precepChance))}% chance of precipitation', lang=self.lang,slow=False)
                    speech.save('weather.mp3')
                    playsound.playsound('weather.mp3')
                    questionAsked = True

                
                    if self.csvFilesforWeather:
                        del weatherResultRaw[7 :]
                        dataList = []

                        for i in weatherResultRaw:
                            dateStr = str(i['datetime'].strftime("%d %b %Y "))
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
                elif 'question' in str.lower(result):
                    with open('previousQuestions.json','r') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        data = json.load(f)

                    firstFiveQuestions = dict(itertools.islice(data.items(),5))
                    firstFiveValues = []

                    for _,v in firstFiveQuestions.items():
                        firstFiveValues.append(v)

                    if len(firstFiveValues) < 5:
                        print("You need to ask more than four questions before using this command.")
                        return;

                    speech = gTTS(text=f'Your first five questions were,{firstFiveValues[0],firstFiveValues[1],firstFiveValues[2],firstFiveValues[3] and firstFiveValues[4]}', lang=self.lang,slow=False)
                    speech.save('previousQuestions.mp3')
                    playsound.playsound('previousQuestions.mp3')

                    with open('previousQuestions.json','w') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        json.dump({},f,indent=4) # Clearing the old data so that new questions can fill up.
                else:
                    speech = gTTS(text=f"Sorry, i didn't get that.", lang=self.lang,slow=False)
                    speech.save('Unrecognized.mp3')
                    playsound.playsound('Unrecognized.mp3') 

                if questionAsked:
                    with open('previousQuestions.json','r') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        data = json.load(f)
                    
                    data[len(data) + 1] = result # Index set to the next highest index, like if the highest index is 1 then it will become 2.

                    with open('previousQuestions.json','w') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        json.dump(data,f,indent=4)

            except Exception as e:
                print(e)
                speech = gTTS(text=f"An error occured, please try again.", lang=self.lang,slow=False)
                speech.save('Error.mp3')
                playsound.playsound('Error.mp3')

    def setCSVfilesforWeathers(self,setCSVFileBOOL : bool = False):
        """
        Enable or disable making CSV files for the weather command, the CSV files have the weather data for a place upto a week, while the Assistant only tells it for the current day.
        """
        self.csvFilesforWeather = setCSVFileBOOL
        print("Setting CSV Files For Weather To ",self.csvFilesforWeather)
    

va = VoiceAssistant(lang='en',username='your_username_here')
"""
Change "EN" to your specific language's code form, if you don't want it to speak in english.
Change your_username_here to your desired username.
"""
va.setCSVfilesforWeathers() # SET THIS TO TRUE IF U WANT IT TO SHOW CSV FILES. DEFAULTS TO FALSE
va.run()

