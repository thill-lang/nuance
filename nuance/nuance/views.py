from .key import BN_KEY
from django.shortcuts import render

def render_query_form(request):
    """
    Presents search box with text input, language dropdowns
    for language of entry, translation language
    :return: null
    """
    return render(request, 'nuance/index.html')

def retrieve_semantic_blob(request):
    """
    Parses the request object for the original term and its language
    and returns a list of possible translations in the target language,
    along with meanings that do not coincide with the original term
    :param request:
    :return:
    """
    pass

def feedback(request):
    """
    Provides a feedback form regarding the quality or otherwise of
    the translations
    :param request:
    :return:
    """
    # TODO: set up postgres backend
    pass



class SemanticBlob:

    def __init__(self, source_term, source_language, target_language):
        self.source_term = source_term
        self.source_language = source_language
        self.target_language = target_language
        self.source_synsets = [] # populated by BabelNet synsets
        self.target_synsets = {}   # keys are headwords, values are BN synsets

    def get_original_synsets(self):
        """
        Gets all synsets of which self.source_term (in self.source_language) is a member
        :return:
        """
        pass

    def rank_original_synsets(self):
        """
        Ranks synsets from most to least likely meanings
        :return:
        """
        # TODO: for the moment we just grab the first non-named-entity
        # multiple synsets can come later
        pass

    def populate_target_synsets(self):
        """
        Populates self.target_synsets with keys=translation term and values = synsets for these terms
        :return:
        """
        # TODO: filter out automatic translations
        # TODO:
        pass

    def rank_translation_terms(self):
        """
        Ranks translation terms from most likely translation to least
        :return:
        """
        pass

    def calculate_semantic_disjunct(self):
        """
        Removes the intersection between source synsets and target synsets
        :return:
        """
        pass

    def serialize_self_to_json(self):
        pass

