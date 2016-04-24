from .key import BN_KEY
from django.shortcuts import render
from django import forms
import requests
from django.http import JsonResponse

SYNSETS = "https://babelnet.io/v3/getSynsetIds?key=" + BN_KEY
# word={word}&langs={lang}&key={key}"

def render_query_form(request):
    """
    Presents search box with text input, language dropdowns
    for language of entry, translation language
    :return: null
    """
    return render(request, 'nuance/index.html', {'form':SearchForm()})

def retrieve_semantic_blob(search_obj):
    """
    Parses the request object for the original term and its language
    and returns a list of possible translations in the target language,
    along with meanings that do not coincide with the original term
    :param request:
    :return:
    """
    # TODO: Validate input
    term = search_obj.GET['term']
    start_lang = search_obj.GET['start_lang'].upper()
    trans_lang = search_obj.GET['trans_lang'].upper()
    qry = SYNSETS + "&word=" + term + "&langs=" + start_lang + "&filterLangs=" + start_lang + "&filterLangs=" + trans_lang
    synsets = requests.get(qry)
    print(synsets.json())
    return JsonResponse(synsets.json(), safe=False)

def feedback(request):
    """
    Provides a feedback form regarding the quality or otherwise of
    the translations
    :param request:
    :return:
    """
    # TODO: set up postgres backend
    pass

# basic form for entry
# TODO: create db backend for languages

class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

    startlangs = [('', '------------'), ('de', 'German'), ('it', 'Italian'), ('fr', 'French'), ('en', 'English'), ('es', 'Spanish')]
    translangs = [('', '------------'), ('de', 'German'), ('it', 'Italian'), ('fr', 'French'), ('en', 'English'), ('es', 'Spanish')]
    stcontrol = forms.ChoiceField(label="Original Language", choices=startlangs, widget=forms.Select(attrs={ 'id' : 'startlang-selector'}), initial='')
    test_query = forms.CharField(label="Term", max_length=60)
    trcontrol = forms.ChoiceField(label="Translation Language", choices=translangs, widget=forms.Select(attrs={ 'id' : 'translang-selector'}), initial='')


# The core data structures. The general picture is:
# user input (the search term) generates a list of synsets.
# These are stored as an OrderedDictionary for which
#   1. Keys are the synset IDs
#   2. Values are DictionaryEntry objects (see below)
# These DictionaryEntry objects have a number of display attributes
# of their own, and also an OrderedDictionary of Translations for which
#   1. Keys are headwords (the translated term)
#   2. Values are SemanticBlob objects

class SemanticBlob:

    def __init__(self, source_term, source_language, target_language):
        from collections import OrderedDict
        self.source_term = source_term
        self.source_language = source_language
        self.target_language = target_language
        self.source_synsets = OrderedDict() # populated by BabelNet synsets

    def wake_up(self):
        # we want loading to be lazy - that is to say
        # synsets aren't populated until explicitly triggered
        # this is the trigger method
        pass

    def build_original_synsets(self):
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
        # TODO: for the moment we just use BabelNet ranking
        # multiple synsets can come later
        pass

    def filter_original_synsets(self):
        # the data is very dirty - we're going to want to filter
        # based on source, automatic translation, etc.
        pass

    def rank_original_synsets(self):
        # the data is very dirty - we're going to want to filter
        # based on source, automatic translation, etc.
        pass


    def populate_target_synsets(self):
        """
        Populates self.target_synsets with keys=translation term and values = synsets for these terms
        :return:
        """
        # TODO: filter out automatic translations
        pass

    def rank_translation_terms(self):
        """
        Ranks translation terms from most likely translation to least
        :return:
        """
        # TODO: for now we just use BabelNet ranking
        pass

    def calculate_semantic_disjunct(self):
        """
        Removes the intersection between source synsets and target synsets
        :return:
        """
        pass

    def serialize_self_to_json(self):
        pass

class DictionaryEntry:

    def __init__(self, synset_id, headword):
        from collections import OrderedDict
        self.definition = ""
        self.image = ""
        self.synset_id = synset_id
        self.headword = ""
        self.translations = OrderedDict()

    def populate_translations(self):
        pass

    def filter_translations(self):
        pass

class Translation:

    def __init__(self, headword, language):
        self.headword = headword
        self.language = language
        self.synsets = []   # contains SemanticBlob objects

    def fetch_synsets(self):
        # gets synsets from headword
        pass