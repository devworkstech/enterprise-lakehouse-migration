from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'sonia-blake',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'enterprise_lakehouse_migration_pipeline',
    default_args=default_args,
    description='Automated migration & dbt transformation to AWS Databricks Lakehouse',
    schedule_interval='@daily',
    catchup=False,
) as dag:
    t1 = BashOperator(task_id='extract_to_bronze_s3', bash_command='python -m src.migration.data_extractor')
    t2 = BashOperator(task_id='run_dbt_models', bash_command='cd dbt_project && dbt run')
    t3 = BashOperator(task_id='test_dbt_data_contracts', bash_command='cd dbt_project && dbt test')
    t1 >> t2 >> t3
