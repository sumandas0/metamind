CREATE TYPE type_def_types AS ENUM ('entity', 'relationship');


CREATE TABLE IF NOT EXISTS type_defs (
    guid VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    super_types VARCHAR(255)[] NOT NULL,
    description TEXT,
    type type_def_types NOT NULL,
    definition JSONB,
    user_defined BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    version INTEGER NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255) NOT NULL
);

CREATE INDEX ON type_defs (name);
CREATE INDEX ON type_defs (super_types);
CREATE INDEX ON type_defs (type);
CREATE INDEX ON type_defs (version);
CREATE INDEX ON type_defs (user_defined);
CREATE INDEX ON type_defs (created_at);
CREATE INDEX ON type_defs (updated_at);
CREATE INDEX ON type_defs (created_by);
CREATE INDEX ON type_defs (updated_by);


