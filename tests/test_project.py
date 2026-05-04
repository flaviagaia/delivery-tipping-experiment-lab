from __future__ import annotations

import unittest
from pathlib import Path

from src.data_factory import build_sample_dataset
from src.modeling import run_analysis


class DeliveryTippingExperimentLabTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]

    def test_dataset_factory_creates_files(self) -> None:
        dataset_info = build_sample_dataset(self.base_dir)
        self.assertEqual(dataset_info["dataset_source"], "synthetic_delivery_tipping_experiment")
        self.assertTrue(Path(dataset_info["dataset_path"]).exists())
        self.assertTrue(Path(dataset_info["dataset_reference_path"]).exists())

    def test_analysis_contract(self) -> None:
        report = run_analysis(self.base_dir)
        self.assertEqual(report["dataset_source"], "synthetic_delivery_tipping_experiment")
        self.assertEqual(report["session_count"], 1200)
        self.assertEqual(report["variant_counts"]["control"], 600)
        self.assertEqual(report["variant_counts"]["treatment"], 600)
        self.assertIn("primary_metric_gross_tip_per_session", report["metrics"])
        self.assertIn("guardrail_checkout_conversion_rate", report["metrics"])
        self.assertIn(report["recommendation"]["decision"], {"ship_treatment", "needs_iteration"})
        self.assertTrue(Path(report["report_artifact"]).exists())

    def test_primary_metric_is_positive_for_treatment(self) -> None:
        report = run_analysis(self.base_dir)
        primary = report["metrics"]["primary_metric_gross_tip_per_session"]
        self.assertGreater(primary["absolute_lift"], 0.0)
        self.assertGreater(primary["treatment"], primary["control"])


if __name__ == "__main__":
    unittest.main()
