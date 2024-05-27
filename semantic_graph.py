from flask import Flask, render_template, request
from spacy import displacy
import spacy

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")

# Маппинг для переобозначения зависимостей на русский язык
dependency_mapping = {
    "ROOT": "корень",
    "acl": "придаточное определение",
    "acomp": "сравнительное дополнение",
    "advcl": "дополнение с наречием",
    "advmod": "наречие",
    "agent": "агент",
    "amod": "определение",
    "appos": "приложение",
    "attr": "атрибут",
    "aux": "вспомогательный глагол",
    "auxpass": "вспомогательный глагол в страдательном залоге",
    "case": "падеж",
    "cc": "союз",
    "ccomp": "сравнительная подчиненная часть",
    "compound": "составное слово",
    "conj": "соединительный союз",
    "csubj": "подчиненное подлежащее",
    "csubjpass": "подчиненное подлежащее в страдательном залоге",
    "dative": "дативный падеж",
    "dep": "зависимость",
    "det": "определитель",
    "dobj": "прямое дополнение",
    "expl": "эксплетив",
    "intj": "междометие",
    "mark": "маркер",
    "meta": "мета",
    "neg": "отрицание",
    "nmod": "модификатор имени",
    "npadvmod": "модификатор наречия",
    "nsubj": "подлежащее",
    "nsubjpass": "подлежащее в страдательном залоге",
    "nummod": "числительное",
    "oprd": "объектный предикат",
    "parataxis": "парадигматический союз",
    "pcomp": "предложение сравнения",
    "pobj": "объект предложения",
    "poss": "собственность",
    "preconj": "предложный союз",
    "predet": "предложный определитель",
    "prep": "предлог",
    "prt": "партитивный род",
    "punct": "пунктуация",
    "quantmod": "квантор",
    "relcl": "относительное предложение",
    "xcomp": "нефинитное дополнение",
    "obl": "косвенный падеж",
    "ADJ": "прилагательное",
    "ADP": "предлог",
    "ADV": "наречие",
    "AUX": "вспомогательный глагол",
    "CCONJ": "союз",
    "DET": "определитель",
    "INTJ": "междометие",
    "NOUN": "существительное",
    "NUM": "числительное",
    "PART": "частица",
    "PRON": "местоимение",
    "PROPN": "имя собственное",
    "PUNCT": "пунктуация",
    "SCONJ": "подчинительный союз",
    "SYM": "символ",
    "VERB": "глагол",
    "X": "другое"
}


def map_dependencies(token):
    return dependency_mapping.get(token.dep_, token.dep_)


def process_semantic_graph_request(request):
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        # Обработка предложения с помощью spaCy
        doc = nlp(sentence)

        # Визуализация семантического графа с переобозначенными зависимостями
        svg = displacy.render(
            doc, style="dep",
            options={"compact": True, "bg": "#ffffff", "color": "#000000", "font": "Arial", "distance": 200,
                     "word_spacing": 50,
                     "fine_grained": True, "deprecation_warning": False},
            jupyter=False
        )

        # Замена меток зависимостей в SVG-разметке
        for old_dep, new_dep in dependency_mapping.items():
            svg = svg.replace(old_dep, new_dep)

        return render_template('semantic_graph.html', svg=svg)


    else:
        return render_template('semantic_graph.html')


__all__ = ['process_semantic_graph_request']  # Экспорт
