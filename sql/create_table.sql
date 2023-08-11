use CS493;

CREATE TABLE User (
    email varchar(100) NOT NULL,
    username varchar(100),
    password varchar(200) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE Scans (
    email varchar(100) NOT NULL,
    scan_id char(32) NOT NULL,
    date datetime NOT NULL,
    FOREIGN KEY (email) REFERENCES User(email),
    PRIMARY KEY (email, scan_id)
);

-- FOR LATER, FUTURE USE
-- CREATE TABLE Group_name (
--     group_id char(32) NOT NULL,
--     group_name varchar(100),
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE Folders (
--     email varchar(100) NOT NULL,
--     group_id char(32) NOT NULL,
--     scan char(32) NOT NULL,
--     PRIMARY KEY (email, group_id, scan),
--     FOREIGN KEY (scan) REFERENCES Scans(scan_id),
--     FOREIGN KEY (group_id) REFERENCES Group_name(group_id)
-- )