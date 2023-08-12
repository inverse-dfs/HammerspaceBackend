use notenote;

CREATE TABLE User (
    email varchar(100) NOT NULL,
    username varchar(100) NOT NULL,
    password varchar(200) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE Scans (
    username varchar(100) NOT NULL,
    pdf varchar(100) NOT NULL,
    latex varchar(100) NOT NULL,
    date datetime NOT NULL,
    FOREIGN KEY (username) REFERENCES User(username),
    PRIMARY KEY (username, pdf, latex)
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