import pymorphy2
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from collections import Counter
import requests


class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.words = self.extract_words()

    def count_words(self):
        """Подсчет общего количества слов"""
        return len(self.words)

    def extract_words(self):
        """Извлечение слов из текста"""
        # Разделение текста на слова
        words = self.text.split()
        return words

    def analyze_words(self):
        """Анализ морфологии слов"""
        morph = pymorphy2.MorphAnalyzer()
        analyzed_words = []
        for word in self.words:
            # Получение нормальной формы слова
            normal_form = morph.parse(word)[0].normal_form
            # Получение грамматической информации о слове
            gramm_info = morph.parse(word)[0].tag
            # Добавление результатов анализа в список
            analyzed_words.append((word, normal_form, gramm_info))
        return analyzed_words

    def count_nouns(self):
        """Подсчет существительных в тексте"""
        nouns_count = 0
        morph = pymorphy2.MorphAnalyzer()
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            if 'NOUN' in parsed_word.tag:
                nouns_count += 1
        return nouns_count

    def count_verbs(self):
        """Подсчет глаголов в тексте"""
        verbs_count = 0
        morph = pymorphy2.MorphAnalyzer()
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            if 'VERB' in parsed_word.tag:
                verbs_count += 1
        return verbs_count

    def find_verbs(self):
        """Поиск глаголов в тексте"""
        verbs = []
        morph = pymorphy2.MorphAnalyzer()
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            if 'VERB' in parsed_word.tag:
                verbs.append(word)
        return verbs

    def find_nouns(self):
        """Поиск существительных в тексте"""
        nouns = []
        morph = pymorphy2.MorphAnalyzer()
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            if 'NOUN' in parsed_word.tag:
                nouns.append(word)
        return nouns

    def analyze_word_forms(self, word):
        """Анализ грамматических форм заданного слова"""
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(word)[0]
        table = PrettyTable(["Часть речи", "Грамматическая форма"])
        for form in parsed_word.lexeme:
            table.add_row([form.tag.POS, form.inflect({'nomn'}).word])
        print(table)

    def count_word_frequency(self):
        """Подсчет частоты встречаемости слов"""
        word_freq = Counter(self.words)
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
        return list(sorted_word_freq.items())

    def analyze_pos(self):
        """Анализ частей речи в тексте"""
        morph = pymorphy2.MorphAnalyzer()
        pos_count = Counter()
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            pos_count[parsed_word.tag.POS] += 1
        pos_count = dict(sorted(pos_count.items(), key=lambda x: x[1], reverse=True))
        return list(pos_count.items())

    def extract_named_entities(self):
        """Извлечение именованных сущностей"""
        morph = pymorphy2.MorphAnalyzer()
        named_entities = []
        for word in self.words:
            parsed_word = morph.parse(word)[0]
            # print('В именованной сущности', parsed_word, parsed_word.tag)
            if ('Name' in parsed_word.tag or 'Surn' in parsed_word.tag or 'Patr' in parsed_word.tag or
                    'Geox' in parsed_word.tag or 'Orgn' in parsed_word.tag or 'Trad' in parsed_word.tag):
                # Проверка на именованные сущности
                named_entities.append(word)
        return named_entities

    def get_adjective_word_forms(self, morph, word):
        parsed_word = morph.parse(word)[0]

        cases = {'nomn': 'именительный',
                 'gent': 'родительный',
                 'datv': 'дательный',
                 'accs': 'винительный',
                 'ablt': 'творительный',
                 'loct': 'предложный',
                 'None': '-'
                 }

        number = {'plur': 'множественное число',
                  'sing': 'единственное число',
                  'None': '-'
                  }

        genders = {'masc': 'мужской', 'neut': 'средний', 'femn': 'женский', 'None': '-'}

        lexeme = parsed_word.lexeme
        for parse in lexeme:
            if 'Supr' in str(parse.tag):
                degree = 'превосходная'
            elif 'Qual' in str(parse.tag):
                degree = 'качественная'
            else:
                degree = '-'
            result_info = (f"{parse.word}, {genders[str(parse.tag.gender)]},"
                           f" {cases[str(parse.tag.case)]}, {number[str(parse.tag.number)]},  {degree}")
            print(result_info)

    def get_noun_word_forms(self, morph, word):
        parsed_word = morph.parse(word)[0]

        cases = {'nomn': 'именительный',
                 'gent': 'родительный',
                 'datv': 'дательный',
                 'accs': 'винительный',
                 'ablt': 'творительный',
                 'loct': 'предложный',
                 'None': '-'
                 }

        number = {'plur': 'множественное число',
                  'sing': 'единственное число',
                  'None': '-'
                  }

        genders = {'masc': 'мужской', 'neut': 'средний', 'femn': 'женский', 'None': '-'}

        lexeme = parsed_word.lexeme
        for parse in lexeme:
            result_info = (f"{parse.word}, {genders[str(parse.tag.gender)]},"
                           f" {cases[str(parse.tag.case)]}, {number[str(parse.tag.number)]}")
            print(result_info)

    def get_verb_word_forms(self, morph, word):
        parsed_word = morph.parse(word)[0]
        persons = {'1per': '1-л',
                   '2per': '2-л',
                   '3per': '3-л',
                   'None': '-'
                   }

        times = {'pres': 'Н.в.',
                 'past': 'П.в.',
                 'futr': 'Б.в.',
                 'None': '-'
                 }

        number = {'plur': 'Множ',
                  'sing': 'Ед',
                  'None': '-'
                  }

        genders = {'masc': 'мужской', 'neut': 'средний', 'femn': 'женский', 'None': '-'}

        lexeme = parsed_word.lexeme
        for parse in lexeme:
            result_info = (f"{parse.word} - {persons[str(parse.tag.person)]}, "
                           f"{genders[str(parse.tag.gender)]},"
                           f"  {times[str(parse.tag.tense)]}, {number[str(parse.tag.number)]}")
            print(result_info)

    def get_all_word_forms(self):
        """Извлечение всех словоформ"""
        morph = pymorphy2.MorphAnalyzer()

        word = morph.parse('прекрасный')[0].normal_form
        parsed_word = morph.parse(word)[0]
        pos = parsed_word.tag.POS
        if pos == 'NOUN':
            self.get_noun_word_forms(morph, word)

        elif pos == 'VERB' or pos == 'INFN':
            self.get_verb_word_forms(morph, word)
        elif pos == 'ADJF' or pos == 'ADJS':
            self.get_adjective_word_forms(morph, word)

    def plot_word_frequency(self, num_words=10):
        """Визуализация частоты встречаемости слов"""
        word_freq = self.count_word_frequency()
        top_words = Counter(word_freq).most_common(num_words)
        words, frequencies = zip(*top_words)
        plt.bar(words, frequencies)
        plt.xlabel('Слово')
        plt.ylabel('Частота')
        plt.title('Топ {} слов по частоте встречаемости'.format(num_words))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('plot.png')

    def spell_service(self):
        """Проверка на орфографию"""
        text_with_pluses = "&text=".join(self.words)
        r = requests.get(f'https://speller.yandex.net/services/spellservice.json/checkTexts?text={text_with_pluses}')
        if r.status_code == 200:
            words_with_errors = []
            returning_words = []
            data = r.json()
            for word in range(len(self.words)):
                if data[word]:
                    returning_words.append(data[word][0]['s'][0])
                    words_with_errors.append(data[word][0]['word'])
            return returning_words, words_with_errors
        else:
            print(f"Ошибка при выполнении запроса: {r.status_code}")
            return


