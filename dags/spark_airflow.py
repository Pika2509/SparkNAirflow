import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG(
    dag_id="sparknairflow",
    default_args={
        "owner": "Airflow",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    schedule_interval="@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)

python_job = SparkSubmitOperator(
    task_id="python_job",
    conn_id="spark-conn",  # Use the connection created in Airflow UI
    application="/opt/airflow/jobs/word_count_job.py",
    name="airflow-word-count",
    conf={
        "spark.sql.adaptive.enabled": "false",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
    },
    verbose=True,
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> python_job >> end