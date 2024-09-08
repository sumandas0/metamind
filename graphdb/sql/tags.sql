CREATE TABLE IF NOT EXISTS tags (
    name VARCHAR(255) NOT NULL,
    entity_guid VARCHAR(255) NOT NULL,
    entity_type_name VARCHAR(255) NOT NULL,
    entity_qualified_name VARCHAR(1024),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS tags_name ON tags (name);
CREATE INDEX IF NOT EXISTS tags_entity_guid ON tags (entity_guid);
CREATE INDEX IF NOT EXISTS tags_entity_type_name ON tags (entity_type_name);
CREATE INDEX IF NOT EXISTS tags_entity_qualified_name ON tags (entity_qualified_name);
CREATE INDEX IF NOT EXISTS tags_created_at ON tags (created_at);
CREATE INDEX IF NOT EXISTS tags_updated_at ON tags (updated_at);
CREATE INDEX IF NOT EXISTS tags_created_by ON tags (created_by);
CREATE INDEX IF NOT EXISTS tags_updated_by ON tags (updated_by);