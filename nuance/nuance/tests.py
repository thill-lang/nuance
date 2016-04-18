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
        # for now, only one synset should be returned
        # TODO: Add multi-synset capacity
        self.roach_blob.rank_original_synsets()
        self.assertEquals(1, len(self.roach_blob.source_synsets), "Ranking function not taking only top-ranked value")

    def test_populate_target_synsets(self):
        # target synsets should contain at least keys 'cafard', 'blatte', 'Blattaria', 'cancrelat', 'coquerelle'
        self.roach_blob.populate_target_synsets()
        self.assertIn('cafard', self.roach_blob.target_synsets, 'Key "cafard" missing from target synsets')
        self.assertIn('Blattaria', self.roach_blob.target_synsets, 'Key "Blattaria" missing from target synsets')
        self.assertIn('blatte', self.roach_blob.target_synsets, 'Key "blatte" missing from target synsets')
        self.assertIn('cancrelat', self.roach_blob.target_synsets, 'Key "cancrelat" missing from target synsets')
        self.assertIn('coquerelle', self.roach_blob.target_synsets, 'Key "coquerelle" missing from target synsets')

    def rank_translation_terms(self):
        # translation ranking should be in the order: 'Blattaria', 'cafard', 'blatte', 'cancrelat', 'coquerelle'
        # TODO: eventually we'll want 'cafard' to be ranked first
        pass

    def test_calculate_semantic_disjunct(self):
        # key 'cafard' with synset bn:00010814n
        # and WITHOUT synset bn:00020298n
        self.roach_blob.calculate_semantic_disjunct()
        self.assertIn('00010814n', self.roach_blob.target_synsets['cafard'], 'Key "cafard" does not have required additional sense')
        self.assertNotIn('00020298n', self.roach_blob.target_synsets['cafard'], 'Key "card" still has non-disjunct synsets included')
        pass

    def test_serialize_self_to_json(self):
        # check completeness plus is valid JSON
        # TODO: Start messing with this once we have some sample data
        pass

