import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json


class LanguageTranslator:
    def __init__(self):
        self.translation_pipeline = pipeline("translation_en_to_fr")
        self.language_detection_pipeline = pipeline("text-classification", model="lid")

    def translate_text(self, text, target_language):
        translation = self.translation_pipeline(text, target_language=target_language)
        return translation[0]["translation_text"]

    def scrape_word_definition(self, word, language):
        url = f"https://www.xyzdictionary.com/{word}"  # Replace with an actual dictionary website URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        definition_tags = soup.find_all("span", class_="definition")
        definitions = [tag.get_text() for tag in definition_tags]
        return definitions

    def translate_and_get_definition(self, input_text, target_language):
        try:
            detected_language = self.detect_language(input_text)
            translation = self.translate_text(input_text, target_language)
            definitions = self.scrape_word_definition(translation, target_language)
            return {
                "Input Text": input_text,
                "Source Language": detected_language,
                "Translation": translation,
                "Definitions": definitions,
            }
        except Exception as e:
            return {
                "Input Text": input_text,
                "Source Language": "Unknown",
                "Translation": "Error occurred during translation",
                "Definitions": [],
                "Error": str(e),
            }

    def detect_language(self, text):
        detection = self.language_detection_pipeline(text)[0]
        return detection["label"]


def main():
    translator = LanguageTranslator()

    input_text = "Hello"
    target_language = "fr"

    translation_result = translator.translate_and_get_definition(
        input_text, target_language
    )
    print(json.dumps(translation_result, indent=4))


if __name__ == "__main__":
    main()
