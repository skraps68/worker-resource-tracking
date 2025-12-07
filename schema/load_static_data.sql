-- Load static reference data for org and worker_type tables

-- Load organization data (parent must be inserted before children)
INSERT INTO org (name, parent) VALUES ('All', NULL)
ON CONFLICT (name) DO NOTHING;

INSERT INTO org (name, parent) VALUES 
    ('Sales', 'All'),
    ('Marketing', 'All'),
    ('Technology', 'All'),
    ('Quality Assurance', 'All')
ON CONFLICT (name) DO NOTHING;

-- Load worker type data
INSERT INTO worker_type (type) VALUES 
    ('Employee'),
    ('Consultant - Fixed'),
    ('Consultant - T&M')
ON CONFLICT (type) DO NOTHING;
