from .key import BN_KEY
from django.shortcuts import render
from django import forms
import requests
import json
from django.http import JsonResponse

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
    sb = SemanticBlob(term, start_lang, trans_lang)
    sb.wake_up()
    print('!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        print(str(json.dumps(sb.source_synsets.__dict__)))
    except Exception as e:
        print("exception is " + str(e))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return sb.source_synsets

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

    SYNSETS = "https://babelnet.io/v3/getSynsetIds?key=" + BN_KEY
    SENSES = "https://babelnet.io/v3/getSenses?key=" + BN_KEY
    RECORDS = "https://babelnet.io/v3/getSynset?key=" + BN_KEY

    def __init__(self, source_term, source_language, target_language):
        from collections import OrderedDict
        self.source_term = source_term
        self.source_language = source_language
        self.translation_language = target_language
        self.source_synsets = OrderedDict() # populated by BabelNet synsets

    def wake_up(self):
        # we want loading to be lazy - that is to say
        # synsets aren't populated until explicitly triggered
        # this is the trigger method
        qry = SemanticBlob.SYNSETS + "&word=" + self.source_term + "&langs=" + self.source_language + "&filterLangs=" + self.source_language + "&filterLangs=" + self.translation_language
        synsets = requests.get(qry)
        ids = [synset['id'] for synset in synsets.json()]
        self.build_original_synsets(ids)

    def build_original_synsets(self, id_list):
        """
        Gets all synsets of which self.source_term (in self.source_language) is a member
        :return:
        """
        raw_synsets = {}
        for id in id_list:
            synqry = SemanticBlob.RECORDS + "&id=" + id + "&filterLangs=" + self.source_language + "&filterLangs=" + self.translation_language
            record = requests.get(synqry)
            raw_synsets[id] = record.json()
        self.rank_original_synsets(raw_synsets)
        self.filter_original_synsets()
        self.build_dictionary_entries()

    def rank_original_synsets(self, raw_synsets):
        """
        Ranks synsets from most to least likely meanings
        :return:
        """
        named_entities = []
        everything = []
        # we want named entities to come last
        for id in raw_synsets:
            record = raw_synsets[id]
            entity_type = record['synsetType']
            named_entities.append(id) if entity_type == 'NAMED_ENTITY' else everything.append(id)
        everything.extend(named_entities)
        for e in everything:
            self.source_synsets[e] = raw_synsets[e]
            # at this point we have the original lemmata in the correct order, though w/o synset data formatted
            # in the right way

    def filter_original_synsets(self):
        # TODO: the data is very dirty - we're going to want to filter
        # based on source, automatic translation, etc.\
        pass

    def build_dictionary_entries(self):
        # creates the entries for each synset
        temp_hash = {}
        for id in self.source_synsets:
            synset = self.source_synsets[id]
            headword = synset['mainSense']
            # we're just grabbing the first entry in the appropriate language
            defn = ""
            for item in synset['glosses']:
                if(item['language'] == self.source_language):
                    defn = item['gloss']
                    break
            translations = self.build_ordered_list_of_translations(synset)
            de = DictionaryEntry(id, headword, defn, translations)
            temp_hash[id] = de
        for key in self.source_synsets.keys():
            self.source_synsets[key] = temp_hash[key]

    def build_ordered_list_of_translations(self, record):
        trans_temp = []
        if('lnToOtherForm' in record.keys() and self.translation_language in record['lnToOtherForm'].keys()):
            for trans_term in record['lnToOtherForm'][self.translation_language]:
                trans_temp.append(trans_term)
        for trans_sense in record['senses']:
            if(trans_sense['language'] == self.translation_language):
                translation = trans_sense['simpleLemma']
                if(translation not in trans_temp):
                    trans_temp.append(translation)
        return trans_temp

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

    def __init__(self, synset_id, headword, gloss, translations):
        from collections import OrderedDict
        self.synset_id = synset_id
        self.headword = ""
        self.definition = ""
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