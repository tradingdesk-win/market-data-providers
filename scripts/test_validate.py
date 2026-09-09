import copy
import unittest
import yaml
from validate import ROOT, validate_document, UniqueLoader


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.document = yaml.safe_load((ROOT / "examples/minimal.yaml").read_text())

    def test_example(self):
        validate_document(self.document)

    def test_reject_invalid_documents(self):
        for key, value in (("id", "../escape"), ("enabled", True), ("supported_markets", ["UNKNOWN"])):
            with self.subTest(key=key), self.assertRaises(Exception):
                document = copy.deepcopy(self.document)
                document[key] = value
                validate_document(document)

    def test_reject_credentials(self):
        self.document["api"]["headers"] = {"Authorization": "Bearer secret"}
        with self.assertRaises(ValueError):
            validate_document(self.document)

    def test_reject_duplicate_keys(self):
        with self.assertRaises(ValueError):
            yaml.load("id: first\nid: second", Loader=UniqueLoader)


if __name__ == "__main__":
    unittest.main()
