import copy
import unittest
import yaml
from validate import ROOT, validate_document, UniqueLoader


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.document = yaml.safe_load((ROOT / "examples/minimal.yaml").read_text())

    def test_example(self):
        validate_document(self.document)

    def test_tencent_declares_verified_market_symbol_mappings(self):
        document = yaml.load((ROOT / "providers/tencent/config.yaml").read_text(), Loader=UniqueLoader)
        self.assertEqual(document["supported_markets"], ["CN", "HK", "US"])
        self.assertFalse(document["enabled"])
        self.assertEqual(document["symbol"]["output_template"], "{{exchange}}{{code}}")
        self.assertEqual(document["symbol"]["exchange_mapping"]["hk"], "hk")
        self.assertEqual(document["symbol"]["exchange_mapping"]["us"], "us")
        self.assertIn("00700.HK", document["metadata"]["verification_scope"])
        self.assertIn("AAPL.US", document["metadata"]["verification_scope"])
        validate_document(document)

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

    def test_allow_runtime_credential_placeholder(self):
        self.document["api"]["headers"] = {"X-api-key": "${HITHINK_FINANCE_API_KEY}"}
        validate_document(self.document)

    def test_reject_duplicate_keys(self):
        with self.assertRaises(ValueError):
            yaml.load("id: first\nid: second", Loader=UniqueLoader)


if __name__ == "__main__":
    unittest.main()
