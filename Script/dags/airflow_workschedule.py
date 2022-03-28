try:
    import airflow
    from airflow import DAG
    from airflow.operators.bash_operator import BashOperator
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime, timedelta
    from create_database import scrape_tweets

    def fetchtweets():
        return None

    def cleantweets():
        return None

    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': airflow.utils.dates.days_ago(2),#start from 3 months ago
        'email': ['airflow@example.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'end_date': datetime(2016, 1, 1),
    }

    # run daily at 6am
    schedule_interval = "00 06 * * *"

    dag = DAG(
        dag_id='airflow_workschedule', 
        default_args=default_args, 
        schedule_interval=schedule_interval
    )

    # fetch_tweets = PythonOperator(
    #     task_id='fetch_tweets',
    #     python_callable=fetchtweets,
    #     dag=dag)

    # clean_tweets = PythonOperator(
    #     task_id='clean_tweets',
    #     python_callable=cleantweets,
    #     dag=dag)

    # clean_tweets.set_upstream(fetch_tweets)

    t1=PythonOperator(
        task_id='scrape_tweets_and_save_db',
        python_callable= scrape_tweets,
        op_kwargs = {"keywords":"[PeacockTV]","database": "tweets.db", "start_date":"None", "end_date":"datetime.now().date()", "num_tweet":"1000"},
        dag = dag

    )

    t2 = BashOperator(
        task_id='topic_modeling',
        bash_command='python3 BERTopic_modeling.py',
        retries=1,
        dag=dag)



    t1.set_downstream(t2)

except Exception as e:
    print('Error:{}'.format(e))

