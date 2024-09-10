CREATE TABLE IF NOT EXISTS entities (
    guid VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    qualified_name VARCHAR(1024),
    description TEXT,
    type_name VARCHAR(255),
    attributes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS entities_type_name_qualified_name ON entities (type_name, qualified_name);
-- Create index on guid
CREATE UNIQUE INDEX IF NOT EXISTS entities_guid ON entities (guid);
-- Create index on name
CREATE INDEX IF NOT EXISTS entities_name ON entities (name);
-- Create text GIN index on description
CREATE INDEX IF NOT EXISTS entities_description ON entities USING GIN (to_tsvector('english', description));
-- Create timestamp index on created_at
CREATE INDEX IF NOT EXISTS entities_created_at ON entities (created_at);
-- Create timestamp index on updated_at
CREATE INDEX IF NOT EXISTS entities_updated_at ON entities (updated_at);
-- Create index on created_by
CREATE INDEX IF NOT EXISTS entities_created_by ON entities (created_by);
-- Create index on updated_by
CREATE INDEX IF NOT EXISTS entities_updated_by ON entities (updated_by);