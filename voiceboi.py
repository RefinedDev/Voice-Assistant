import speech_recognition as SR
from gtts import gTTS
from datetime import datetime
import playsound
import wikipedia

class Access():
    def __init__(self,main,mic,lang):
        self.Srmain = main
        self.Mic = mic
        self.lang = lang
        self.WikiCheckList = ['who is','what is']

    def start(self):
        with self.Mic as source:
            speech = gTTS(text=f'How can i help you?', lang=self.lang,slow=False)
            speech.save('Welcome.mp3')
            playsound.playsound('Welcome.mp3')

            self.Srmain.adjust_for_ambient_noise(source)
            query = self.Srmain.listen(source)
            try:
                result = self.Srmain.recognize_google(query)
                print(result)
                print('Transcribing, please wait...')
                if 'time' in str.lower(result):
                    unformTIME = datetime.now()
                    formattedtime = unformTIME.strftime('%I:%M %p')
                    speech = gTTS(text=f'Current time is {formattedtime}.', lang=self.lang,slow=False)
                    speech.save('Time.mp3')
                    playsound.playsound('Time.mp3')
                elif any(value in str.lower(result) for value in self.WikiCheckList):
                    res = wikipedia.summary(result,sentences = 2)
                    speech = gTTS(text=f'According to wikipedia,{res}', lang=self.lang,slow=False)
                    speech.save('wiki.mp3')
                    playsound.playsound('wiki.mp3')
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
    
Srmain = SR.Recognizer()
Mic = SR.Microphone()

Access(Srmain,Mic,'en').start()