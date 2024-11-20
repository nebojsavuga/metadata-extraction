import json
import uuid
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
    

def insert_general_metadata(general_data, config_path):
    db_config = load_db_config(config_path)
    server = db_config['server']
    database = db_config['database']
    driver = db_config['driver']

    # Kreiranje konekcije ka bazi
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    cursor = connection.cursor()
    
    user_id = uuid.UUID("04C6872F-334B-4D3B-9934-928DA8732E9A")
    # username = 'john_doe'
    # email = 'john.doe@example.com'
    # password = 'password123'

    # cursor.execute("""
    #     INSERT INTO Users (id, username, email, password)
    #     VALUES (?, ?, ?, ?)
    # """, (user_id, username, email, password))
    
    file_id1 = uuid.uuid4()
    cursor.execute("""
        INSERT INTO UploadedFile (id, name, size, user_id)
        VALUES (?, ?, ?, ?)
    """, (file_id1, 'document1.txt', 1024, user_id))  # 1KB fajl
    # cursor.execute("""
    #     INSERT INTO UploadedFile (id, name, size, user_id)
    #     VALUES (?, ?, ?, ?)
    # """, (file_id2, 'image1.jpg', 2048, user_id))  # 2KB fajl

    connection.commit()
    print("Sample data inserted successfully.")

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

    # Mapiranje vrednosti iz objekta general_data u tuple za SQL upit
    values = (
        file_id1,
        general_data.classification.description,  # classification_description
        general_data.classification.keywords,     # classification_keywords
        general_data.classification.purpose,        # classification_purpose
        general_data.classification.taxon_path,        # classification_taxon_path
        general_data.educational.context,  # educational_context
        general_data.educational.description,  # educational_description
        general_data.educational.difficulty,  # educational_difficulty
        general_data.educational.intended_end_user_role,  # educational_intended_end_user_role
        general_data.educational.interactivity_level,  # educational_interactivity_level
        general_data.educational.interactivity_type,  # educational_interactivity_type
        general_data.educational.language,     # educational_language
        general_data.educational.learning_resource_type,  # educational_learning_resource_type
        general_data.educational.semantic_density,  # educational_semantic_density
        general_data.educational.typical_age_range,  # educational_typical_age_range
        general_data.educational.typical_learning_time,  # educational_typical_learning_rate
        general_data.general.aggregation_level,  # general_aggregation_level
        general_data.general.coverage,    # general_coverage
        general_data.general.description[:1999],  # general_description
        general_data.general.keywords,    # general_keywords
        general_data.general.language,    # general_language
        general_data.general.structure,   # general_structure
        general_data.general.title,       # general_title
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
        None   # relation_resource
    )

    # Ubacivanje podataka u tabelu
    try:
        cursor.execute(insert_query, values)
        connection.commit()
        print("GeneralMetadata data inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        connection.rollback()

    cursor.close()
    connection.close()