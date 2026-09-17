import pytest
from src.migration.schema_converter import SchemaConverter
from src.migration.data_extractor import ParallelDataExtractor
from src.migration.validator import MigrationValidator

def test_schema_converter():
    conv = SchemaConverter()
    assert conv.map_data_type("VARCHAR(100)") == "STRING"
    assert conv.map_data_type("DATETIME2") == "TIMESTAMP"
    ddl = conv.generate_delta_ddl("t1", [{"name": "id", "type": "INT", "nullable": False}])
    assert "USING DELTA" in ddl

def test_extractor_partitions():
    ext = ParallelDataExtractor("dummy_url", max_workers=2)
    ranges = ext.calculate_partition_ranges(1, 100, 2)
    assert len(ranges) == 2
    assert ranges[0]["start_id"] == 1
    assert ranges[1]["end_id"] == 100

def test_validator():
    val = MigrationValidator()
    assert val.verify_row_counts(500, 500)["passed"] is True
    assert val.verify_row_counts(500, 499)["passed"] is False
