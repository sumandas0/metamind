CREATE TABLE IF NOT EXISTS relationships (
    guid VARCHAR(255) PRIMARY KEY,
    relationship_name VARCHAR(255) NOT NULL,
    source_guid VARCHAR(255) NOT NULL,
    source_type_name VARCHAR(255) NOT NULL,
    source_qualified_name VARCHAR(1024),
    target_guid VARCHAR(255) NOT NULL,
    target_type_name VARCHAR(255) NOT NULL,
    target_qualified_name VARCHAR(1024),
    relationship_type VARCHAR(255) NOT NULL,
    relationship_attributes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255) NOT NULL
);

-- Create index on relationship_name
CREATE INDEX IF NOT EXISTS relationships_relationship_name ON relationships (relationship_name);
-- Create index on source_guid
CREATE INDEX IF NOT EXISTS relationships_source_guid ON relationships (source_guid);
-- Create index on target_guid
CREATE INDEX IF NOT EXISTS relationships_target_guid ON relationships (target_guid);
-- Create index on relationship_type
CREATE INDEX IF NOT EXISTS relationships_relationship_type ON relationships (relationship_type);
-- Create composite index on source guid, target guid, relationship type, relationship name
CREATE INDEX IF NOT EXISTS relationships_source_target_relationship ON relationships (source_guid, target_guid, relationship_type, relationship_name);

-- Create index on created_at
CREATE INDEX IF NOT EXISTS relationships_created_at ON relationships (created_at);
-- Create index on updated_at
CREATE INDEX IF NOT EXISTS relationships_updated_at ON relationships (updated_at);
-- Create index on created_by
CREATE INDEX IF NOT EXISTS relationships_created_by ON relationships (created_by);
-- Create index on updated_by
CREATE INDEX IF NOT EXISTS relationships_updated_by ON relationships (updated_by);