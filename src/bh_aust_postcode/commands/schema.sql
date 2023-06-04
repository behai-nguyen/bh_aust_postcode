DROP TABLE IF EXISTS postcode;

CREATE TABLE postcode (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  locality TEXT NOT NULL, 
  state TEXT NOT NULL,
  postcode TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);