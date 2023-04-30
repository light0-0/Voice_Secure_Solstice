import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import librosa
import csv
import os
import pandas as pd
import csv
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from keras import models
from keras import layers
import keras
from keras.callbacks import EarlyStopping


TRAIN_CSV_FILE = "train.csv"
TEST_CSV_FILE = "test.csv"
MORE_TRAIN_CSV_FILE = "more_train.csv"
MORE_TEST_CSV_FILE = "more_test.csv"
CREATE_CSV_FILES = True

#For extracting features of training data
def extractWavFeaturesTrainData(soundFilesFolder, csvFileName):
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()

    file = open(csvFileName, 'w', newline='')
    #with file:
    writer = csv.writer(file)
    writer.writerow(header)
    genres = '1 2 3 4 5 6 7 8 9 0'.split()
    
    for filename in os.listdir(soundFilesFolder):
        Name=filename
        
        for itr in os.listdir(f"{soundFilesFolder}/{filename}"):
            number = f'{soundFilesFolder}/{filename}/{itr}'
            y, sr = librosa.load(number, mono=True, duration=30)
            # remove leading and trailing silence
            y, index = librosa.effects.trim(y)
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
            rmse = librosa.feature.rms(y=y)
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
            for e in mfcc:
                to_append += f' {np.mean(e)}'
            to_append += f' {Name}'    
            
            writer.writerow(to_append.split())
          
    file.close()


#For extraxting the features of test data
def extractWavFeaturesTestData(soundFilesFolder, csvFileName):
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()

    file = open(csvFileName, 'w', newline='')
    #with file:
    writer = csv.writer(file)
    writer.writerow(header)
    genres = '1 2 3 4 5 6 7 8 9 0'.split()
    for filename in os.listdir(soundFilesFolder):
        Id=filename.split("-")[0]
        number = f'{soundFilesFolder}/{filename}'
        y, sr = librosa.load(number, mono=True, duration=30)
        # remove leading and trailing silence
        y, index = librosa.effects.trim(y)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        
        to_append += f' {Id}'    
        writer.writerow(to_append.split())
    file.close()




def preProcessData(csvFileName):
    data = pd.read_csv(csvFileName)
    data = data.drop(['filename'],axis=1)
    data = data.drop(['chroma_stft'],axis=1)
    return data




def voiceRecognition():
        
    extractWavFeaturesTrainData("recording", TRAIN_CSV_FILE)
    extractWavFeaturesTestData("userTest", TEST_CSV_FILE)

    
    trainData = preProcessData(TRAIN_CSV_FILE)
    testData = preProcessData(TEST_CSV_FILE)


    X = np.array(trainData.iloc[:, :-1], dtype = float)
    y = trainData.iloc[:, -1]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)




    scaler = StandardScaler()
    X_train = scaler.fit_transform( X_train )
    X_val = scaler.transform( X_val )


    #Creating a Model
    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(100000, activation='softmax'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
    
    # Learning Process of a model
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    history = model.fit(x=X_train,
                        y=y_train,
                        validation_data=(X_val, y_val),
                        epochs=75,
                        batch_size=128,callbacks=[es])



    testting=np.array(testData.iloc[:, :-1], dtype = float)
    testting = scaler.fit_transform( testting )

    testing_labels = testData.iloc[:, -1]


    y_predict = np.argmax(model.predict(testting), axis=1)


    # print(y_predict)
    # print(testing_labels)
    # for i in range(0,len(y_predict)):
    #     print(f"Predicted user {y_predict[i]} and Actual User {testing_labels[i]}")
    return y_predict[0]