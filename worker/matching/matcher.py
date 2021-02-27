import Levenshtein
import distance

from .tokeniser import Tokeniser

class Matcher():

    term_cache = None
    lev_threshold = 85
    jacc_threshold = 0.25

    tokeniser = None

    def __init__(self, term_cache):
        self.term_cache = term_cache
        self.init_services()

    def init_services(self):
        self.tokeniser = Tokeniser()

    def match(self, menu_item, full_search=True):

        term_matches = {}

        term_matches = self._process_match(menu_item['ProductName'], menu_item)

        if not term_matches:
            if full_search:
                term_matches = self._process_match(menu_item['ProductDescription'], menu_item)

        return term_matches

    def _process_match(self, input_string, menu_item):

        term_matches = {}

        point_match = lambda a, b : a.lower() in b.lower()

        for term_id, term in self.term_cache.items():

            match_found = False

            # If we have a direct match, don't do anything fancy
            if point_match(term, input_string):
                match_found = True
            # Before performing heavy NLP operations
            # Check Jaccard shingle distance of the compared terms
            elif distance.jaccard(term, input_string) > self.jacc_threshold:
                # Now we can perform a distance search on individual linguistic tokens
                tokens = self.tokeniser.tokenize(input_string)
                for token in tokens:
                    token_text = ''
                    # If our tokeniser model returns multi-part tokens, create a string
                    if type(token) is list:
                        token_text = ' '.join([single_token.text for single_token in token])
                    else:
                        token_text = token.text
                    # Don't bother distance searching if the terms don't share any common letters
                    # This uses set intersection for performance
                    if self._terms_share_common_letters(token_text, term):
                        # Perform Levenshtein distancing search on a prefined proximity threshold
                        if self._distance_match(token_text, term):
                            match_found = True

            if match_found:
                match_record = {}
                match_record[term] = menu_item
                term_matches[term_id] = match_record

        return term_matches

    def _terms_share_common_letters(self, term1, term2):

        return len(''.join(set(term1.lower()).intersection(term2.lower()))) > 0

    def _distance_match(self, term1, term2):

        result = self._get_lev_ratio(term1, term2)

        return result >= self.lev_threshold

    def _get_lev_ratio(self, term1, term2):

        return Levenshtein.ratio(term1, term2) 
