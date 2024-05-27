from textblob import TextBlob


def check_tone(text):
    blob = TextBlob(text)
    tone = blob.sentiment
    if tone.polarity > 0:
        return "Положительная", tone
    elif tone.polarity < 0:
        return "Отрицательная", tone
    else:
        return "Нейтральная", tone


__all__ = ['check_tone']  # Экспорт
