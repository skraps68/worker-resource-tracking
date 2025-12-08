-- Test worker data for 2025 to demonstrate over/under budget scenarios
-- Workers join from January 2025 onwards with varying pace

-- Sales organization workers - 2025
-- January: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Sandra Bullock', 'Sales', 'Employee'),
('Tom Cruise', 'Sales', 'Employee'),
('Uma Thurman', 'Sales', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-01-15', '9999-12-31', '2025-01-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Sandra Bullock', 'Tom Cruise', 'Uma Thurman');

-- February: Add 4 workers (going over budget)
INSERT INTO worker (name, org, type) VALUES 
('Vincent Price', 'Sales', 'Employee'),
('Winona Ryder', 'Sales', 'Consultant - Fixed'),
('Xavier Dolan', 'Sales', 'Employee'),
('Yvonne Strahovski', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-02-10', '9999-12-31', '2025-02-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Vincent Price', 'Winona Ryder', 'Xavier Dolan', 'Yvonne Strahovski');

-- March: Add 5 workers
INSERT INTO worker (name, org, type) VALUES 
('Zachary Quinto', 'Sales', 'Employee'),
('Angelina Jolie', 'Sales', 'Consultant - T&M'),
('Brad Pitt', 'Sales', 'Employee'),
('Cameron Diaz', 'Sales', 'Employee'),
('Denzel Washington', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-03-05', '9999-12-31', '2025-03-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Zachary Quinto', 'Angelina Jolie', 'Brad Pitt', 'Cameron Diaz', 'Denzel Washington');

-- April: Add 2 workers (slowing down)
INSERT INTO worker (name, org, type) VALUES 
('Edward Norton', 'Sales', 'Consultant - Fixed'),
('Frances McDormand', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-04-12', '9999-12-31', '2025-04-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Edward Norton', 'Frances McDormand');

-- May: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Gary Oldman', 'Sales', 'Employee'),
('Helen Mirren', 'Sales', 'Consultant - T&M'),
('Idris Elba', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-05-08', '9999-12-31', '2025-05-08 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Gary Oldman', 'Helen Mirren', 'Idris Elba');

-- June: Add 4 workers
INSERT INTO worker (name, org, type) VALUES 
('Jennifer Lawrence', 'Sales', 'Employee'),
('Keanu Reeves', 'Sales', 'Employee'),
('Leonardo DiCaprio', 'Sales', 'Consultant - Fixed'),
('Meryl Streep', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-06-15', '9999-12-31', '2025-06-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Jennifer Lawrence', 'Keanu Reeves', 'Leonardo DiCaprio', 'Meryl Streep');

-- July: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Natalie Portman', 'Sales', 'Employee'),
('Orlando Bloom', 'Sales', 'Consultant - T&M'),
('Penelope Cruz', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-07-10', '9999-12-31', '2025-07-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Natalie Portman', 'Orlando Bloom', 'Penelope Cruz');

-- August: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Quentin Blake', 'Sales', 'Employee'),
('Reese Witherspoon', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-08-05', '9999-12-31', '2025-08-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Quentin Blake', 'Reese Witherspoon');

-- September: Add 5 workers
INSERT INTO worker (name, org, type) VALUES 
('Scarlett Johansson', 'Sales', 'Consultant - Fixed'),
('Tom Hanks', 'Sales', 'Employee'),
('Viola Davis', 'Sales', 'Employee'),
('Will Smith', 'Sales', 'Employee'),
('Zoe Saldana', 'Sales', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-09-12', '9999-12-31', '2025-09-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Scarlett Johansson', 'Tom Hanks', 'Viola Davis', 'Will Smith', 'Zoe Saldana');

-- October: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Anthony Hopkins', 'Sales', 'Employee'),
('Brie Larson', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-10-18', '9999-12-31', '2025-10-18 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Anthony Hopkins', 'Brie Larson');

-- November: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Christian Bale', 'Sales', 'Consultant - T&M'),
('Daisy Ridley', 'Sales', 'Employee'),
('Ethan Hawke', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-11-05', '9999-12-31', '2025-11-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Christian Bale', 'Daisy Ridley', 'Ethan Hawke');


-- Marketing organization workers - 2025
-- January: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Emily Blunt', 'Marketing', 'Employee'),
('Forest Whitaker', 'Marketing', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-01-20', '9999-12-31', '2025-01-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Emily Blunt', 'Forest Whitaker');

-- February: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Gal Gadot', 'Marketing', 'Employee'),
('Harrison Ford', 'Marketing', 'Employee'),
('Isla Fisher', 'Marketing', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-02-15', '9999-12-31', '2025-02-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Gal Gadot', 'Harrison Ford', 'Isla Fisher');

-- March: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Jake Gyllenhaal', 'Marketing', 'Employee'),
('Kate Winslet', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-03-10', '9999-12-31', '2025-03-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Jake Gyllenhaal', 'Kate Winslet');

-- April: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Liam Neeson', 'Marketing', 'Consultant - Fixed'),
('Margot Robbie', 'Marketing', 'Employee'),
('Nicolas Cage', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-04-18', '9999-12-31', '2025-04-18 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Liam Neeson', 'Margot Robbie', 'Nicolas Cage');

-- May: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Octavia Spencer', 'Marketing', 'Employee'),
('Patrick Stewart', 'Marketing', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-05-12', '9999-12-31', '2025-05-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Octavia Spencer', 'Patrick Stewart');

-- June: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Queen Latifah', 'Marketing', 'Employee'),
('Robert Downey Jr', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-06-20', '9999-12-31', '2025-06-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Queen Latifah', 'Robert Downey Jr');

-- July: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Samuel L Jackson', 'Marketing', 'Consultant - Fixed'),
('Tessa Thompson', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-07-15', '9999-12-31', '2025-07-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Samuel L Jackson', 'Tessa Thompson');

-- August: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Vin Diesel', 'Marketing', 'Employee'),
('Whoopi Goldberg', 'Marketing', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-08-10', '9999-12-31', '2025-08-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Vin Diesel', 'Whoopi Goldberg');

-- September: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Zendaya Coleman', 'Marketing', 'Employee'),
('Adam Driver', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-09-08', '9999-12-31', '2025-09-08 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Zendaya Coleman', 'Adam Driver');

-- October: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Benedict Cumberbatch', 'Marketing', 'Consultant - Fixed'),
('Cate Blanchett', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-10-22', '9999-12-31', '2025-10-22 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Benedict Cumberbatch', 'Cate Blanchett');

-- November: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Daniel Craig', 'Marketing', 'Employee'),
('Emma Stone', 'Marketing', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-11-12', '9999-12-31', '2025-11-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Daniel Craig', 'Emma Stone');


-- Technology organization workers - 2025
-- January through November: Add workers with varying pace
-- (Similar pattern - I'll add a representative sample)

INSERT INTO worker (name, org, type) VALUES 
('Florence Pugh', 'Technology', 'Employee'),
('Greta Gerwig', 'Technology', 'Employee'),
('Hugh Jackman', 'Technology', 'Consultant - Fixed'),
('Irina Shayk', 'Technology', 'Employee'),
('John Boyega', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-01-10', '9999-12-31', '2025-01-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Florence Pugh', 'Greta Gerwig', 'Hugh Jackman', 'Irina Shayk', 'John Boyega');


-- Quality Assurance organization workers - 2025
INSERT INTO worker (name, org, type) VALUES 
('Keira Knightley', 'Quality Assurance', 'Employee'),
('Lupita Nyongo', 'Quality Assurance', 'Consultant - Fixed'),
('Michael B Jordan', 'Quality Assurance', 'Employee'),
('Naomi Watts', 'Quality Assurance', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2025-01-25', '9999-12-31', '2025-01-25 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Keira Knightley', 'Lupita Nyongo', 'Michael B Jordan', 'Naomi Watts');
