import copy
import unittest
import yaml
from validate import ROOT, validate_document, UniqueLoader


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.document = yaml.safe_load((ROOT / "examples/minimal.yaml").read_text())

    def test_example(self):
        validate_document(self.document)

    def test_binance_spot_includes_backwards_paginated_klines(self):
        document = yaml.load((ROOT / "providers/binance/config.yaml").read_text(), Loader=UniqueLoader)
        kline = document["api"]["kline"]
        self.assertEqual(kline["endpoint"], "/api/v3/klines")
        self.assertEqual(kline["date_format"], "unix_ms")
        self.assertEqual(kline["price_basis"], "RAW")
        self.assertEqual(kline["params"]["endTime"], "{{endDate}}")
        # startTime selects the oldest page on Binance, defeating backwards paging.
        self.assertNotIn("startTime", kline["params"])
        self.assertEqual(document["response"]["kline"]["field_mapping"]["timestamp"]["index"], 0)
        self.assertEqual(document["response"]["kline"]["field_mapping"]["close_px"]["index"], 4)
        for period in ("1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1w", "1M"):
            self.assertEqual(document["period_mapping"][period], period)
            self.assertIn(period, document["limits"]["supported_periods"])
        self.assertEqual(document["metadata"]["test_symbol"], "BTC-USDT")
        self.assertFalse(document["enabled"])
        validate_document(document)

    def test_binance_stream_contract(self):
        document = yaml.safe_load((ROOT / 'providers/binance/config.yaml').read_text())
        self.assertEqual(document['version'], '1.2.0')
        validate_document(document)
        for mutation in ('no_parser', 'no_symbol', 'insecure', 'credentials', 'bad_type'):
            bad = copy.deepcopy(document)
            if mutation == 'no_parser': del bad['response']['kline_stream']
            elif mutation == 'no_symbol': del bad['response']['kline_stream']['symbol_field']
            elif mutation == 'insecure': bad['api']['kline_stream']['url'] = 'ws://example.com/ws'
            elif mutation == 'credentials': bad['api']['kline_stream']['url'] = 'wss://user:pass@example.com/ws'
            else: bad['response']['kline_stream']['field_mapping']['close_px']['type'] = 'int'
            with self.subTest(mutation=mutation), self.assertRaises(Exception):
                validate_document(bad)

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

    def test_tushare_cross_market_configs_use_dedicated_endpoints(self):
        cases = {
            "tushare-hk": ("HK", "hk_daily", "00001.HK"),
            "tushare-us": ("US", "us_daily", "AAPL"),
        }
        for provider, (market, api_name, symbol) in cases.items():
            with self.subTest(provider=provider):
                document = yaml.load((ROOT / f"providers/{provider}/config.yaml").read_text(), Loader=UniqueLoader)
                self.assertEqual(document["supported_markets"], [market])
                self.assertFalse(document["enabled"])
                self.assertEqual(document["api"]["kline"]["params"]["api_name"], api_name)
                self.assertEqual(document["metadata"]["test_symbol"], symbol)
                validate_document(document)

    def test_sina_keeps_hk_us_out_of_supported_markets_after_probe(self):
        document = yaml.load((ROOT / "providers/sina/config.yaml").read_text(), Loader=UniqueLoader)
        self.assertEqual(document["supported_markets"], ["CN"])
        self.assertEqual(document["metadata"]["unsupported_market_probes"], {"HK": "hk00700", "US": "gb_aapl"})
        validate_document(document)

    def test_sina_cross_market_configs_are_realtime_only(self):
        for provider, market, symbol, prefix in (("sina-hk", "HK", "00700.HK", "rt_hk"), ("sina-us", "US", "AAPL.US", "gb_")):
            with self.subTest(provider=provider):
                document = yaml.load((ROOT / f"providers/{provider}/config.yaml").read_text(), Loader=UniqueLoader)
                self.assertEqual(document["supported_markets"], [market])
                self.assertFalse(document["enabled"])
                self.assertEqual(document["limits"]["supported_periods"], [])
                self.assertEqual(document["metadata"]["test_symbol"], symbol)
                self.assertTrue(document["symbol"]["output_template"].startswith(prefix))
                for capability in ("realtime", "batch_realtime"):
                    parser = document["response"][capability]
                    self.assertNotIn("field_mapping", parser["text_parse"])
                    self.assertTrue(parser["field_mapping"])
                    if market == "HK":
                        self.assertEqual(parser["field_mapping"]["last_px"]["index"], 6)
                        self.assertEqual(parser["field_mapping"]["prod_name"]["index"], 1)
                    else:
                        self.assertEqual(document["symbol"]["output_template"], "gb_{{code_lower}}")
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
