import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import requests
import serial
import time

def time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    print('Current time is ' + time)
    talk('Current time is ' + time)

def weather():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = 'Perambalur'
    O_W_API_KEY = 'Your API KEY'
    URL = BASE_URL + "q=" + CITY + "&appid=" + O_W_API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp'] - 273.15
        humidity = main['humidity']
        pressure = main['pressure']
        report = data['weather']
        print(f"Temperature is {temperature} celsius.")
        print(f"Humidity is {humidity} %.")
        print(f"Pressure is {pressure} Hectopascal.")
        print(f"Weather is {report[0]['description']}.")
        talk(f"Temperature is {temperature} degree celsius.")
        talk(f"Humidity is {humidity} %.")
        talk(f"Pressure is {pressure} Hectopascal.")
        talk(f"Weather is {report[0]['description']}.")
    else:
        print("Error in the HTTP request")
        talk("Error in the HTTP request")

recording = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 130)

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk("Hello Harry!")
hour = int(datetime.datetime.now().hour)
if hour >= 0 and hour < 12:
    talk("Good Morning!")

elif hour >= 12 and hour < 18:
    talk("Good Afternoon!")

else:
    talk("Good Evening!")

def take_command():
    with sr.Microphone() as source:
        recording.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recording.listen(source)
        command = recording.recognize_google(audio)
    return command


def run_Hardin():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'how are you' in command:
        print('Yeah, I am fine. And you?')
        talk('Yeah, I am fine. And you?')

    elif 'I am fine' in command:
        print('Nice')
        talk('Nice')

    elif 'your name' in command:
        print('My name is Hardin')
        talk('My name is Hardin')

    elif 'who are you' in command:
        print('I am Hardin, your virtual personal assistant.')
        talk('I am Hardin, your virtual personal assistant.')

    elif 'my name' in command:
        print('your name is Harry')
        talk('your name is Harry')

    elif 'what are you doing' in command:
        print('I just searching some information to you')
        talk('I just searching some information to you')

    elif 'time' in command:
        time()

    elif 'weather' in command or 'about the day' in command or 'good morning' in command or 'good afternoon' in command or 'good evening' in command or 'temperature' in command:
        time()
        weather()

    elif 'light' in command:
        command = command.replace('light', '')
        if 'on' in command:
            serialcomm = serial.Serial('/dev/ttyACM0', 9600)
            serialcomm.timeout = 1
            S = True
            while S == True:
                i = command.strip()
                if i == 'done':
                    print('finished program')
                    break
                serialcomm.write(i.encode())
                #time.sleep(0.5)
                print(serialcomm.readline().decode('ascii'))
                S=False
            serialcomm.close()
        elif 'off' in command:
            serialcomm = serial.Serial('/dev/ttyACM0', 9600)
            serialcomm.timeout = 1
            while True:
                i = command.strip()
                if i == 'done':
                    print('finished program')
                    break
                serialcomm.write(i.encode())
                #time.sleep(0.5)
                print(serialcomm.readline().decode('ascii'))
                #break
            serialcomm.close()

    elif 'who is Hardin' in command:
        talk('I am hardin')

    elif 'who is' in command or 'what is' in command:
        try:
            person = command.replace('what is' or 'who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except:
            person = command.replace('what is' or 'who is', '')
            talk('I found some results for you')
            pywhatkit.search(person)

    elif 'open' in command:
        site = command.replace('open', '')
        print("opening" + site)
        talk("opening" + site)
        webbrowser.open(site+'.com')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'I love you' in command:
        print('Me too, harry')
        talk('Me too, harry')

    else:
        print('I cant understand what you said')
        talk('I cant understand what you said')
while True:
    run_Hardin()
