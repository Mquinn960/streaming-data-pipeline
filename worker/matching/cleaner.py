class Cleaner():
    
    def __init__(self):
        pass
    
    def strip_escapes(self, sentence_str):
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        sentence_str = sentence_str.translate(translator)
        return self._strip_unicode(sentence_str)

    def _strip_unicode(self, sentence_str):
        return sentence_str.encode('ascii', 'ignore').decode('utf-8')
