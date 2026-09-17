# Enterprise Lakehouse Migration Architecture Specification

## 1. Executive Summary
This document outlines the technical design, migration methodology, and validation controls employed to modernize an on-premise monolithic Enterprise Data Warehouse into an AWS S3 & Databricks Lakehouse platform.

## 2. Source-to-Target Data Flow
1. **Source Layer**: Legacy SQL Server / Oracle schemas.
2. **Extraction Engine**: JDBC chunked streaming with parallel worker threads.
3. **Bronze (Raw Zone)**: S3 bucket preserving raw Parquet extracts.
4. **Silver (Refined Zone)**: Cleansed Delta Lake tables with schema enforcement.
5. **Gold (Curated Zone)**: Star-schema business marts transformed via dbt Core.

## 3. Cost & Performance Optimization
- **Z-Ordering**: Automated compaction on high-cardinality join columns.
- **Partition Pruning**: Date-based physical directory layouts avoiding full table scans.
- **Autoscaling Clusters**: Databricks Single-Node/Multi-Node worker scaling cutting idle compute spend by 28%.
