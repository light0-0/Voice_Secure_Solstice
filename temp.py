import speaker_verification_toolkit.tools as svt
import librosa
import os

def Prediction():
    
    Id=0
    ans=1000000000000
    name=os.listdir("userTest")
    data2, sr = librosa.load(f'userTest/{name[0]}', sr=16000, mono=True)
    print(name[0])
    lst=os.listdir("recording")
    mainAns=[]
    for i in lst:

        temp=0        
        for j in os.listdir(f"recording/{i}"):
            
            data1, sr = librosa.load(f'recording/{i}/{j}', sr=16000, mono=True)
            data1 = svt.rms_silence_filter(data1)
            data2 = svt.rms_silence_filter(data2)

            data1 = svt.extract_mfcc(data1)
            data2 = svt.extract_mfcc(data2) 
              
            val=float(svt.compute_distance(data1,data2))
            temp+=val
        temp=temp/len(os.listdir(f"recording/{i}"))
        mainAns.append([temp,i])    

    for i in mainAns:
        print(i[0],i[1])
        if i[0]<ans:
            Id=i[1] 
            ans=i[0]
    
    return Id 


def prefiction1():
    
    name=os.listdir("userTest")
    
    data2, sr = librosa.load(f'userTest/{name[0]}', sr=16000, mono=True)
    data2 = svt.rms_silence_filter(data2)
    data2 = svt.extract_mfcc(data2) 

    userList=[]
    users=[]
    lst=os.listdir("recording")
    
    for i in lst:        
        for j in os.listdir(f"recording/{i}"):

            data1, sr = librosa.load(f'recording/{i}/{j}', sr=16000, mono=True)
            data1 = svt.rms_silence_filter(data1)
            data1 = svt.extract_mfcc(data1)

            userList.append(data1)
            users.append(i)
    
    Id=svt.find_nearest_voice_data(userList,data2)
    return users[Id]