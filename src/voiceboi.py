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
from weather import weatherResultError
from math import ceil
import numpy

class VoiceAssistant():
    def __init__(self,lang,username):
        self.SR =  SR.Recognizer()
        self.Microphone = SR.Microphone()
        self.lang = lang
        self.username = username
        self.wikiParams = numpy.array(['who is', 'what is'])

    def run(self):
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
                
                if 'time' in str.lower(result):
                    unformTIME = datetime.now()
                    formattedtime = unformTIME.strftime('%I:%M %p')
                    speech = gTTS(text=f'Current time is {formattedtime}.', lang=self.lang,slow=False)
                    speech.save('Time.mp3')
                    playsound.playsound('Time.mp3')
                elif any(i in str.lower(result) for i in self.wikiParams):
                    res = wikipedia.summary(result,sentences = 2)
                    speech = gTTS(text=f'{res}', lang=self.lang,slow=False)
                    speech.save('wiki.mp3')
                    playsound.playsound('wiki.mp3')
                elif 'play' in str.lower(result):
                    formatresult = result.replace(" ", "+")
                    url = f'https://www.youtube.com/results?search_query={formatresult}'
                    YoutubeResult = urllib.request.urlopen(url)
                    videos_results = re.findall(r"watch\?v=(\S{11})",YoutubeResult.read().decode()) # Parsing to an array of youtuber video_ids
                    VidResult = 'https://www.youtube.com/watch?v=' + videos_results[0] # Setting video Url from the best result of the search.
                    webbrowser.get().open_new(VidResult)
                elif 'weather' in str.lower(result):
                    splittedResult = result.split()
                    del splittedResult[0:len(splittedResult) - 1]
                    initWeather = SetupWeatherForcasting('YOUR_WEATHER_API_KEY_HERE') # YOU NEED TO WRITE YOUR API KEY HERE, READ THE README.MD FILE FOR MORE INFORMATION ABOUT GETTING YOUR API KEY!
                    weatherResult = initWeather.findWeather(splittedResult[0])[0]
                    temp = weatherResult['temp']
                    precepChance = weatherResult['precip']
                    speech = gTTS(text=f'In {splittedResult[0]} it is {ceil(int(temp))} celcius with {ceil(int(precepChance))}% chance of precipitation', lang=self.lang,slow=False)
                    speech.save('weather.mp3')
                    playsound.playsound('weather.mp3')
                else:
                    speech = gTTS(text=f"Sorry, i didn't get that.", lang=self.lang,slow=False)
                    speech.save('Unrecognized.mp3')
                    playsound.playsound('Unrecognized.mp3')    
            except BaseException as e:
                print(e)
                speech = gTTS(text=f"An error occured, please try again.", lang=self.lang,slow=False)
                speech.save('Error.mp3')
                playsound.playsound('Error.mp3')
    

VoiceAssistant(lang='en',username='your_username_here').run() 
"""
Change "EN" to your specific language's code form, if you don't want it to speak in english.
Change your_username_here to your desired username.
"""