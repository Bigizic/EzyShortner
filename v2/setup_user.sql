-- setup user and password for database
CREATE DATABASE IF NOT EXISTS Ezy_url_2;
CREATE USER IF NOT EXISTS 'ezy_user'@'localhost' IDENTIFIED BY '0000';
GRANT ALL PRIVILEGES ON `Ezy_url_2`.* TO 'ezy_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ezy_user'@'localhost';
FLUSH PRIVILEGES;
ALTER USER 'ezy_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '0000';