# Пример использования
if __name__ == "__main__":
    # Пример текста для анализа
    with open('test_texts/text_test.txt', 'r', encoding='utf-8') as file:
        sample_text = file.read()
    # Удаление всех знаков препинания из строки
    cleaned_string = (sample_text.replace(',', '').replace('.', '').replace('!', '')
                      .replace('?', '').replace(':', '').replace(';', '')
                      .replace('-', '').replace('—', '').replace('(', '')
                      .replace(')', ''))

    # Создание экземпляра класса TextAnalyzer
    analyzer = TextAnalyzer(cleaned_string)

    print("\nКоличество слов:", analyzer.count_words())

    # Анализ морфологии слов
    print("\nАнализ морфологии слов:")
    analyzed_words = analyzer.analyze_words()
    for word, normal_form, gramm_info in analyzed_words:
        print(f"Слово: {word}, Нормальная форма: {normal_form}, Грамматическая информация: {gramm_info}")

    print("\nИсправленная орфография:", analyzer.spell_service())

    # Подсчет существительных в тексте
    print("\nКоличество существительных:", analyzer.count_nouns())

    # Поиск глаголов в тексте
    print("\nНайденные глаголы:", analyzer.find_verbs())

    # Подсчет частоты встречаемости слов
    print("Частота встречаемости слов:", analyzer.count_word_frequency())

    # Анализ частей речи
    print("\nАнализ частей речи:", analyzer.analyze_pos())

    # Извлечение именованных сущностей
    print("\nИменованные сущности:", analyzer.extract_named_entities())

    # Вывод всех словоформ
    print("\nСловоформы:")
    analyzer.get_all_word_forms()

    print()

    # Визуализация частоты встречаемости слов
    # analyzer.plot_word_frequency()
# TODO: gtts нужен ли текст ту спич?
__all__ = ['TextAnalyzer']