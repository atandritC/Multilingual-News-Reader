import googletrans
import requests
import json
from playsound import playsound
from gtts import gTTS
import os
from googletrans import Translator

translator = Translator()
languages = googletrans.LANGUAGES

class NewsPaper:
    def setup(self, stored):
        self.store = stored
        self.speak_up(f"Hello and welcome to Multilingual News Center. Here I am going to give you {len(self.store)} top and hot news headlines. Please tell me your language.")
        
        while True:
            found = False
            self.display_languages()
            print("Enter the number of your language:")
            self.chosen = input().lower()
            
            if self.chosen.isdigit() and 0 < int(self.chosen) <= len(languages):
                self.chosen_lang_code = list(languages.keys())[int(self.chosen) - 1]
                break
            else:
                print("Invalid selection. Please enter the number corresponding to your language.")
        
        print(self.chosen_lang_code)
        self.speak_up(f"Delivering the news in {languages[self.chosen_lang_code]}.")

        for j, headline in enumerate(self.store):
            if j == 0:
                text = "First news is "
                src_lang = self.guess_lang(text)
                self.speak_in_lang(text, src_lang, self.chosen_lang_code)
            elif j < len(self.store) - 1:
                text = "The next news is "
                src_lang = self.guess_lang(text)
                self.speak_in_lang(text, src_lang, self.chosen_lang_code)
            else:
                text = "The last news is "
                src_lang = self.guess_lang(text)
                self.speak_in_lang(text, src_lang, self.chosen_lang_code)
            
            self.speak_in_lang(headline, self.guess_lang(headline), self.chosen_lang_code)
        
        self.speak_in_lang("Thanks for paying attention.", 'en', self.chosen_lang_code)

    def speak_up(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save('speech.mp3')
        playsound('speech.mp3')
        os.remove('speech.mp3')

    def guess_lang(self, title):
        detected_lang = translator.detect(title)
        lang_code = detected_lang.lang
        return lang_code

    def speak_in_lang(self, text, src_id, dest_id):
        translated_text = translator.translate(text, src=src_id, dest=dest_id).text
        tts = gTTS(text=translated_text, lang=dest_id)
        tts.save('sample.mp3')
        playsound('sample.mp3')
        os.remove('sample.mp3')

    def speak_error(self, error):
        tts = gTTS(text=error, lang='en')
        tts.save('error.mp3')
        playsound('error.mp3')
        os.remove('error.mp3')

    def display_languages(self):
        print("Available languages:")
        for i, lang in enumerate(languages.values(), 1):
            print(f"{i}. {lang}")

if __name__ == "__main__":
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=2e5a2cb1608b48a0b6bdab272e8038b4"
    store = []
    np = NewsPaper()

    try:
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            response_dict = response.json()
            for article in response_dict['articles']:
                store.append(article['title'])
            print(store[:7])
            np.setup(store[:5])
        else:
            np.speak_error("The site is not reachable at this moment. Please try again later. Thank you.")
    except Exception as e:
        np.speak_error("Something went wrong, or this language is not supported, or the connection might be lost.")