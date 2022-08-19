from datetime import datetime
from random import random
#import datetime
import subprocess
import pyttsx3
import speech_recognition as sr
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
from decouple import config
import encrypt
#import json
import requests
#from urllib.request import Request, urlopen

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",178)

def speak(audio):
       engine.say(audio) 
       engine.runAndWait() #Without this command, speech will not be audible to us.

def wishMe():
       hour = datetime.now().hour
       if (hour >= 6) and (hour < 12):
              speak(f"Good Morning")
       elif (hour >= 12) and (hour < 16):
              speak(f"Good afternoon")
       elif (hour >= 16) and (hour < 19):
              speak(f"Good Evening")

def takeCommand():
       #It takes microphone input from the user and returns string output
       r = sr.Recognizer() #recogniser class
       with sr.Microphone() as source:
              print("Listening...")
              #try all thresholds using ctrl and clicking on below pause_threshold
              r.pause_threshold = 1 # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
              r.energy_threshold=3000 
              audio = r.listen(source)
       try:
              print("Recognizing...")    
              query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
              print(f"You said: {query}\n")  #User query will be printed. f string(f)

       except Exception as e:
              # print(e)    
              print("Please say that again...")   #Say that again will be printed in case of improper voice recognition
              return "None" #None string will be returned
       return query

def sendEmail(to, content):
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.ehlo()
       server.starttls()
       server.login('surabhimahale12@gmail.com', encrypt.password) #provide your gmail account password here
       server.sendmail('surabhimahale12@gmail.com', to, content)
       server.close()

def tellDay():
      
    # This function is for telling the
    # day of the week
    day = datetime.today().weekday() + 1
      
    #this line tells us about the number 
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday', 
                3: 'Wednesday', 4: 'Thursday', 
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
      
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)

def tellTime():
      
    # This method will give the time
    datetime1 = str(datetime.now())
      
    # the time will be displayed like 
    # this "2020-06-05 17:50:14.582630"
    #nd then after slicing we can get time   
    hour = datetime1[11:13]
    min = datetime1[14:16]
    print(hour+" "+min)
    speak("The time iz " + hour + " ours and" + min + "Minutes")

  
def take_query():
        while True:
              query = takeCommand().lower() #Converting user query into lower case
        # Logic for executing tasks based on query
              if 'wikipedia' in query: #if wikipedia found in the query then this block will be executed
                     speak('Searching Wikipedia...')
                     query = query.replace("wikipedia", "")
                     results = wikipedia.summary(query, sentences=2) #(sentences)for no. of sentecnes from wikipedia in result
                     speak("According to Wikipedia")
                     print(results)
                     speak(results)

              elif 'open youtube' in query:
                     speak("Opening Youtube ")
                     webbrowser.open("youtube.com")

              elif 'open google' in query:
                     speak("Opening Google ")
                     webbrowser.open("google.com")

              elif 'open geeks for geeks' in query:
                     speak("Opening geeks for geeks ")
                     webbrowser.open("geeksforgeeks.org")
              
              elif 'play' in query:
                     song=query.split(" ")
                     url="https://www.youtube.com/watch/"+song[1]
                     webbrowser.open(url)
   
              elif 'the time' in query:
                     tellTime()
                     continue
              
              elif "day" in query:
                     tellDay()
                     continue
              
              elif 'open i d l e' in query:
                     speak("Opening IDLE ")
                     codePath = "C:\\Users\\Devesh\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Python 2.7\\IDLE (Python GUI).lnk"
                     os.startfile(codePath)
              
              elif 'open chrome' in query:
                     speak("Opening Chrome ")
                     codePath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk"
                     os.startfile(codePath)
              
              elif 'open edge' in query:
                     speak("Opening edge ")
                     codePath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk"
                     os.startfile(codePath)
              
              elif 'send email to' in query:
                     email_dict={'Tejas': 'tejaslahase999@gmail.com', 'Surabhi': 'surabhimahale12@gmail.com','chetna': 'chetanamahale05@gmail.com', 'neha': 'nehaushir54@gmail.com','rupali': 'rupalikale12@gmail.com'}
                     query = query.split(" ")
                     print(email_dict[query[3]])

                     try:
                            speak("What should I say?")
                            content = takeCommand() #returns user input as string
                            to = email_dict[query[3]]    
                            sendEmail(to, content)
                            speak("Email has been sent!")
                     except Exception as e:
                            print(e)
                            speak("Apologies your highness")
                            speak("The email could not be sent!")    

              #for weather forecast
              elif "weather" in query:
                     api_key="46f8e23f67c8ed06353aceb89534d5f5"
                     base_url="https://api.openweathermap.org/data/2.5/weather?"
                     speak("what is the city name")
                     print("what is the city name")
                     city_name=takeCommand()
                     complete_url=base_url+"appid="+api_key+"&q="+city_name
                     response = requests.get(complete_url)
                     x=response.json()
                     if x["cod"]!="404":
                            y=x["main"]
                            kelvin_temperature=y["temp"]
                            current_temperature = kelvin_temperature-273.15 #kelvin to celsius
                            current_humidiy = y["humidity"]
                            z = x["weather"]
                            weather_description = z[0]["description"]
                            print(" Temperature in degree celsius = " +str(current_temperature) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
                            speak(" Temperature in degree celsius is " +str(current_temperature) +"\n humidity in percentage is " +str(current_humidiy) +"\n description  " +str(weather_description))
              
              elif "where is" in query:
                     query = query.split(" ")
                     location_url = "https://www.google.com/maps/place/" + str(query[2])
                     speak(" Your Highness I will show you where " + query[2] + " is.")
                     #maps_arg = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + location_url
                     #os.system(maps_arg)
                     webbrowser.open(location_url)

              elif "your name" in query:
                     speak("Your highness,I am Anna 1 point 0. Your very own deskstop Assistant")
              
              elif "something about us" in query:
                     print("Your Majesty My masters have built me especially for their micro-project They expect praise from you in the form of great marks L O L")
                     speak("Your Majesty")
                     speak("My masters have built me especially for their micro-project")
                     speak("They expect praise from you in the form of reallygood marks , Hahaha!")
              
              elif "quit" in query:
                     speak("Qveeting")
                     exit()

              elif "log off" in query or "sign out" in query:
                     speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                     subprocess.call(["shutdown", "/l"]) #logout windows pc

              elif "restart" in query:
                     speak("ok, restarting your pc" )
                     subprocess.call(["shutdown", "/r"]) #restart windows pc			

if __name__=="__main__" :
       #wishMe()
       #speak("Your Highness! Ana at your service ") 
       take_query()
       #takeCommand() 