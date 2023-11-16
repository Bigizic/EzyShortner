-- setup user and password for database
CREATE DATABASE IF NOT EXISTS Ezy_url;
CREATE USER IF NOT EXISTS 'ezy_user'@'localhost' IDENTIFIED BY '0000';
GRANT ALL PRIVILEGES ON `Ezy_url`.* TO 'ezy_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ezy_user'@'localhost';
FLUSH PRIVILEGES;
