import string

from nltk import word_tokenize
from nltk.corpus import stopwords

class LiteraryFile:
    def __init__(self, filename):
        self.filename = filename
        if len(filename.split("_"))>1:
            self.set_language(filename.split("_")[1].split(".")[0])

    def set_language(self, _lang):
        if _lang.lower() in stopwords.fileids():
            self.language = _lang
            self.stop_words = set(stopwords.words(self.language))
            return
        raise Exception(f"Language {_lang} not available")

    def normalize_text(self,data):
        data = data.translate(string.punctuation)
        word_tokens = word_tokenize(data)
        filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in self.stop_words]
        return filtered_sentence

    def max_number_words(self):
        _sum = 0
        word_count= 0
        for line in open(self.filename,'r',encoding='utf-8'):
            _sum+=1
            word_count = max([word_count,len(line.split(" "))])
        return _sum*word_count

    def read_file(self):
        f = open(self.filename, 'r', encoding="utf-8")
        line = f.readline()
        while line:
            yield self.normalize_text(line)
            line = f.readline()
