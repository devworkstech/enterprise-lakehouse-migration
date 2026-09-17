@echo off
setlocal
echo ===================================================
echo  Enterprise Multi-Cloud Lakehouse Migration
echo ===================================================
git init
git branch -M main
git add .
git commit -m "feat: Enterprise Multi-Cloud Lakehouse Migration Platform - AWS S3, Databricks Delta Lake, dbt Core, Airflow, and Terraform IaC"
set /p GH_USER="Enter GitHub username (or press enter for soniablake): "
if "%GH_USER%"=="" set GH_USER=soniablake
git remote remove origin 2>nul
git remote add origin https://github.com/%GH_USER%/enterprise-lakehouse-migration.git
git push -u origin main
pause
