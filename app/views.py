from django.shortcuts import render,redirect
import pyaudio
import wave
import time
from django.urls import reverse
from datetime import datetime, timedelta
import threading
from .models import *
import os
import random
import nltk
from nltk.corpus import brown
from threading import Thread
import json
import speech_recognition as sr
import random
import pandas as pd
from difflib import SequenceMatcher
from voiceBasedCode import *
from temp import *

#Function for returning similarity ratio between 2 sentences
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



#Class for recording the audio of person
class CountdownTask:
	
    def __init__(self):
        self._running = True
        self.status=""

    def terminate(self):
        self._running = False
        
    def run(self, userName,sentence,userPath):
        audio=pyaudio.PyAudio()
        stream=audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        frames=[]

        while self._running:
            data=stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        path=""

        #To check if the user is recording the voice or testing the voice 
        if userPath=="recording":
            Id=UserTable.objects.filter(username=userName)[0].id
            path = f"recording/{Id}"
            # Check whether the specified path exists or not
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            else:
                lt=len([name for name in os.listdir(path)])
                userName=userName+str(lt)    

            sound_file=wave.open(f'{path}/{userName}.wav','wb')
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
            sound_file.close()
        else:
            path="userTest"
            sound_file=wave.open(f'{path}/{userName}.wav','wb')
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
            sound_file.close()

        #Matching the sentence said by user and original sentence
        try:
            audioPath=f"{path}/{userName}.wav"
            r = sr.Recognizer()
            with sr.AudioFile(audioPath) as source:
             audio = r.record(source) 
            
            text=r.recognize_google(audio)  
            
            print(text)
            print(f"original Sentence -- > {sentence}\n \n")
            print(f"\n Similrity between two sentences is {similar(text.lower(),sentence.lower())}")   
            
            if similar(text.lower(),sentence.lower())<0.8:
                self.status="0"
                os.remove(f"{path}/{userName}.wav")
            else:
                self.status="1"

        except Exception as e:
            os.remove(f"{path}/{userName}.wav")
            self.status="0"






#Function for producing random sentences
def randomSentence():
        
    quotes = pd.read_csv(r'quotes.csv')
    randnum = random.randrange(0, 10000, 1)
    randsentence = quotes["0"][randnum]
    return randsentence   







#Function for login page
def login(request):
    if request.method=="POST":
        
        username=request.POST.get("username")
        obj=UserTable.objects.filter(username=username)
        
        if len(obj)==0:
            print(username)
            return render(request,'login.html',{"user":username,"message":f"Username {username} doesn't exist","flag":1})     
        else:
            if obj[0].voiceRecorded<5:
                return redirect(f"/recording-voice-of-{username}-{obj[0].voiceRecorded+1}/")
            return redirect(f"/login-{username}/")
    else:
        print("Hello")
        return render(request,'login.html',{"flag":0})


#Function for sing up page 
def signup(request):

    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        fname=request.POST.get("fname")
        age=request.POST.get("age")

        obj=UserTable.objects.filter(username=username)

        if len(obj)!=0:
                return render(request,'signup.html',{'name':username,'email':email,"fname":fname,"age":age, "message":f"Username {username} is already taken please try any other username"})
        else:   
                obj=UserTable(username=username,email=email,full_name=fname,age=age)
                obj.save()
                return redirect(f"/recording-voice-of-{username}-1/")     
    else:    
       return render(request,'signup.html')



def vba_RulesLogin(request,name):    
    url=f"/{name}-recording-voice/"   
    return render(request,'startRecording.html',{'url':url})



def vba_RulesSignup(request,name,num):    
    url=f"/read-sentence-{name}-{num}/"   
    return render(request,'voice.html',{'url':url,"num":num})


#Class for controlling the thread objects
class ControlThread:
    def __init__(self):
        self.Thread=None

c = CountdownTask()
obj=ControlThread()

#Function for taking the user's input voice for recording
def recordingVoiceUser(request,name,num):
    print(request.method)
    print("*****************")
    if request.method=='POST':        
        c.terminate()
        obj.Thread.join()
        status=c.status 
        print(status)
        print("************************************")
        if status=="0":
            status="You didn't speak the sentence properly"
            url=f"/recording-voice-of-{name}-{num}/"
            return render(request,'Registration.html',{'status':status,'id':1,'name':name,'url':url})
        else:
            if num==5:
                UserTable.objects.filter(username=name).update(voiceRecorded=num)
                status="Your Voice has been recorded successfully and you are registererd successfully"    
                return render(request,'Registration.html',{'status':status,'id':2,'name':name})
            else:
                UserTable.objects.filter(username=name).update(voiceRecorded=num)
                num+=1
                status="Your Voice has been recorded successfully. Please record your Voice for one for time"
                url=f"/recording-voice-of-{name}-{num}/"
                return render(request,'Registration.html',{'status':status,'id':3,'name':name,'url':url})

    
    else:
        sentence=randomSentence()
        c._running = True
        obj.Thread = Thread(target = c.run, args =(name,sentence,"recording" ))
        obj.Thread.start() 
        return render(request,'randomSentence.html',{'name':name,'sentence':sentence,"num":num})
     



#Function for taking the user's input voice for authentication 
def AutheticateUser(request,name):
    
    if request.method=='POST':        
        c.terminate()
        obj.Thread.join()
        status=c.status 
        if status=="0":
            status="You didn't speak the sentence properly"
            url=f"/login-{name}/"
            return render(request,'Registration.html',{'status':status,'id':1,'name':name,'url':url})
        else:
            Id=prefiction1()
            Id1=Prediction()
            print(f"Using first model {Id1}")
            org_id=UserTable.objects.filter(username=name)[0].id
            print(f"{org_id} {Id}")
            os.remove(f"userTest/{name}.wav")
            if str(org_id)==str(Id):
                    
                    url = reverse('noter:home', args=[name])
                    return redirect(url)

            url=f"/login-{name}/" 
            status=f"Your Voice doesn't match with the user {name}'s voice"    
            return render(request,'Registration.html',{'status':status,'id':1,'name':name,'url':url})
    
    else:
        sentence=randomSentence()
        c._running = True
        obj.Thread = Thread(target = c.run, args =(name,sentence,"userTest" ))
        obj.Thread.start() 
        return render(request,'randomSentence1.html',{'name':name,'sentence':sentence})