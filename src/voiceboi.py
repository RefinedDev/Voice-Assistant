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

initWeather = SetupWeatherForcasting('YOUR_WEATHER_API_KEY_HERE') # YOU NEED TO WRITE YOUR API KEY HERE, READ THE README.MD FILE FOR MORE INFORMATION ABOUT GETTING YOUR API KEY!

class VoiceAssistant():
    def __init__(self,lang : str,username : str):
        self.SR =  SR.Recognizer()
        self.Microphone = SR.Microphone()
        self.lang = lang
        self.username = username
        self.wikiParams = numpy.array(['who is', 'what is'])

    def saveAndPlaySound(self,text : str,soundName : str):
        speech = gTTS(text=text, lang=self.lang,slow=False)
        speech.save(f'{soundName}.mp3')
        playsound.playsound(f'{soundName}.mp3')

    def run(self):
        """
        Runs the Assistant.
        """
        with self.Microphone as source:
            self.saveAndPlaySound(f'Hello {self.username}, how can i help you?','Welcome')

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
                    self.saveAndPlaySound(f'Current time is {formattedtime}.','Time')
                    questionAsked = True
                elif any(i in str.lower(result) for i in self.wikiParams):
                    res = wikipedia.summary(result,sentences = 2)
                    self.saveAndPlaySound(f'{res}','wiki')
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
                    weatherResultRaw = initWeather.findWeather(splittedResult[0])
                    weatherResult = weatherResultRaw[0]
                    temp = weatherResult['temp']
                    precepChance = weatherResult['precip']
                    self.saveAndPlaySound(f'In {splittedResult[0]} it is {ceil(int(temp))} celcius with {ceil(int(precepChance))}% chance of precipitation','weather')
                    questionAsked = True

                    if initWeather.getCSVFilesPermission:
                       initWeather.createCSVFile(RawData=weatherResultRaw,cityName=splittedResult[0])

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

                    self.saveAndPlaySound(f'Your first five questions were,{firstFiveValues[0],firstFiveValues[1],firstFiveValues[2],firstFiveValues[3] and firstFiveValues[4]}','questions')

                    with open('previousQuestions.json','w') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        json.dump({},f,indent=4) # Clearing the old data so that new questions can fill up.
                else:
                    self.saveAndPlaySound(f"Sorry, i didn't get that.",'Unrecog')

                if questionAsked:
                    with open('previousQuestions.json','r') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        data = json.load(f)
                    
                    data[len(data) + 1] = result # Index set to the next highest index, like if the highest index is 1 then it will become 2.

                    with open('previousQuestions.json','w') as f: # You might get directory error, so make sure your code is being excecuted in the SRC file.
                        json.dump(data,f,indent=4)

            except Exception as e:
                print(e)
                self.saveAndPlaySound(f"An error occured, please try again.",'Error')

va = VoiceAssistant(lang='en',username='your_username_here')
"""
Change "EN" to your specific language's code form, if you don't want it to speak in english.
Change your_username_here to your desired username.
"""
initWeather.setCSVfilesforWeathers() # SET THIS TO TRUE IF U WANT IT TO SHOW CSV FILES. DEFAULTS TO FALSE
va.run()

