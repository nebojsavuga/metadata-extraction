import json
import pyodbc
import os


def load_db_config(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, path)
    with open(absolute_path, "r") as file:
        config = json.load(file)
    return config


def create_tables(path, config_path):
    db_config = load_db_config(config_path)
    server = db_config["server"]
    database = db_config["database"]
    driver = db_config["driver"]
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()

    with open(path, "r") as file:
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


def insert_user(config_path):
    db_config = load_db_config(config_path)
    server = db_config["server"]
    database = db_config["database"]
    driver = db_config["driver"]

    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()

    username = "nebojsa"
    email = "nebojsavuga01@gmail.com"
    password = "Password123"

    cursor.execute(
        """
        INSERT INTO Users (username, email, password)
        VALUES (?, ?, ?)
    """,
        (username, email, password),
    )
    connection.commit()
    cursor.close()
    connection.close()


def insert_general_metadata(filename, general_data, config_path):
    db_config = load_db_config(config_path)
    server = db_config["server"]
    database = db_config["database"]
    driver = db_config["driver"]

    # Kreiranje konekcije ka bazi
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
    SELECT id
    FROM Users
    WHERE email = ?
""",
        ("nebojsavuga01@gmail.com",),
    )

    user_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO UploadedFile (name, size, user_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?);
    """,
        (filename, general_data.tehnical.size, user_id),
    )

    file_id = cursor.fetchone()[0]

    connection.commit()

    # SQL upit za unos podataka u tabelu Metadata
    insert_query = """
    INSERT INTO Metadata (
        fileId,
        classification_description,
        classification_keywords,
        classification_purpose,
        classification_taxon_path,
        educational_context,
        educational_description,
        educational_difficulty,
        educational_intended_end_user_role,
        educational_interactivity_level,
        educational_interactivity_type,
        educational_language,
        educational_learning_resource_type,
        educational_semantic_density,
        educational_typical_age_range,
        educational_typical_learning_rate,
        general_aggregation_level,
        general_coverage,
        general_description,
        general_keywords,
        general_language,
        general_structure,
        general_title,
        technical_format,
        technical_size,
        technical_location,
        technical_requirement,
        technical_installation_remarks,
        technical_duration,
        rights_cost,
        rights_copyright_restrictions,
        rights_description,
        life_cycle_version,
        life_cycle_status,
        life_cycle_contribute_role,
        life_cycle_contribute_entity,
        life_cycle_contribute_date,
        relation_annotation,
        relation_kind,
        relation_resource
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?)
    """

    values = (
        file_id,
        general_data.classification.description,  # classification_description
        general_data.classification.keywords,  # classification_keywords
        general_data.classification.purpose,  # classification_purpose
        general_data.classification.taxon_path,  # classification_taxon_path
        general_data.educational.context,  # educational_context
        general_data.educational.description,  # educational_description
        general_data.educational.difficulty,  # educational_difficulty
        general_data.educational.intended_end_user_role,  # educational_intended_end_user_role
        general_data.educational.interactivity_level,  # educational_interactivity_level
        general_data.educational.interactivity_type,  # educational_interactivity_type
        general_data.educational.language,  # educational_language
        general_data.educational.learning_resource_type,  # educational_learning_resource_type
        general_data.educational.semantic_density,  # educational_semantic_density
        general_data.educational.typical_age_range,  # educational_typical_age_range
        general_data.educational.typical_learning_time,  # educational_typical_learning_rate
        general_data.general.aggregation_level,  # general_aggregation_level
        general_data.general.coverage,  # general_coverage
        general_data.general.description[:1999],  # general_description
        general_data.general.keywords,  # general_keywords
        general_data.general.language,  # general_language
        general_data.general.structure,  # general_structure
        general_data.general.title,  # general_title
        general_data.tehnical.format,  # technical_format
        general_data.tehnical.size,  # technical_size
        general_data.tehnical.location,  # technical_location
        general_data.tehnical.requirement,  # technical_requirement
        general_data.tehnical.installation_remarks,  # technical_installation_remarks
        general_data.tehnical.duration,  # technical_duration
        general_data.rights.cost,  # rights_cost
        general_data.rights.copyright,  # rights_copyright_restrictions
        general_data.rights.description,  # rights_description
        general_data.lifeCycle.version,  # life_cycle_version
        general_data.lifeCycle.status,  # life_cycle_status
        None,  # life_cycle_contribute_role
        None,  # life_cycle_contribute_entity
        None,  # life_cycle_contribute_date
        None,  # relation_annotation
        None,  # relation_kind
        None,  # relation_resource
    )

    try:
        cursor.execute(insert_query, values)
        connection.commit()
        print("GeneralMetadata data inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        connection.rollback()

    cursor.close()
    connection.close()


def get_all_files(config_path):
    db_config = load_db_config(config_path)
    server = db_config["server"]
    database = db_config["database"]
    driver = db_config["driver"]
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()
    query = "SELECT id, name, size FROM UploadedFile"
    cursor.execute(query)
    rows = cursor.fetchall()
    files = [{"id": row[0], "name": row[1], "size": row[2]} for row in rows]

    cursor.close()
    connection.close()

    return files
