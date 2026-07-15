import unittest

from src.data.mock_data import capacity_detail, demand_mix, scenarios, weekly_demand


class MockDataTests(unittest.TestCase):
    def test_weekly_demand_has_eight_weeks(self):
        data = weekly_demand()
        self.assertEqual(len(data), 8)
        self.assertTrue((data["Forecast final"] >= data["Baseline"]).all())

    def test_b2c_share_is_valid_and_increases(self):
        data = demand_mix()
        self.assertTrue(data["Share B2C"].between(0, 1).all())
        self.assertGreater(data["Share B2C"].iloc[-1], data["Share B2C"].iloc[0])

    def test_capacity_status_matches_occupancy(self):
        data = capacity_detail()
        critical = data[data["Ocupação"] > 1.05]
        self.assertTrue((critical["Status"] == "Crítico").all())

    def test_standard_scenarios_are_available(self):
        self.assertEqual(scenarios()["Cenário"].tolist(), ["Conservador", "Base", "Agressivo"])


if __name__ == "__main__":
    unittest.main()
