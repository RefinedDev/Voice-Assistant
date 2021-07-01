import speech_recognition as SR
from gtts import gTTS
from datetime import datetime
import playsound
import wikipedia
import urllib
import re
import webbrowser

class Access():
    def __init__(self,lang,username):
        self.Srmain =  SR.Recognizer()
        self.Mic = SR.Microphone()
        self.lang = lang
        self.username = username
        self.WikiCheckList = ['who is','what is']


    def start(self):
        with self.Mic as source:
            speech = gTTS(text=f'Hello {self.username}, how can i help you?', lang=self.lang,slow=False)
            speech.save('Welcome.mp3')
            playsound.playsound('Welcome.mp3')

            self.Srmain.adjust_for_ambient_noise(source) # If there's alot of noice in the background, this function will help to compensate for it.
            query = self.Srmain.listen(source) # Listening for the voice. (Yields)
            try:
                result = self.Srmain.recognize_google(query) # Transcribes the voice
                print(result) # The result that was transcribed
                print('Transcribing, please wait...')
                if 'time' in str.lower(result):
                    unformTIME = datetime.now()
                    formattedtime = unformTIME.strftime('%I:%M %p')
                    speech = gTTS(text=f'Current time is {formattedtime}.', lang=self.lang,slow=False)
                    speech.save('Time.mp3')
                    playsound.playsound('Time.mp3')
                elif any(i in str.lower(result) for i in self.WikiCheckList):
                    res = wikipedia.summary(result,sentences = 2)
                    speech = gTTS(text=f'According to wikipedia,{res}', lang=self.lang,slow=False)
                    speech.save('wiki.mp3')
                    playsound.playsound('wiki.mp3')
                elif 'play' in str.lower(result):
                    formatresult = result.replace(" ", "+")
                    url = f'https://www.youtube.com/results?search_query={formatresult}'
                    YoutubeResult = urllib.request.urlopen(url)
                    videos_results = re.findall(r"watch\?v=(\S{11})",YoutubeResult.read().decode()) # Parsing to an array of youtuber video_ids
                    VidResult = 'https://www.youtube.com/watch?v=' + videos_results[0] # Setting video Url
                    webbrowser.get().open_new(VidResult)
                else:
                    speech = gTTS(text=f"Sorry, i didn't get that.", lang=self.lang,slow=False)
                    speech.save('Unrecognized.mp3')
                    playsound.playsound('Unrecognized.mp3')
                    
            except SR.UnknownValueError as e:
                print(e)
                speech = gTTS(text=f"An error occured, please try again.", lang=self.lang,slow=False)
                speech.save('Error.mp3')
                playsound.playsound('Error.mp3')
            except wikipedia.PageError as e:
                print(e)
                speech = gTTS(text=f"An error occured, please try again.", lang=self.lang,slow=False)
                speech.save('Error.mp3')
                playsound.playsound('Error.mp3')
    

Access('en','your_username_here').start() 
# Change "EN" to your specific language's code form, if you don't want it to speak in english.
# Change your_username_here to your desired username.