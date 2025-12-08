-- Test worker data to demonstrate over/under budget scenarios
-- Workers join from June 2024 onwards with varying pace to show budget variance

-- Sales organization workers
-- June: Add 3 workers (budget allows for growth from 20 to 22)
INSERT INTO worker (name, org, type) VALUES 
('Alice Johnson', 'Sales', 'Employee'),
('Bob Martinez', 'Sales', 'Employee'),
('Carol White', 'Sales', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-06-15', '9999-12-31', '2024-06-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Alice Johnson', 'Bob Martinez', 'Carol White');

-- July: Add 4 workers (going over budget - budget is 22, will have 7 total)
INSERT INTO worker (name, org, type) VALUES 
('David Chen', 'Sales', 'Employee'),
('Emma Davis', 'Sales', 'Consultant - Fixed'),
('Frank Wilson', 'Sales', 'Employee'),
('Grace Lee', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-07-10', '9999-12-31', '2024-07-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('David Chen', 'Emma Davis', 'Frank Wilson', 'Grace Lee');

-- August: Add 2 workers (still over budget)
INSERT INTO worker (name, org, type) VALUES 
('Henry Taylor', 'Sales', 'Employee'),
('Iris Brown', 'Sales', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-08-05', '9999-12-31', '2024-08-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Henry Taylor', 'Iris Brown');

-- September: Add 5 workers (way over budget now)
INSERT INTO worker (name, org, type) VALUES 
('Jack Anderson', 'Sales', 'Employee'),
('Kelly Moore', 'Sales', 'Employee'),
('Liam Garcia', 'Sales', 'Consultant - Fixed'),
('Maya Rodriguez', 'Sales', 'Employee'),
('Nathan Kim', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-09-01', '9999-12-31', '2024-09-01 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Jack Anderson', 'Kelly Moore', 'Liam Garcia', 'Maya Rodriguez', 'Nathan Kim');

-- October: Add only 1 worker (slowing down hiring)
INSERT INTO worker (name, org, type) VALUES 
('Olivia Thompson', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-10-15', '9999-12-31', '2024-10-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Olivia Thompson';

-- November: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Paul Martinez', 'Sales', 'Consultant - T&M'),
('Quinn Foster', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-11-08', '9999-12-31', '2024-11-08 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Paul Martinez', 'Quinn Foster');

-- December: Add 1 worker
INSERT INTO worker (name, org, type) VALUES 
('Rachel Green', 'Sales', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-12-01', '9999-12-31', '2024-12-01 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Rachel Green';


-- Marketing organization workers
-- June: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Sarah Mitchell', 'Marketing', 'Employee'),
('Tom Harris', 'Marketing', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-06-20', '9999-12-31', '2024-06-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Sarah Mitchell', 'Tom Harris');

-- July: Add 3 workers (going over budget)
INSERT INTO worker (name, org, type) VALUES 
('Uma Patel', 'Marketing', 'Employee'),
('Victor Santos', 'Marketing', 'Employee'),
('Wendy Clark', 'Marketing', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-07-15', '9999-12-31', '2024-07-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Uma Patel', 'Victor Santos', 'Wendy Clark');

-- August: Add 1 worker
INSERT INTO worker (name, org, type) VALUES 
('Xavier Lopez', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-08-12', '9999-12-31', '2024-08-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Xavier Lopez';

-- September: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Yara Ahmed', 'Marketing', 'Consultant - Fixed'),
('Zack Turner', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-09-05', '9999-12-31', '2024-09-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Yara Ahmed', 'Zack Turner');

-- October: Add 1 worker
INSERT INTO worker (name, org, type) VALUES 
('Amy Cooper', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-10-20', '9999-12-31', '2024-10-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Amy Cooper';

-- November: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Brian Scott', 'Marketing', 'Consultant - T&M'),
('Chloe Adams', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-11-10', '9999-12-31', '2024-11-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Brian Scott', 'Chloe Adams');

-- December: Add 1 worker (Drew Barrymore already exists)
INSERT INTO worker (name, org, type) VALUES 
('Derek Nelson', 'Marketing', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-12-15', '9999-12-31', '2024-12-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Derek Nelson';


-- Technology organization workers
-- June: Add 5 workers
INSERT INTO worker (name, org, type) VALUES 
('Elena Vasquez', 'Technology', 'Employee'),
('Felix Wong', 'Technology', 'Employee'),
('Gina Park', 'Technology', 'Consultant - Fixed'),
('Hugo Silva', 'Technology', 'Employee'),
('Ivy Chen', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-06-10', '9999-12-31', '2024-06-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Elena Vasquez', 'Felix Wong', 'Gina Park', 'Hugo Silva', 'Ivy Chen');

-- July: Add 6 workers (going over budget)
INSERT INTO worker (name, org, type) VALUES 
('Jake Morrison', 'Technology', 'Employee'),
('Kara Bennett', 'Technology', 'Employee'),
('Leo Ramirez', 'Technology', 'Consultant - T&M'),
('Mia Foster', 'Technology', 'Employee'),
('Noah Price', 'Technology', 'Employee'),
('Opal Hughes', 'Technology', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-07-05', '9999-12-31', '2024-07-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Jake Morrison', 'Kara Bennett', 'Leo Ramirez', 'Mia Foster', 'Noah Price', 'Opal Hughes');

-- August: Add 4 workers
INSERT INTO worker (name, org, type) VALUES 
('Peter Walsh', 'Technology', 'Employee'),
('Quincy Reed', 'Technology', 'Employee'),
('Rosa Diaz', 'Technology', 'Consultant - T&M'),
('Sam Porter', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-08-08', '9999-12-31', '2024-08-08 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Peter Walsh', 'Quincy Reed', 'Rosa Diaz', 'Sam Porter');

-- September: Add 7 workers (way over budget)
INSERT INTO worker (name, org, type) VALUES 
('Tina Brooks', 'Technology', 'Employee'),
('Uri Cohen', 'Technology', 'Employee'),
('Vera Mills', 'Technology', 'Consultant - Fixed'),
('Wade Fisher', 'Technology', 'Employee'),
('Xena Knight', 'Technology', 'Employee'),
('Yuki Tanaka', 'Technology', 'Consultant - T&M'),
('Zara Bell', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-09-12', '9999-12-31', '2024-09-12 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Tina Brooks', 'Uri Cohen', 'Vera Mills', 'Wade Fisher', 'Xena Knight', 'Yuki Tanaka', 'Zara Bell');

-- October: Add only 2 workers (slowing down)
INSERT INTO worker (name, org, type) VALUES 
('Aaron Stone', 'Technology', 'Employee'),
('Bella Cruz', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-10-18', '9999-12-31', '2024-10-18 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Aaron Stone', 'Bella Cruz');

-- November: Add 3 workers
INSERT INTO worker (name, org, type) VALUES 
('Carlos Ruiz', 'Technology', 'Consultant - Fixed'),
('Diana Ross', 'Technology', 'Employee'),
('Ethan Hunt', 'Technology', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-11-05', '9999-12-31', '2024-11-05 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Carlos Ruiz', 'Diana Ross', 'Ethan Hunt');

-- December: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Fiona Apple', 'Technology', 'Employee'),
('George Lucas', 'Technology', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-12-10', '9999-12-31', '2024-12-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Fiona Apple', 'George Lucas');


-- Quality Assurance organization workers
-- June: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Hannah Montana', 'Quality Assurance', 'Employee'),
('Ian Fleming', 'Quality Assurance', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-06-25', '9999-12-31', '2024-06-25 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Hannah Montana', 'Ian Fleming');

-- July: Add 3 workers (going over budget)
INSERT INTO worker (name, org, type) VALUES 
('Julia Roberts', 'Quality Assurance', 'Employee'),
('Kevin Bacon', 'Quality Assurance', 'Employee'),
('Laura Palmer', 'Quality Assurance', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-07-20', '9999-12-31', '2024-07-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Julia Roberts', 'Kevin Bacon', 'Laura Palmer');

-- August: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Mike Tyson', 'Quality Assurance', 'Employee'),
('Nina Simone', 'Quality Assurance', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-08-15', '9999-12-31', '2024-08-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Mike Tyson', 'Nina Simone');

-- September: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Oscar Wilde', 'Quality Assurance', 'Employee'),
('Penny Lane', 'Quality Assurance', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-09-10', '9999-12-31', '2024-09-10 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Oscar Wilde', 'Penny Lane');

-- October: Add 1 worker
INSERT INTO worker (name, org, type) VALUES 
('Quentin Tarantino', 'Quality Assurance', 'Consultant - T&M');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-10-25', '9999-12-31', '2024-10-25 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Quentin Tarantino';

-- November: Add 2 workers
INSERT INTO worker (name, org, type) VALUES 
('Rita Hayworth', 'Quality Assurance', 'Employee'),
('Steve Jobs', 'Quality Assurance', 'Employee');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-11-15', '9999-12-31', '2024-11-15 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name IN ('Rita Hayworth', 'Steve Jobs');

-- December: Add 1 worker
INSERT INTO worker (name, org, type) VALUES 
('Tilda Swinton', 'Quality Assurance', 'Consultant - Fixed');

INSERT INTO resource (RID, version, WID, res_start, res_end, proc_start, proc_end)
SELECT nextval('resource_rid_seq'), 1, WID, '2024-12-20', '9999-12-31', '2024-12-20 12:00:00', '9999-12-31 23:59:59'
FROM worker WHERE name = 'Tilda Swinton';
