"""
Automated DDL and Schema Translation Engine.
Converts legacy SQL Server / Oracle schemas into PySpark StructTypes and Delta Lake DDL.
"""

import re
from typing import Dict, List, Any, Optional


class SchemaConverter:
    """Translates legacy RDBMS DDL to Spark SQL / Delta Lake syntax."""

    TYPE_MAPPINGS = {
        "INT": "INT",
        "INTEGER": "INT",
        "BIGINT": "BIGINT",
        "SMALLINT": "SMALLINT",
        "TINYINT": "BYTE",
        "BIT": "BOOLEAN",
        "VARCHAR": "STRING",
        "NVARCHAR": "STRING",
        "VARCHAR2": "STRING",
        "CHAR": "STRING",
        "TEXT": "STRING",
        "CLOB": "STRING",
        "DECIMAL": "DECIMAL",
        "NUMERIC": "DECIMAL",
        "NUMBER": "DECIMAL",
        "MONEY": "DECIMAL(19,4)",
        "FLOAT": "DOUBLE",
        "REAL": "FLOAT",
        "DATETIME": "TIMESTAMP",
        "DATETIME2": "TIMESTAMP",
        "DATE": "DATE",
        "TIME": "STRING",
        "VARBINARY": "BINARY",
        "BLOB": "BINARY",
        "UNIQUEIDENTIFIER": "STRING",
    }

    def __init__(self, source_engine: str = "sqlserver"):
        self.source_engine = source_engine.lower()

    def map_data_type(self, data_type: str, precision: Optional[int] = None, scale: Optional[int] = None) -> str:
        clean_type = re.sub(r'\(.*\)', '', data_type).strip().upper()
        target_type = self.TYPE_MAPPINGS.get(clean_type, "STRING")

        if target_type == "DECIMAL" and precision is not None:
            if scale is not None:
                return f"DECIMAL({precision},{scale})"
            return f"DECIMAL({precision},0)"
        return target_type

    def convert_column_definition(self, col_name: str, raw_type: str, is_nullable: bool = True) -> Dict[str, Any]:
        delta_type = self.map_data_type(raw_type)
        return {
            "name": col_name.strip().lower(),
            "type": delta_type,
            "nullable": is_nullable
        }

    def generate_delta_ddl(self, table_name: str, columns: List[Dict[str, Any]], partition_col: Optional[str] = None) -> str:
        col_defs = []
        for col in columns:
            null_clause = "" if col.get("nullable", True) else " NOT NULL"
            col_defs.append(f"  {col['name']} {col['type']}{null_clause}")

        ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n" + ",\n".join(col_defs) + "\n) USING DELTA"

        if partition_col:
            ddl += f"\nPARTITIONED BY ({partition_col})"

        ddl += "\nTBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true', 'delta.autoOptimize.autoCompact' = 'true');"
        return ddl
