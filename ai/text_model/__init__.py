import joblib
import re

import validators

from filters import FILTER, SPECIAL_SYMBOLS


CURRENT_PATH = os.path.dirname(__file__)


"""
Ищет персональные данные, мат и проверяет текст на токсичность.
"""


class TextModel:

    def __init__(self):
        self.classifier = joblib.load(CURRENT_PATH + '/model.pkl')

    def preprocess_text_(self, text):
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', text)
        text = re.sub('@[^\s]+','USER', text)
        text = text.lower().replace("ё", "е")
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +',' ', text)
        return text.strip()

    def predict_toxic_(self, samples):
        samples = [self.preprocess_text_(t) for t in samples]
        return self.classifier.predict_proba(samples)

    def is_personal_(self, text):
        # Проверяет, содержит ли текст >= 3 цифер и специальные символы
        num_of_digits = 0
        special_symbols = 0
        for let in text:
            num_of_digits += int(let.isdigit())
            if let in SPECIAL_SYMBOLS:
                special_symbols += 1
        if num_of_digits >= 3 or special_symbols > 0 or validators.url(text):
            return True
        return False

    def user_msg(self, text):
        toxic_level = self.predict_toxic_([text])[0][0]

        words = text.split(' ')
        obscene_vocab = 0
        updated_text = []

        for word in words:
            processed = self.preprocess_text_(word)
            if processed in FILTER:
                obscene_vocab += 1
            if self.is_personal_(word):
                updated_text.append('********')
            else:
                updated_text.append(word)

        updated_text = ' '.join(updated_text)

        return {'text': text, 'updated': updated_text, 'toxic': toxic_level, 'obscene': obscene_vocab}
