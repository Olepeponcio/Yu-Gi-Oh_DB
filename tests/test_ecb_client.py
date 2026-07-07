from decimal import Decimal
import unittest

from src.api.ecb_client import parse_eur_usd_csv


class EcbClientTest(unittest.TestCase):
    def test_parse_eur_usd_csv_returns_exchange_rate(self):
        raw_csv = (
            "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE\n"
            "EXR.D.USD.EUR.SP00.A,D,USD,EUR,SP00,A,2026-07-07,1.1433\n"
        )

        exchange_rate = parse_eur_usd_csv(raw_csv)

        self.assertEqual(exchange_rate.source, "ECB Data Portal")
        self.assertEqual(exchange_rate.base_currency, "EUR")
        self.assertEqual(exchange_rate.quote_currency, "USD")
        self.assertEqual(exchange_rate.rate, Decimal("1.1433"))
        self.assertEqual(exchange_rate.observed_at, "2026-07-07")

    def test_parse_eur_usd_csv_rejects_unexpected_series(self):
        raw_csv = (
            "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE\n"
            "EXR.D.GBP.EUR.SP00.A,D,GBP,EUR,SP00,A,2026-07-07,0.87\n"
        )

        with self.assertRaisesRegex(ValueError, "EUR/USD"):
            parse_eur_usd_csv(raw_csv)


if __name__ == "__main__":
    unittest.main()
