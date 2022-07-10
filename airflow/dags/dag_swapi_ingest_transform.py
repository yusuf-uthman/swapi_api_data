from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="swapi_ingest_transform_dag",
    description='An Airflow DAG to invoke a python script and commands',
    schedule_interval="10 * * * *",
    start_date=datetime(2022, 3, 19),
    default_args=default_args,
    max_active_runs=1,
    catchup=False,
    tags=['swapi_api_DE_practice_test'],
) as dag:

    api_data_ingest_to_db = BashOperator(
        task_id='api_data_ingest_to_db',
        bash_command='cd /pipeline && python pipeline.py',
        dag=dag
    )

    dbt_trasformations = BashOperator(
        task_id='dbt_trasformations',
        bash_command= 'cd /swapi_dbt && dbt run  --profiles-dir .' ,
        dag=dag
    )
    # dag execution order
    api_data_ingest_to_db >> dbt_trasformations # Define dependenciesversion