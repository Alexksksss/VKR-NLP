from flask import Flask, render_template, request
from semantic_graph import process_semantic_graph_request
from comparing import TextComparing
from translator import translate_text
from text_tone import check_tone
from keywords_and_summarize import RakeKeywordExtractor, summarize_with_bart
from main import TextAnalyzer

app = Flask(__name__)


# TODO:  all_word_forms=analyzer.get_all_word_forms()
# TODO: перевести на русский анализ морфологии; добавить график частотности

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translator', methods=['GET', 'POST'])
def translator():
    if request.method == 'POST':
        text_to_translate = request.form.get('value1')

        translated_text = translate_text(text_to_translate, target_language='en')
        return render_template('translator.html', result=f"{translated_text}")

    return render_template('translator.html')


@app.route('/sentiment-analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    if request.method == 'POST':

        if 'file' not in request.files:
            return "Файл не был загружен."
        file = request.files['file']

        if file.filename == '':
            return "Имя файла не было указано."

        lines = []
        for line in file:
            decoded_line = line.decode("utf-8")
            cleaned_line = decoded_line.strip()
            lines.append(cleaned_line)
        translated_lines = []
        for line in lines:
            translated_line = translate_text(line)
            translated_lines.append(translated_line)
        # Проверяем тональность текста
        tones = []
        for translated_line in translated_lines:
            tone, info = check_tone(translated_line)
            tones.append([tone, info])
        res = 0
        for tone in tones:
            res += tone[1].polarity
        res = res/len(tones)
        res = 2*res+3
        res = f'Средняя оценка = {res}'
        return render_template('sentiment_analysis.html', result=tones, res_tone=res)
    return render_template('sentiment_analysis.html')


@app.route('/keywords-summarization', methods=['GET', 'POST'])
def keywords_summarization():
    if request.method == 'POST':

        if 'file' not in request.files:
            return "Файл не был загружен."
        file = request.files['file']

        if file.filename == '':
            return "Имя файла не было указано."

        keyword_extractor = RakeKeywordExtractor()

        text = file.read().decode("utf-8")

        # Извлекаем ключевые слова из текста
        keywords, word_score = keyword_extractor.extract_keywords(text)

        summary = summarize_with_bart(text)

        return render_template('keywords_summarization.html', keywords=word_score, summary=summary)
    return render_template('keywords_summarization.html')


@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    if request.method == 'POST':
        value1 = request.form.get('value1')
        value2 = request.form.get('value2')

        if not value1 or not value2:
            return render_template('comparison.html', error='Оба поля должны быть заполнены.')

        similarity_checker = TextComparing(value1, value2)
        similarity_score, distance = similarity_checker.similarity_score()

        return render_template('comparison.html', result=f"Схожесть текстов: {similarity_score*100}%, расстояние: {distance}")

    return render_template('comparison.html')


@app.route('/semantic-graph', methods=['GET', 'POST'])
def semantic_graph():
    return process_semantic_graph_request(request)


@app.route('/morphological-analysis', methods=['GET', 'POST'])
def morphological_analysis():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Файл не был загружен."
        file = request.files['file']

        if file.filename == '':
            return "Имя файла не было указано."

        sample_text = file.read().decode("utf-8")

        cleaned_string = (sample_text.replace(',', '').replace('.', '').replace('!', '')
                          .replace('?', '').replace(':', '').replace(';', '')
                          .replace('-', '').replace('—', '').replace('(', '')
                          .replace(')', ''))

        # Создание экземпляра класса TextAnalyzer
        analyzer = TextAnalyzer(cleaned_string)
        analyzed_words = analyzer.analyze_words()
        word_count = analyzer.count_words()
        word_freq = analyzer.count_word_frequency()
        # print(f'word_freq{word_freq}')

        return render_template('morphological_analysis.html', word_count=word_count,
                               an_w=analyzed_words, spell_check=analyzer.spell_service(),
                               noun_count=analyzer.count_nouns(), verb_count=analyzer.count_verbs(),
                               find_verbs=analyzer.find_verbs(), find_nouns=analyzer.find_nouns(), word_freq=word_freq,
                               pos=analyzer.analyze_pos(), named_entity=analyzer.extract_named_entities()  #,
                               # all_word_forms=analyzer.get_all_word_forms()
                               )
    return render_template('morphological_analysis.html')


if __name__ == '__main__':
    app.run(debug=True)
