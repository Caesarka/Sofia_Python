SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS realty (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  city TEXT NOT NULL,
  image TEXT,
  address TEXT NOT NULL,
  created_at TEXT,
  published_at TEXT,
  status INT DEFAULT 0,
  user_id INTEGER NOT NULL,
  is_deleted INT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  reg_date TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS favorite (
  user_id INTEGER,
  realty_id INTEGER,
  PRIMARY KEY (user_id, realty_id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (realty_id) REFERENCES realty(id)
);
"""