CREATE TABLE IF NOT EXISTS calendar_item(
    id INTEGER PRIMARY KEY,
    date_begins TEXT NOT NULL,
    date_ends TEXT,
    time_begins TEXT,
    time_ends TEXT,
    title TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind in ('plan','task','event','note','checkpoint')),
    status TEXT NOT NULL CHECK (status in ('planned','done','skipped','cancled')),
    priority TEXT NOT NULL CHECK (priority in (0,1,2,3)),
    created_at TEXT NOT NULL,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS  task(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    notes TEXT,
    status TEXT NOT NULL CHECK  (status in ('open','done','blocked')),
    due_at TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority in (0,1,2,3)),
    created_at TEXT NOT NULL,
    updated_at TEXT,
    completed_at TEXT
);
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS journal_body(
    id INTEGER PRIMARY KEY,
    journal_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (journal_id) REFERENCES journal (id)

);
CREATE TABLE IF NOT EXISTS weight(
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    weight TEXT NOT NULL,
    skeletal_mass TEXT,
    body_fat_percentage TEXT,
    notes TEXT
);
