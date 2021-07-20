# Things you can do with it currently
You can ask what is something, example - `What is gravity.`<br />
You can ask who is who, example - `Who is Mr Beast`<br />
You can ask your local time, example - `What is the time`<br />
You can ask the weather of any place, example - `Weather in New York`<br />
You can play Youtube Videos, example - `Play Never gonna give you up`

All the questions that you asked are saved so..<br />
You can ask what were your previous questions, example - `What were my previous questions.` (Tells your first 5 questions.)

# Dependancies

To make this work, you need the following modules.

```
pip install SpeechRecognition
pip install playsound
pip install wikipedia
pip install gTTS
pip install pyweatherbit
pip install numpy
```
Ok you're good now.
I didn't make this a PyPi package because... why?

# File saving and respond time
The assistant's respond time will depend on your internet.

The `mp3` files will be saved in the directory where the `voicebot.py` file is located.

# Language change
You can change the language by editing the following line and changing the `first argument` to your language's code form. `Access(lang='your_language_code_form').start()`

You MUST use the language code form, find your language's code form here. https://developers.google.com/admin-sdk/directory/v1/languages

# Setting up the Weather class
To make your weather questions work, you need to initialize the Weather class first with your API Key.

To get your API KEY, visit https://www.weatherbit.io/api and Sign Up!
After logging in, you will see A number of weird characters lined up with the Name (KEY), that is your api Key!
Copy your API key, and paste it in the function where you initialize the Weather class! 
`SetupWeatherForcasting(your_api_key_here)`

Boom! You're good to go.

PS: IT TAKES 1 - 2 Hours for your API KEY To actually work after making the account!