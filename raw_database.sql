CREATE TABLE Raw_Papers (
  id INTEGER,
  type VARCHAR(100),
  number VARCHAR(50),
  doi VARCHAR(100),
  spage INTEGER,
  epage INTEGER,
  issue INTEGER,
  partnum INTEGER,
  publication VARCHAR(2000),
  year INTEGER,
  rank INTEGER,
  title VARCHAR(2000),
  abstract VARCHAR(10000),
  affiliation VARCHAR(2000)
);

CREATE TABLE Raw_PaperTerms (
  paperid INTEGER,
  term VARCHAR(255)
);

CREATE TABLE Raw_PaperAuthors (
  paperid INTEGER,
  author VARCHAR(255)
);