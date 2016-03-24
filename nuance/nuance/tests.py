from django.test import TestCase
from views import SemanticBlob

class SemanticBlobTest(TestCase):

    def setUp(self):
        self.roach_blob = SemanticBlob("cockroach", "en", "fr")

    def test_get_original_synsets(self):
        # there should be at least three synsets for 'cockroach'
        synsets = self.roach_blob.get_original_synsets()
        self.assertGreaterEqual(3, len(synsets), "Insufficient synsets retrieved: " + str(len(synsets)))

    def test_rank_original_synsets(self):
        # concepts should rank before named entities
        # monosemous terms should rank before polysemous
        pass

    def test_populate_target_synsets(self):
        # target synsets should contain at least keys 'cafard', 'blatte', 'Blattaria', 'cancrelat', 'coquerelle'
        pass

    def rank_translation_terms(self):
        # translation ranking should be in the order: 'cafard', 'blatte', 'cancrelat', 'coquerelle', 'Blattaria'
        pass

    def test_calculate_semantic_disjunct(self):
        # key 'cafard' with synset bn:00010814n
        self.roach_blob.calculate_semantic_disjunct()
        pass

    def test_serialize_self_to_json(self):
        # check completeness plus is valid JSON
        pass

