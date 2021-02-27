import spacy

from .cleaner import Cleaner

class Tokeniser():

    def __init__(self):            
        self._nlp = self._set_up_model('en_core_web_sm')
        self._cleaning = Cleaner()

    def tokenize(self, sentence):
        sentence = self._cleaning.strip_escapes(str(sentence))
        sentence =  self._nlp(sentence)
        tokens = [token for token in sentence if not token.is_stop and not token.is_punct and len(token.text) != 1 and not token.is_space]
        return tokens

    def _set_up_model(self, model):
        if not spacy.util.is_package(model):
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
        return spacy.load(model)
