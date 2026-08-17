import unittest

import main


class TypeChartTests(unittest.TestCase):
    def test_modern_type_chart_contains_all_types(self):
        self.assertEqual(18, len(main.TYPES))
        self.assertIn("Fairy", main.TYPES)
        self.assertEqual(set(main.TYPES), set(main.TYPE_CHART))

    def test_known_effectiveness_values(self):
        self.assertEqual(2.0, main.get_type_multiplier("Fairy", "Dragon"))
        self.assertEqual(0.0, main.get_type_multiplier("Dragon", "Fairy"))
        self.assertEqual(0.0, main.get_type_multiplier("Electric", "Ground"))
        self.assertEqual(1.0, main.get_type_multiplier("Normal", "Water"))

    def test_dual_type_defense_multiplies_both_types(self):
        profile = main.calculate_defensive_profile(["Grass", "Steel"])

        self.assertEqual(4.0, profile["Fire"])
        self.assertEqual(0.25, profile["Grass"])
        self.assertEqual(0.0, profile["Poison"])

    def test_best_coverage_uses_strongest_selected_attack(self):
        coverage = main.calculate_best_coverage(["Fire", "Water"])

        self.assertEqual(2.0, coverage["Grass"])
        self.assertEqual(2.0, coverage["Rock"])
        self.assertEqual(2.0, coverage["Fire"])
        self.assertEqual(0.5, coverage["Dragon"])

    def test_selected_types_are_valid_and_unique(self):
        self.assertEqual(
            ["Fire", "Water"],
            main.normalize_selected_types(["Fire", "Water", "Fire", "Unknown"]),
        )

    def test_bucketization_accounts_for_every_type(self):
        buckets = main.bucketize_matchups(
            main.calculate_defensive_profile(["Normal", "Ghost"])
        )

        self.assertEqual(len(main.TYPES), sum(map(len, buckets.values())))
        self.assertIn("Ghost", buckets["immune"])
        self.assertIn("Fighting", buckets["immune"])


if __name__ == "__main__":
    unittest.main()
