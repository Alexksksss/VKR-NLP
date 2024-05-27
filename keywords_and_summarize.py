from rake_nltk import Rake
import nltk
import requests


# nltk.download('stopwords')  # Загрузка списка стоп-слов для русского языка

class RakeKeywordExtractor:
    def __init__(self):
        self.rake = Rake(language='russian')  # Указываем язык

    def extract_keywords(self, text):
        # Извлекаем ключевые слова
        self.rake.extract_keywords_from_text(text)
        # Получаем список кортежей (ключевое слово, его оценка)
        keywords = self.rake.get_ranked_phrases()
        word_scores = self.rake.get_word_degrees()
        sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        return keywords, sorted_word_scores


__all__ = ['RakeKeywordExtractor', 'summarize_with_bart']


def summarize_with_bart(text, api_key = "API_KEY"):
    # mod = 'IlyaGusev/rubert_telegram_headlines'
    # mod = 'Nehc/mT5_ru_XLSum'
    # mod = 'IlyaGusev/rugpt3medium_sum_gazeta'
    mod = 'csebuetnlp/mT5_m2o_russian_crossSum'
    url = f"https://api-inference.huggingface.co/models/{mod}"

    payload = {
        "inputs": text,
        "parameters": {"max_length": 200, "min_length": 30, "early_stopping": True}
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    if 'error' in result:
        return result['error']
    else:
        result = response.text
        summary = result  # ["generated_text"]

        return summary


