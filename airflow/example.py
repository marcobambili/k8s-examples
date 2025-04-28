import os
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Percorso per salvare il file di output
desktop_path = os.path.expanduser("~/Desktop/output.txt")  # Mac/Linux
# desktop_path = "C:\\Users\\TuoNomeUtente\\Desktop\\output.txt"  # Windows (cambia "TuoNomeUtente")

# Funzione per recuperare il TODO
def fetch_todo():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Funzione per recuperare la lista di utenti
def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Funzione per unire i dati e salvare l'output in un file
def match_user(**kwargs):
    ti = kwargs["ti"]
    
    todo = ti.xcom_pull(task_ids="fetch_todo_task")  # Prende il TODO
    users = ti.xcom_pull(task_ids="fetch_users_task")  # Prende la lista utenti
    
    user_id = todo["userId"]
    user_name = next((user["name"] for user in users if user["id"] == user_id), "Utente non trovato")

    output_text = f"L'utente corrispondente a userId={user_id} è: {user_name}\n"
    
    # Scrive l'output nel file
    with open(desktop_path, "a") as file:
        file.write(output_text)
    
    print(output_text)  # Mostra anche l'output nei log di Airflow
    return user_name

# Definizione del DAG
with DAG(
    dag_id="airflow_api_join",
    schedule_interval="*/5 * * * *",  # Esegui ogni 5 minuti
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    task_fetch_todo = PythonOperator(
        task_id="fetch_todo_task",
        python_callable=fetch_todo
    )

    task_fetch_users = PythonOperator(
        task_id="fetch_users_task",
        python_callable=fetch_users
    )

    task_match_user = PythonOperator(
        task_id="match_user_task",
        python_callable=match_user,
        provide_context=True
    )

    # Definizione del flusso
    [task_fetch_todo, task_fetch_users] >> task_match_user
