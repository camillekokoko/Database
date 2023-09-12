CREATE DATABASE test1;
USE test1;

CREATE TABLE tab1 (
    recordID INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) DEFAULT NULL
);

INSERT INTO tab1(recordID, name) VALUES(1, "Fred");
INSERT INTO tab1(recordID, name) VALUES(2, "Freda");

SELECT * FROM tab1;
