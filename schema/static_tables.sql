-- Static reference tables for organizations and worker types

-- Organization table with hierarchical structure
CREATE TABLE IF NOT EXISTS org (
    name TEXT PRIMARY KEY,
    parent TEXT,
    FOREIGN KEY (parent) REFERENCES org(name)
);

-- Worker type table
CREATE TABLE IF NOT EXISTS worker_type (
    type TEXT PRIMARY KEY
);
