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

-- Headcount series table for budget and forecast time series
CREATE TABLE IF NOT EXISTS hc_series (
    series_type CHAR(1) NOT NULL CHECK (series_type IN ('B', 'F')),
    org TEXT NOT NULL,
    date DATE NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (series_type, org, date),
    FOREIGN KEY (org) REFERENCES org(name)
);
