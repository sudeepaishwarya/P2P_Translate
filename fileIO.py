"""
    This file deals with all the functions related to file IO
"""

import os
import speech_recognition as sr
import sounddevice as sd
import scipy
from scipy.io.wavfile import write
import numpy as np
import time
from googletrans import Translator
from gtts import gTTS

cwd = os.getcwd()

def file_type(file_path):
    while True:
        i = input("Please enter \n 1. To share live audio \n 2. To share recorded audio file \n 3. To share live Text \n 4. To share pre-existing text file\n")
        if i == '1':
            print("Note: The original voice is converted into a prerecorded voice to protect identity")
            duration = 10  # seconds
            fs = 48000
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            time.sleep(15)
            y = (np.iinfo(np.int32).max * (myrecording/np.abs(myrecording).max())).astype(np.int32)
            scipy.io.wavfile.write(file_path+"1.wav", fs, y)
            new_file_path = speech_recog(file_path, file_path+"1.wav")
            return new_file_path
            break
        elif i == '2':
            print("Note: The original voice is converted into a prerecorded voice to protect identity")
            j = input("Please enter the file name: ")
            try:
                f = open(file_path+j)
            except:
                print("File not found")
            new_file_path = speech_recog(file_path, file_path+j)
            return new_file_path
            break
        elif i == '3':
            j = input("Please enter the text you want to send: ")
            save = open(file_path +"read_file.txt","w")
            save.write(j)
            save.close
            return(file_path+"read_file.txt")
            break
        elif i == '4':
            j = input("Please enter the file name: ")
            try:
                f = open(file_path+j)
            except:
                print("File not found")
            return(file_path+j)
            break
        else:
            print("Invalid Input, Try again")

def speech_recog(file_path, audio_file):
    print(sr.__version__)
    r = sr.Recognizer()

    file_audio = sr.AudioFile(audio_file)

    with file_audio as source:
       audio_text = r.record(source)

    print(type(audio_text))
    save = open(file_path +"read_file.txt","w")
    save.write(r.recognize_google(audio_text))
    save.close
    return(file_path+"read_file.txt")


def convert_to_bytes():
    file_path = file_type(cwd + "/server_files/")
    print(file_path)
    read_data = None
    with open(file_path, 'r') as file:
        read_data = file.read()
    return read_data.encode("utf-8")


def translate(new_file, file_path):
    LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'}
    LANGCODES = dict(map(reversed, LANGUAGES.items()))
    lang = input("Please enter the language you want to translate the text/audio to: ")
    while True:
        if lang in LANGCODES:
            language = LANGCODES[lang]
            break
        else:
            print("Language not found, Try again ")
    translator = Translator()
    f = open(new_file, "r")
    src = f.read()
    dst = translator.translate(src, dest=language)
    print(dst.text)
    save = open(file_path +"translated_file.txt","w")
    save.write(dst.text)
    save.close
    speech = gTTS(text = dst.text, lang = language, slow = False)
    speech.save(file_path +"translated_audio.mp3")

def create_file(data):
    new_file_path = cwd + "/client_files/original_file.txt"
    data = data.decode("utf-8")
    print("Writing to file")
    with open(new_file_path, 'w') as file:
        file.write(data)
    translate(cwd + "/client_files/original_file.txt", cwd + "/client_files/")
    return True


def main():
    data = convert_to_bytes()
    create_file(data)


if __name__ == "__main__":
    main()
