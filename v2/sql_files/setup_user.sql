-- setup user and password for database
CREATE DATABASE IF NOT EXISTS Ezy_url;
CREATE USER IF NOT EXISTS 'isaac'@'localhost' IDENTIFIED BY '1738';
GRANT ALL PRIVILEGES ON `Ezy_url`.* TO 'isaac'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'isaac'@'localhost';
FLUSH PRIVILEGES;
