CREATE TABLE IF NOT EXISTS vote_table (
    name VARCHAR(10) PRIMARY KEY,
    vote_number INT,
    last_vote TIMESTAMP
);

INSERT INTO vote_table VALUES
('Cats', 0, '2024-10-10 00:00:00')
ON CONFLICT (name) DO NOTHING;

INSERT INTO vote_table VALUES
('Dogs', 0, '2024-10-10 00:00:00')
ON CONFLICT (name) DO NOTHING;
