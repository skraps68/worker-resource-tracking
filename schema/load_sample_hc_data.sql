-- Sample budget data for testing Forecast vs Budget feature
-- Note: Forecast data is calculated dynamically from the resource table

-- Sales organization budget
INSERT INTO hc_series (series_type, org, date, value) VALUES
('B', 'Sales', '2024-01-01', 10),
('B', 'Sales', '2024-02-01', 12),
('B', 'Sales', '2024-03-01', 15),
('B', 'Sales', '2024-04-01', 15),
('B', 'Sales', '2024-05-01', 18),
('B', 'Sales', '2024-06-01', 20)
ON CONFLICT (series_type, org, date) DO NOTHING;

-- Marketing organization budget
INSERT INTO hc_series (series_type, org, date, value) VALUES
('B', 'Marketing', '2024-01-01', 8),
('B', 'Marketing', '2024-02-01', 8),
('B', 'Marketing', '2024-03-01', 10),
('B', 'Marketing', '2024-04-01', 10),
('B', 'Marketing', '2024-05-01', 12),
('B', 'Marketing', '2024-06-01', 12)
ON CONFLICT (series_type, org, date) DO NOTHING;

-- Technology organization budget
INSERT INTO hc_series (series_type, org, date, value) VALUES
('B', 'Technology', '2024-01-01', 25),
('B', 'Technology', '2024-02-01', 28),
('B', 'Technology', '2024-03-01', 30),
('B', 'Technology', '2024-04-01', 32),
('B', 'Technology', '2024-05-01', 35),
('B', 'Technology', '2024-06-01', 38)
ON CONFLICT (series_type, org, date) DO NOTHING;

-- Quality Assurance organization budget
INSERT INTO hc_series (series_type, org, date, value) VALUES
('B', 'Quality Assurance', '2024-01-01', 5),
('B', 'Quality Assurance', '2024-02-01', 6),
('B', 'Quality Assurance', '2024-03-01', 7),
('B', 'Quality Assurance', '2024-04-01', 8),
('B', 'Quality Assurance', '2024-05-01', 8),
('B', 'Quality Assurance', '2024-06-01', 10)
ON CONFLICT (series_type, org, date) DO NOTHING;
