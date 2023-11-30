import unittest
import os
import game_records


class TestGameRecords(unittest.TestCase):
    def setUp(self):
        self.records = game_records.GameStatistics("test_records")

    def tearDown(self):
        os.remove("test_records.bak")
        os.remove("test_records.dat")
        os.remove("test_records.dir")

    def testAddRecord(self):
        game_records.reset_statistics(self.records.file_name)
        self.records.save_record(0, "person")
        recs = dict(self.records.get_records())
        self.assertEqual(1, len(recs.keys()))
        self.assertIn("person", recs.keys())
        self.assertEqual(0, recs["person"])

    def testAddSeveralRecord(self):
        game_records.reset_statistics(self.records.file_name)
        self.records.save_record(0, "person1")
        self.records.save_record(120, "person2")
        recs = dict(self.records.get_records())
        self.assertEqual(2, len(recs.keys()))
        self.assertIn("person1", recs.keys())
        self.assertIn("person2", recs.keys())
        self.assertEqual(0, recs["person1"])
        self.assertEqual(120, recs["person2"])

    def testRewriteRecord(self):
        game_records.reset_statistics(self.records.file_name)
        self.records.save_record(0, "person1")
        self.records.save_record(120, "person1")
        recs = dict(self.records.get_records())
        self.assertEqual(1, len(recs.keys()))
        self.assertIn("person1", recs.keys())
        self.assertEqual(120, recs["person1"])

    def testRecordsSortedCorrectly(self):
        game_records.reset_statistics(self.records.file_name)
        self.records.save_record(0, "person1")
        self.records.save_record(120, "person2")
        recs = dict(self.records.get_records())
        self.assertEqual(2, len(recs.keys()))
        self.assertIn("person1", recs.keys())
        self.assertIn("person2", recs.keys())
        self.assertGreaterEqual(recs[list(recs.keys())[0]], recs[list(recs.keys())[1]])

    def testRecordsReset(self):
        game_records.reset_statistics(self.records.file_name)
        self.records.save_record(0, "person1")
        self.records.save_record(120, "person2")
        recs = dict(self.records.get_records())
        self.assertEqual(2, len(recs.keys()))
        self.assertIn("person1", recs.keys())
        self.assertIn("person2", recs.keys())
        game_records.reset_statistics(self.records.file_name)
        recs = self.records.get_records()
        self.assertEqual(0, len(recs))