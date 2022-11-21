from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime

with DAG(
    "project1-workflow",
    start_date=datetime(2015, 12, 1),
    schedule_interval=None,
    # TODO Uruchamiając projekt, za każdym razem w konfiguracji uruchomienia Apache Airflow popraw ścieżki w parametrach dags_home i input_dir
    # TODO Zmień poniżej domyślne wartości parametrów classic_or_streaming oraz pig_or_hive na zgodne z Twoim projektem
    params={
      "dags_home": Param("/home/michal_r_kwarta/airflow/dags", type="string"),
      "input_dir": Param("gs://michal-r-kwarta-bucket/projekt1/input", type="string"),
      "output_mr_dir": Param("/project1/output_mr3", type="string"),
      "output_dir": Param("/project1/output6", type="string"),
      "classic_or_streaming": Param("streaming", enum=["classic", "streaming"]),
      "pig_or_hive": Param("hive", enum=["hive", "pig"]),
    },
    render_template_as_native_obj=True
) as dag:
  clean_output_mr_dir = BashOperator(
    task_id="clean_output_mr_dir",
    bash_command="""if $(hadoop fs -test -d {{ params.output_mr_dir }}) ; then hadoop fs -rm -f -r {{ params.output_mr_dir }}; fi""",
  )
  clean_output_dir = BashOperator(
    task_id="clean_output_dir",
    bash_command="""if $(hadoop fs -test -d {{ params.output_dir }}) ; then hadoop fs -rm -f -r {{ params.output_dir }}; fi""",
  )


  hadoop_streaming = BashOperator(
    task_id="hadoop_streaming",
    bash_command="""mapred streaming \
-files {{ params.dags_home }}/project_files/mapper.py,\
{{ params.dags_home }}/project_files/combiner.py,\
{{ params.dags_home }}/project_files/reducer.py \
-input {{ params.input_dir }}/datasource1 \
-mapper  mapper.py \
-combiner combiner.py \
-reducer reducer.py \
-output {{ params.output_mr_dir }}""",
  )





  # TODO Jeśli w Twoim projekcie wykorzystywany jest Hive, zmień poniższe polecenia dostosowując sposób uruchamiania skryptu Hive
  hive = BashOperator(
    task_id="hive",
    bash_command="""hive -f {{ params.dags_home }}/project_files/transform5.hql \
      -hiveconf input_dir4={{ params.input_dir }}/datasource4 \
      -hiveconf input_dir3={{ params.output_mr_dir }} \
      -hiveconf output_dir6={{ params.output_dir }}""",
  )



  get_output = BashOperator(
    task_id="get_output",
    bash_command="""hadoop fs -getmerge {{ params.output_dir }} output6.json; cat output6.json""",
    trigger_rule="none_failed",
  )

  [clean_output_mr_dir, clean_output_dir] >> hadoop_streaming
  hadoop_streaming >> hive
  hive >> get_output
  