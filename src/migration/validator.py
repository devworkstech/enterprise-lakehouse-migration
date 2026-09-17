"""
Reconciliation & Data Parity Validator.
"""
import hashlib
from typing import Dict, Any, List

class MigrationValidator:
    def __init__(self, tolerance_pct: float = 0.0):
        self.tolerance_pct = tolerance_pct

    def verify_row_counts(self, source_count: int, target_count: int) -> Dict[str, Any]:
        delta = abs(source_count - target_count)
        pct_diff = (delta / source_count * 100.0) if source_count > 0 else 0.0
        passed = pct_diff <= self.tolerance_pct
        return {
            "metric": "row_count_parity",
            "source_count": source_count,
            "target_count": target_count,
            "discrepancy": delta,
            "discrepancy_pct": round(pct_diff, 4),
            "passed": passed
        }

    def compute_sample_checksum(self, records: List[Dict[str, Any]], key_cols: List[str]) -> str:
        sorted_records = sorted(records, key=lambda r: tuple(str(r.get(k, "")) for k in key_cols))
        hasher = hashlib.sha256()
        for rec in sorted_records:
            row_str = "|".join(f"{k}:{rec.get(k)}" for k in sorted(rec.keys()))
            hasher.update(row_str.encode("utf-8"))
        return hasher.hexdigest()
