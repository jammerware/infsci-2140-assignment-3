import re
from nltk.stem.snowball import SnowballStemmer
from Classes.Query import Query
from Classes.Path import Stopwords, Topics


class ExtractQuery:

    # i just did everything in getqueries because it's not good practice to do stuff in the constructor
    # (and this only gets called once)
    def getQuries(self):
        queries = []
        stop_words = self._load_stop_words()

        with open(Topics, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith('<num>'):
                    query = Query()
                    topic_id = int(line.replace('<num> Number: ', '').strip())
                    query.setTopicId(topic_id)
                if line.startswith('<title>'):
                    raw_content = line.replace('<title> ', '').strip()
                    query.setQueryContent(self._preprocess_content(raw_content))
                    queries.append(query)

        return queries

    def _load_stop_words(self):
        with open(Stopwords, 'r') as f:
            return [word.strip() for word in f.readlines()]

    def _preprocess_content(self, content):
        stemmer = SnowballStemmer(language='english')
        stop_words = self._load_stop_words()

        # tokenize, normalize, and remove stop words
        regex = re.compile('[a-zA-Z]+')
        tokenized = regex.findall(content)

        # normalize
        normalized = [stemmer.stem(token.lower()) for token in tokenized]

        # stop word removal
        ret_val = []
        for token in normalized:
            if token not in stop_words:
                ret_val.append(token)

        return ret_val
