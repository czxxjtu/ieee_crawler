CREATE TABLE Papers (
  number VARCHAR(20) NOT NULL UNIQUE,
  doi VARCHAR(50),
  spage INTEGER,
  epage INTEGER,
  issue INTEGER,
  partnum INTEGER,
  publication VARCHAR(255),
  year INTEGER,
  rank INTEGER,
  title VARCHAR(1000) NOT NULL,
  abstract VARCHAR(3000)
);


CREATE TABLE Terms (
  term VARCHAR(255) UNIQUE,
  id INTEGER AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE PaperTerms (
  paperid varchar(20),
  termid INTEGER,
  PRIMARY KEY (paperid, termid)
);

CREATE TABLE Authors (
  name VARCHAR(200) UNIQUE,
  id INTEGER AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE PaperAuthors (
  paperid VARCHAR(20),
  authorid INTEGER,
  PRIMARY KEY (paperid, authorid)
);

CREATE TABLE Publishers (
  name VARCHAR(200),
  id INTEGER AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE Log (
  date DATE,
  time TIME,
  timestamp INTEGER,
  operation VARCHAR(100),
  result VARCHAR(1000)
);

CREATE TABLE Publications (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) UNICODE NOT NULL,
  issn VARCHAR(20),
  type VARCHAR(100) NOT NULL,
  number INTEGER,
  partnum INTEGER,
  publisherid INTEGER,
  last_update INTEGER DEFAULT 0
)
