import json
import pyodbc


def load_db_config(path):
    with open(path, 'r') as file:
        config = json.load(file)
    return config


def create_tables(path, config_path):
    db_config = load_db_config(config_path)
    server = db_config['server']
    database = db_config['database']
    driver = db_config['driver']
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()

    with open(path, 'r') as file:
        sql_script = file.read()

    try:
        cursor.execute(sql_script)
        connection.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()

    cursor.close()
    connection.close()