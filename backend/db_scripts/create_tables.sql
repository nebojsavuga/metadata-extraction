IF OBJECT_ID('Metadata', 'U') IS NOT NULL DROP TABLE Metadata;
IF OBJECT_ID('UploadedFile', 'U') IS NOT NULL DROP TABLE UploadedFile;
IF OBJECT_ID('MetadataFolders', 'U') IS NOT NULL DROP TABLE MetadataFolders;
IF OBJECT_ID('Users', 'U') IS NOT NULL DROP TABLE Users;

CREATE TABLE Users (
    id INT IDENTITY(1,1) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE MetadataFolders (
    id INT IDENTITY(1,1) NOT NULL,
    name VARCHAR(255) NOT NULL,
    parent_folder_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (parent_folder_id) REFERENCES MetadataFolders(id) ON DELETE NO ACTION
    );


CREATE TABLE UploadedFile (
    id INT IDENTITY(1,1) NOT NULL,
    name VARCHAR(255) NOT NULL,
    size VARCHAR(255) NOT NULL,
    user_id INT,
    folder_id INT,
    file_path VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (folder_id) REFERENCES MetadataFolders(id) ON DELETE SET NULL,
);

CREATE TABLE Metadata (
    id INT IDENTITY(1,1) NOT NULL,
    fileId INT,
    date_created DATETIME NOT NULL DEFAULT GETDATE(),
    classification_description VARCHAR(2000) NOT NULL,
    classification_keywords VARCHAR(2000) NOT NULL,
    classification_purpose VARCHAR(2000) NOT NULL,
    classification_taxon_path VARCHAR(2000) NOT NULL,
    educational_context VARCHAR(2000) NOT NULL,
    educational_description VARCHAR(2000) NOT NULL,
    educational_difficulty VARCHAR(2000) NOT NULL,
    educational_intended_end_user_role VARCHAR(2000) NOT NULL,
    educational_interactivity_level VARCHAR(2000) NOT NULL,
    educational_interactivity_type VARCHAR(2000) NOT NULL,
    educational_language VARCHAR(2000) NOT NULL,
    educational_learning_resource_type VARCHAR(2000) NOT NULL,
    educational_semantic_density VARCHAR(2000) NOT NULL,
    educational_typical_age_range VARCHAR(2000) NOT NULL,
    educational_typical_learning_rate VARCHAR(2000) NOT NULL,
    general_aggregation_level VARCHAR(2000) NOT NULL,
    general_coverage VARCHAR(2000) NOT NULL,
    general_description VARCHAR(2000) NOT NULL,
    general_keywords VARCHAR(2000) NOT NULL,
    general_language VARCHAR(2000) NOT NULL,
    general_structure VARCHAR(2000) NOT NULL,
    general_title VARCHAR(2000) NOT NULL,
    technical_format VARCHAR(500),
    technical_size VARCHAR(500),
    technical_location VARCHAR(2000),
    technical_requirement VARCHAR(2000),
    technical_installation_remarks VARCHAR(2000),
    technical_duration VARCHAR(2000),
    rights_cost VARCHAR(2000),
    rights_copyright_restrictions VARCHAR(2000),
    rights_description VARCHAR(4000),
    life_cycle_version VARCHAR(500),
    life_cycle_status VARCHAR(2000),
    life_cycle_contribute VARCHAR(2000),
    relation_annotation VARCHAR(2000),
    relation_kind VARCHAR(2000),
    relation_resource VARCHAR(2000),
    PRIMARY KEY (id),
    FOREIGN KEY (fileId) REFERENCES UploadedFile(id) ON DELETE CASCADE
);