from __future__ import annotations

import json
from pathlib import Path

from src.modeling import run_analysis


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    result = run_analysis(base_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
