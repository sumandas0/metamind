CREATE TABLE IF NOT EXISTS attributes_index (
    guid VARCHAR(255) PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL,
    qualified_name VARCHAR(1024) NOT NULL
);

CREATE INDEX IF NOT EXISTS attributes_index_type_name_qualified_name ON attributes_index (type_name, qualified_name);
CREATE INDEX IF NOT EXISTS attributes_index_guid ON attributes_index (guid);