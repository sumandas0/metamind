DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_def_types') THEN
        CREATE TYPE type_def_types AS ENUM ('entity', 'relationship', 'classification');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS type_defs (
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    super_type VARCHAR(255),
    alias VARCHAR(255),
    description TEXT,
    type_def_type type_def_types NOT NULL,
    properties JSONB,
    version INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255) NOT NULL
);

-- Create index on name
CREATE UNIQUE INDEX IF NOT EXISTS type_defs_name ON type_defs (name);
-- Create index on super_type
CREATE INDEX IF NOT EXISTS type_defs_super_type ON type_defs (super_type);
-- Create index on alias
CREATE INDEX IF NOT EXISTS type_defs_alias ON type_defs (alias);
-- Create index on type_def_type
CREATE INDEX IF NOT EXISTS type_defs_type_def_type ON type_defs (type_def_type);
-- Create text GIN index on description
CREATE INDEX IF NOT EXISTS type_defs_description ON type_defs USING GIN (to_tsvector('english', description));
-- Create timestamp index on created_at
CREATE INDEX IF NOT EXISTS type_defs_created_at ON type_defs (created_at);
-- Create timestamp index on updated_at
CREATE INDEX IF NOT EXISTS type_defs_updated_at ON type_defs (updated_at);
-- Create index on created_by
CREATE INDEX IF NOT EXISTS type_defs_created_by ON type_defs (created_by);
-- Create index on updated_by
CREATE INDEX IF NOT EXISTS type_defs_updated_by ON type_defs (updated_by);


