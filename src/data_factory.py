from __future__ import annotations

import csv
import json
from pathlib import Path
from random import Random
from typing import Dict, List


PUBLIC_DATASET_REFERENCE = {
    "primary_reference": {
        "name": "NYC TLC Trip Record Data",
        "url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        "role": "Public trip marketplace data with fare, time, and tip behavior fields used here only as a behavioral reference for gratuity and operational signals.",
    },
    "project_note": {
        "name": "Synthetic delivery checkout experiment",
        "url": "local_runtime_only",
        "role": "The runtime dataset in this repository is synthetic because production-grade food delivery tipping experiments are not typically public.",
    },
    "notes": [
        "This project simulates an A/B test for a new tipping nudge shown during checkout.",
        "The data is intended for product experimentation practice, not for business forecasting in a real marketplace.",
    ],
}


REGIONS = ["north", "south", "east", "west"]
SEGMENTS = ["new_user", "casual", "power_user"]
DEVICES = ["ios", "android", "web"]


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_sample_dataset(base_dir: Path, row_count: int = 1200) -> Dict[str, str]:
    rng = Random(42)
    rows: List[Dict[str, object]] = []

    for index in range(row_count):
        region = REGIONS[index % len(REGIONS)]
        user_segment = SEGMENTS[index % len(SEGMENTS)]
        device = DEVICES[index % len(DEVICES)]
        variant = "control" if ((index * 7) % 10) < 5 else "treatment"
        peak_hour = 1 if index % 5 in (0, 1) else 0
        rainy = 1 if index % 7 == 0 else 0

        base_subtotal = 18 + (index % 9) * 3.2 + rng.uniform(-1.2, 2.0)
        subtotal = round(max(10.0, base_subtotal), 2)
        basket_size = 1 + (index % 4)
        delivery_fee = round(2.49 + (0.35 * peak_hour) + rng.uniform(0.0, 1.1), 2)

        conversion_prob = 0.60
        if user_segment == "power_user":
            conversion_prob += 0.08
        elif user_segment == "new_user":
            conversion_prob -= 0.04
        if device == "web":
            conversion_prob -= 0.03
        if rainy:
            conversion_prob += 0.02
        if variant == "treatment":
            conversion_prob -= 0.005
        conversion_prob = _clamp(conversion_prob, 0.35, 0.9)

        converted_order = 1 if rng.random() < conversion_prob else 0

        tip_rate = 0.58
        if user_segment == "power_user":
            tip_rate += 0.07
        if peak_hour:
            tip_rate += 0.03
        if variant == "treatment":
            tip_rate += 0.06
        tip_rate = _clamp(tip_rate, 0.35, 0.92)

        tipped = 1 if converted_order and rng.random() < tip_rate else 0
        base_tip_pct = 0.11 + (0.008 * basket_size) + (0.01 if variant == "treatment" else 0.0)
        tip_pct = round(_clamp(base_tip_pct + rng.uniform(-0.025, 0.03), 0.0, 0.28), 4) if tipped else 0.0
        tip_amount = round(subtotal * tip_pct, 2) if tipped else 0.0

        dasher_acceptance_prob = 0.73
        if tipped:
            dasher_acceptance_prob += 0.07
        if peak_hour:
            dasher_acceptance_prob -= 0.04
        if rainy:
            dasher_acceptance_prob -= 0.03
        dasher_acceptance_prob = _clamp(dasher_acceptance_prob, 0.45, 0.96)
        driver_accepted = 1 if converted_order and rng.random() < dasher_acceptance_prob else 0

        rows.append(
            {
                "session_id": f"TIP-{index + 1:05d}",
                "user_id": f"USR-{(index % 360) + 1:04d}",
                "region": region,
                "user_segment": user_segment,
                "device": device,
                "variant": variant,
                "peak_hour": peak_hour,
                "rainy_weather": rainy,
                "basket_size": basket_size,
                "order_subtotal": subtotal,
                "delivery_fee": delivery_fee,
                "checkout_started": 1,
                "converted_order": converted_order,
                "tipped": tipped,
                "tip_pct": tip_pct,
                "tip_amount": tip_amount,
                "driver_accepted": driver_accepted,
            }
        )

    raw_dir = base_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = raw_dir / "checkout_sessions.csv"
    reference_path = raw_dir / "public_dataset_reference.json"
    _write_csv(dataset_path, rows)
    reference_path.write_text(json.dumps(PUBLIC_DATASET_REFERENCE, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "dataset_source": "synthetic_delivery_tipping_experiment",
        "dataset_path": str(dataset_path),
        "dataset_reference_path": str(reference_path),
    }
