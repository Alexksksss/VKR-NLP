import re


class TextComparing:
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def preprocess_text(self, text):
        # Приводим текст к нижнему регистру
        text = text.lower()
        # Удаляем знаки препинания и лишние пробелы
        text = re.sub(r'[^\w\s]', '', text)
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        return text

    def levenshtein_distance(self, s1, s2):
        # Создаем матрицу и преобразуем строки
        matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        s1 = ' ' + s1
        s2 = ' ' + s2

        # Инициализируем первую строку и первый столбец
        for i in range(len(s1)):
            matrix[i][0] = i
        for j in range(len(s2)):
            matrix[0][j] = j

        # Заполняем матрицу
        for i in range(1, len(s1)):
            for j in range(1, len(s2)):
                cost = 0 if s1[i] == s2[j] else 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

        # Возвращаем значение расстояния Левенштейна
        return matrix[-1][-1]

    def levenstein(self, str_1, str_2):
        n, m = len(str_1), len(str_2)
        if n > m:
            str_1, str_2 = str_2, str_1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str_1[j - 1] != str_2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    def similarity_score(self):
        # Обработка текста перед вычислением расстояния Левенштейна
        processed_text1 = self.preprocess_text(self.text1)
        processed_text2 = self.preprocess_text(self.text2)

        # Вычисляем расстояние Левенштейна между обработанными текстами
        distance = self.levenstein(processed_text1, processed_text2)

        # Вычисляем схожесть текстов
        max_length = max(len(processed_text1), len(processed_text2))
        similarity = 1 - (distance / max_length)

        return similarity, distance


__all__ = ['TextComparing']  # Экспорт
