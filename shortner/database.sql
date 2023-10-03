-- prepares a database to store the url records

CREATE DATABASE IF NOT EXISTS Ezy_url;
USE Ezy_url;
CREATE TABLE IF NOT EXISTS records (
	Id INT PRIMARY KEY,
	Original_url VARCHAR(500) NOT NULL,
	short_url VARCHAR(10) NOT NULL
);
