param([string]$Username = "soniablake")
git init; git branch -M main; git add .
git commit -m "feat: Enterprise Multi-Cloud Lakehouse Migration Platform - AWS S3, Databricks Delta Lake, dbt Core, Airflow, and Terraform IaC"
git remote remove origin 2>$null
git remote add origin "https://github.com/$Username/enterprise-lakehouse-migration.git"
git push -u origin main
